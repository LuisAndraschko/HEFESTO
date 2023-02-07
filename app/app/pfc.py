import pandas as pd
import numpy as np
import app.sys_primetives as sp
import app.sys_components as sc
import app.admitance_matrix as gam
import app.operations as op
import cmath as cm
import copy

class ExcelToObjs:
    instances = []

    def add_instance(self):
        ExcelToObjs.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, excel) -> None:
        self.excel_bars = pd.read_excel(excel, sheet_name="Barras")
        self.excel_params = pd.read_excel(excel, sheet_name="Parâmetros")
        self.tolerance = None
        self.create_bars()
        self.create_params()
        self.add_instance()

    def create_bars(self):
        df = pd.DataFrame(self.excel_bars).fillna('')
        # Get the list of all column names from headers
        column_names = df.columns.values.tolist()
        # Getting bars excel data index columns
        bars_data_indexes = [df.columns.get_loc(column) for column in column_names]
        # Attribution struct
        prep_bar_obj = {'id': None, 
                        'type': None, 
                        'values': {'power_in': None, 
                                   'power_out': None, 
                                   'voltage': None}}

        # Getting bars created in gam.ExcelToComponents
        sc.Bars.order_bars()
        bars = sc.Bars.get_bars()
        # Assuring ground bar
        sc.Bars(0)
        for row_index, row in df.iterrows(): 
            # Processing data
            df = self.process_bars_data(df, row_index, bars_data_indexes)
            # Getting bars data
            prep_bar_obj = self.get_bars_data(prep_bar_obj, row)
                
            # Setting bar values in Bar instances
            self.set_bars(bars, prep_bar_obj)

    def process_bars_data(self, df, row_index, bars_data_indexes):
        for col_index in bars_data_indexes:
            try:
                df.iloc[row_index, col_index] = float(str((df.iloc[row_index, col_index])).replace(",", "."))
            except ValueError:
                df.iloc[row_index, col_index] = str((df.iloc[row_index, col_index])).replace(",", ".")
            except:
                df.iloc[row_index, col_index] = "ERRO NÃO PREVISTO" 
        return df

    def get_bars_data(self, prep_bar_obj, row):
        d = op.DefaultDictFormat()
        prep_bar_obj['id'] = row['Identificador']
        prep_bar_obj['values']['voltage'] = sp.Voltage(cm.rect(row['|V| [pu]'], row['θv']), '', 'pu')
        prep_bar_obj['values']['voltage'] = d.get_primitive_struct(prep_bar_obj['values']['voltage'], 'pu')
        if "SLACK" in row['Tipo de Barra']:
            prep_bar_obj['type'] = "SLACK"
        else:
            if "PV" in row['Tipo de Barra']:
                prep_bar_obj['type'] = "PV"
            else:
                prep_bar_obj['type'] = "PQ"
            load_power = complex(row['Pcarga [pu]'], row['Qcarga [pu]'])
            gen_power = complex(row['Pgeração [pu]'], row['Qgeração [pu]'])
            specified_power = gen_power - load_power
            specified_power_struct = d.get_primitive_struct(sp.Power(specified_power, '', 'pu'), 'pu')
            if specified_power.real > 0:
                prep_bar_obj['values']['power_in'] = specified_power_struct
                prep_bar_obj['values']['power_out'] = None
            elif specified_power.real < 0:
                prep_bar_obj['values']['power_out'] = specified_power_struct
                prep_bar_obj['values']['power_in'] = None
            else:
                prep_bar_obj['values']['power_in'] = None
                prep_bar_obj['values']['power_out'] = None
        return prep_bar_obj

    def set_bars(self, bars, prep_bar_obj):
        for bar in bars:
            if prep_bar_obj['id'] == bar.id:
                bar.set_bar_type(prep_bar_obj['type'])
                bar.set_power_in(prep_bar_obj['values']['power_in'])
                bar.set_power_out(prep_bar_obj['values']['power_out'])
                bar.set_voltage(prep_bar_obj['values']['voltage'])
                # Cleaning values
                prep_bar_obj['values']['power_in'] = None
                prep_bar_obj['values']['power_out'] = None
                prep_bar_obj['values']['voltage'] = None
                break

    def create_params(self):
        d = op.DefaultDictFormat()
        df = pd.DataFrame(self.excel_params).fillna('')
        
        # Get component list to attribute base voltages and power
        component_list = gam.ExcelToComponents.instances[-1].component_list
        # Get bars list to attribute base voltages
        bars = sc.Bars.get_bars()
        
        # Define base_power variable for attribution
        # Getting parms data (base power, tolerance)
        base_power = sp.Power(df.iloc[0]['Potência de Base'], df.iloc[0]['Unnamed: 5'][0], df.iloc[0]['Unnamed: 5'][1:])
        base_power = d.get_primitive_struct(base_power, 'base')
        self.tolerance = df.iloc[0]['Tolerância']
        # Define base_bar_obj variable for attribution
        prep_bar_obj = {'id': None, 
                        'base_voltage': None}

        for row_index, row in df.iterrows():
            # Getting bars data
            prep_bar_obj['id'] = row['Barra']
            prep_bar_obj['base_voltage'] = sp.Voltage(row['Tensão de Base'], row['Unnamed: 2'][0], row['Unnamed: 2'][1])
            # Setting bar voltages in Bar instances
            bar = bars[prep_bar_obj['id']]
            bar.set_voltage(prep_bar_obj['base_voltage'], 'base')
            # Setting base voltage and power in components
            self.set_components_voltage_and_power(component_list, prep_bar_obj, base_power, d)
            # Cleaning values
            prep_bar_obj['base_voltage'] = None

    def set_components_voltage_and_power(self, component_list, prep_bar_obj, base_power, d):
        # Now that the sp.Voltage has been used in bars, get dict struct for None voltages in components
        if type(prep_bar_obj['base_voltage']) != dict: 
            prep_bar_obj['base_voltage'] = d.get_primitive_struct(prep_bar_obj['base_voltage'], 'base')
        for component in component_list:
            for terminal_idx, terminal in enumerate(component.terminals):
                if prep_bar_obj['id'] == terminal and terminal_idx == 0: 
                    if not component.voltage_t0:
                        component.set_voltage_t0(prep_bar_obj['base_voltage'])
                if prep_bar_obj['id'] == terminal and terminal_idx == 1: 
                    if not component.voltage_t1:
                        component.set_voltage_t1(prep_bar_obj['base_voltage'])
            if not component.power:
                component.set_power(base_power)

class NewtonRaphson:
    instances = []

    def add_instance(self):
        NewtonRaphson.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, a_matrix_cls, tolerance) -> None:
        self.a_matrix_cls = a_matrix_cls
        self.tolerance = tolerance
        self.bars = sc.Bars.get_bars()
        self.position_type_relations = None
        self.npq = 0
        self.npv = 0
        self.x = []
        self.f_x = []
        self.jacobian = []
        self.it = 0
        self.converged = False
        self.set_npq_npv(self.bars)
        self.add_instance()

    def update_voltages(self):
        npq, npv = self.npq, self.npv
        x_1 = self.x[-1]
        new_voltages_abs = None
        new_voltages_phase = None
        new_voltage = None
        for bar in self.bars[1:]:
            bar_type = bar.bar_type
            if "SLACK" not in bar_type:
                if "PV" in bar_type:
                    for position, bar_id in enumerate(self.position_type_relations['PV']):
                        if bar.id == bar_id:
                            new_voltages_phase = x_1[position]
                            new_voltages_abs = cm.polar(bar.voltage['pu'].mag)[0]
                elif "PQ" in bar_type:
                    for position, bar_id in enumerate(self.position_type_relations['PQ']):
                        if bar.id == bar_id:
                            new_voltages_phase = x_1[npv + position]
                            new_voltages_abs = x_1[npv + npq + position]
                
                
                            
                new_voltage = sp.Voltage(complex(cm.rect(new_voltages_abs, new_voltages_phase)) , '', 'pu')
                bar.set_voltage(new_voltage, 'pu')

    def solve(self):
        self.set_position_type_relations()
        while(not self.converged):
            if self.it != 0:
                self.update_voltages()
            self.iterate()
            self.converged = np.all(np.absolute(self.f_x[-1]) <= self.tolerance)
             
    def iterate(self):
        self.evaluate_f_x()
        self.evaluate_jacobian()
        jacobian = self.jacobian[-1]
        inv_jacobian = np.linalg.inv(jacobian)
        f_x = self.f_x[-1]
        x = self.x[-1]
        x1 = x + np.matmul(inv_jacobian, f_x)
        self.x.append(x1)
        self.it += 1

    def evaluate_f_x(self):
        a_mtx = self.a_matrix_cls.a_matrix
        bars = self.bars
        npq, npv = self.npq, self.npv
        bars_total = npq + npv + 1

        ### F(X[]) e X[]
        f_x = np.zeros(2 * npq + npv)
        if self.it == 0:
            x = np.zeros(2 * npq + npv)
            
        # Elements to calculate F(X[])
        power_injection = 0
        pk_somat, qk_somat = 0, 0
        pk_calc_list, qk_calc_list = np.zeros(bars_total), np.zeros(bars_total)
        delta_pk_list, delta_qk_list = np.zeros(bars_total), np.zeros(bars_total)

        # Calculate F(X[]) and get X[] from bars
        for iter, bar in enumerate(bars[1:]):
            bar_type = bar.bar_type
            power_injection = self.get_power_injection(bar)
            bar.injected_power = power_injection
            if "SLACK" not in bar_type:
                # Defining and getting bar k interest values
                bar_k = bar.id - 1
                vk, ok = cm.polar(bar.voltage['pu'].mag)
                gkk, bkk = a_mtx[bar_k][bar_k].real, a_mtx[bar_k][bar_k].imag
                
                # Defining and getting bar m interest values
                for adjacent in bar.adjacents:
                    if adjacent != 0:
                        bar_m = adjacent - 1
                        vm, om = cm.polar(bars[adjacent].voltage['pu'].mag)
                        okm = ok - om
                        gkm, bkm = a_mtx[bar_k][bar_m].real, a_mtx[bar_k][bar_m].imag

                        # Calculating power equations terms
                        pk_somat += vm * (gkm * np.cos(okm) + bkm * np.sin(okm))
                        qk_somat += vm * (gkm * np.sin(okm) - bkm * np.cos(okm))
                
                # Finishing power equations calculations
                pk_calc_list[iter] = ((vk ** 2) * gkk) + (vk * pk_somat)
                qk_calc_list[iter] = -((vk ** 2) * bkk) + (vk * qk_somat)

                # Defining power residues values
                delta_pk_list[iter] = power_injection.real - pk_calc_list[iter]
                delta_qk_list[iter] = power_injection.imag - qk_calc_list[iter]
                
                # Attributing to F[x] and x 
                if self.it == 0:
                    x = self.attribute_x_or_f_x(x, {'type': 'theta', 'value': ok}, bar, npq, npv)
                f_x = self.attribute_x_or_f_x(f_x, {'type': 'P', 'value': delta_pk_list[iter]}, bar, npq, npv)
                if "PQ" in bar_type:
                    f_x = self.attribute_x_or_f_x(f_x, {'type': 'Q', 'value': delta_qk_list[iter]}, bar, npq, npv)
                    if self.it == 0:
                        x = self.attribute_x_or_f_x(x, {'type': 'v', 'value': vk}, bar, npq, npv)
                pk_somat = 0
                qk_somat = 0
        if self.it == 0:
            self.x.append(x)
        self.f_x.append(f_x)

    def evaluate_jacobian(self):
        a_mtx = self.a_matrix_cls.a_matrix
        bars = self.bars
        
        ### JACOBIANA
        ## H
        h_matrix = self.calculate_h_matrix(a_mtx, bars, self.npq, self.npv)
        ## N
        n_matrix = self.calculate_n_matrix(a_mtx, bars, self.npq, self.npv)
        ## N
        m_matrix = self.calculate_m_matrix(a_mtx, bars, self.npq, self.npv)
        ## L
        l_matrix = self.calculate_l_matrix(a_mtx, bars, self.npq, self.npv)
        #Join
        hn = np.concatenate((h_matrix, n_matrix), axis=1)
        ml = np.concatenate((m_matrix, l_matrix), axis=1)
        jacobian = np.concatenate((hn, ml), axis=0)
        self.jacobian.append(jacobian)

    def calculate_h_matrix(self, a_mtx, bars, npq, npv):
        h_matrix = np.zeros((npq + npv, npq + npv))
        rows = self.get_rows_jacobian_mtx("H")
        cols = self.get_cols_jacobian_mtx("H")
        # Itera H
        for row, bar_row in enumerate(rows):
            # Bar voltage slow iteration
            vk, ok = cm.polar(bars[bar_row].voltage['pu'].mag)
            for col, bar_col in enumerate(cols):
                # Logical Tests for sub matrix
                is_diagonal_term_h_mtx = True if bar_row == bar_col else False
                if not is_diagonal_term_h_mtx:
                    # m bar voltage
                    vm, om = cm.polar(bars[bar_col].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[bar_row - 1][bar_col -1]
                    gkm, bkm = ykm.real, ykm.imag
                    # Elemento kl
                    h_matrix[row][col] += vk * vm * (gkm * np.sin(okm) - bkm * np.cos(okm))
                else:
                    for adjacent_bar in bars[bar_row].adjacents:
                        if adjacent_bar != 0:
                            # adjacent_bar voltage
                            vm, om = cm.polar(bars[adjacent_bar].voltage['pu'].mag)
                            okm = ok - om
                            ykm = a_mtx[bar_row - 1][adjacent_bar -1]
                            gkm, bkm = ykm.real, ykm.imag
                            # Termo do somatório kk
                            h_matrix[row][col] += vm * (-gkm * np.sin(okm) + bkm * np.cos(okm))
                    h_matrix[row][col] *= vk
        return h_matrix

    def calculate_n_matrix(self, a_mtx, bars, npq, npv):
        n_matrix = np.zeros((npq + npv, npq))
        rows = self.get_rows_jacobian_mtx("N")
        cols = self.get_cols_jacobian_mtx("N")
        gkk, bkk = 0, 0
        # Itera N
        for row, bar_row in enumerate(rows):
            # Bar voltage slow iteration
            vk, ok = cm.polar(bars[bar_row].voltage['pu'].mag)
            for col, bar_col in enumerate(cols):
                # Logical Tests for sub matrix
                is_diagonal_term_n_mtx = True if bar_row == bar_col else False
                if not is_diagonal_term_n_mtx:
                    # m bar voltage
                    vm, om = cm.polar(bars[bar_col].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[bar_row - 1][bar_col -1]
                    gkm, bkm = ykm.real, ykm.imag
                    # Elemento kl
                    n_matrix[row][col] += vk * (gkm * np.cos(okm) + bkm * np.sin(okm))
                else:
                    ykm = a_mtx[bar_row - 1][bar_row - 1]
                    gkk, bkk = ykm.real, ykm.imag
                    for adjacent_bar in bars[bar_row].adjacents:
                        if adjacent_bar != 0:
                            # adjacent_bar voltage
                            vm, om = cm.polar(bars[adjacent_bar].voltage['pu'].mag)
                            okm = ok - om
                            ykm = a_mtx[bar_row - 1][adjacent_bar -1]
                            gkm, bkm = ykm.real, ykm.imag
                            # Termo do somatório kk
                            n_matrix[row][col] += vm * (gkm * np.cos(okm) + bkm * np.sin(okm))
                    n_matrix[row][col] += 2 * vk * gkk
        return n_matrix

    def calculate_m_matrix(self, a_mtx, bars, npq, npv):
        m_matrix = np.zeros((npq, npq + npv))
        rows = self.get_rows_jacobian_mtx("M")
        cols = self.get_cols_jacobian_mtx("M")
        # Itera M
        for row, bar_row in enumerate(rows):
            # Bar voltage slow iteration
            vk, ok = cm.polar(bars[bar_row].voltage['pu'].mag)
            for col, bar_col in enumerate(cols):
                # Logical Tests for sub matrix
                is_diagonal_term_m_mtx = True if bar_row == bar_col else False
                if not is_diagonal_term_m_mtx:
                    # m bar voltage
                    vm, om = cm.polar(bars[bar_col].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[bar_row - 1][bar_col -1]
                    gkm, bkm = ykm.real, ykm.imag
                    # Elemento kl
                    m_matrix[row][col] += -vk * vm * (gkm * np.cos(okm) + bkm * np.sin(okm))
                else:
                    for adjacent_bar in bars[bar_row].adjacents:
                        if adjacent_bar != 0:
                            # adjacent_bar voltage
                            vm, om = cm.polar(bars[adjacent_bar].voltage['pu'].mag)
                            okm = ok - om
                            ykm = a_mtx[bar_row - 1][adjacent_bar -1]
                            gkm, bkm = ykm.real, ykm.imag
                            # Termo do somatório kk
                            m_matrix[row][col] += vm * (gkm * np.cos(okm) + bkm * np.sin(okm))
                    m_matrix[row][col] *= vk
        return m_matrix

    def calculate_l_matrix(self, a_mtx, bars, npq, npv):
        l_matrix = np.zeros((npq, npq))
        rows = self.get_rows_jacobian_mtx("L")
        cols = self.get_cols_jacobian_mtx("L")
        gkk, bkk = 0, 0
        # Itera L
        for row, bar_row in enumerate(rows):
            # Bar voltage slow iteration
            vk, ok = cm.polar(bars[bar_row].voltage['pu'].mag)
            for col, bar_col in enumerate(cols):
                # Logical Tests for sub matrix
                is_diagonal_term_l_mtx = True if bar_row == bar_col else False
                if not is_diagonal_term_l_mtx:
                    _vm, om = cm.polar(bars[bar_col].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[bar_row - 1][bar_col -1]
                    gkm, bkm = ykm.real, ykm.imag
                    # Elemento kl
                    l_matrix[row][col] += vk * (gkm * np.sin(okm) - bkm * np.cos(okm))
                else:
                    ykm = a_mtx[bar_row - 1][bar_row -1]
                    gkk, bkk = ykm.real, ykm.imag
                    for adjacent_bar in bars[bar_row].adjacents:
                        if adjacent_bar != 0:
                            # adjacent_bar voltage
                            vm, om = cm.polar(bars[adjacent_bar].voltage['pu'].mag)
                            okm = ok - om
                            ykm = a_mtx[bar_row - 1][adjacent_bar -1]
                            gkm, bkm = ykm.real, ykm.imag
                            # Termo do somatório kk
                            l_matrix[row][col] += vm * (gkm * np.sin(okm) - bkm * np.cos(okm))
                    l_matrix[row][col] += -2 * vk * bkk
        return l_matrix

    def get_cols_jacobian_mtx(self, mtx_type):
        cols = []
        if mtx_type == "H" or mtx_type == "M":
            cols = self.position_type_relations['PQPV']
        elif mtx_type == "N" or mtx_type == "L":
            cols = self.position_type_relations['PQ']
        return cols

    def get_rows_jacobian_mtx(self, mtx_name):
        rows = []
        if mtx_name == "H" or mtx_name == "N":
            rows = self.position_type_relations['PQPV']
        elif mtx_name == "M" or mtx_name == "L":
            rows = self.position_type_relations['PQ']
        return rows

    def set_npq_npv(self, bars):
        for bar in bars[1:]:
            if "PQ" in bar.bar_type:
                self.npq += 1
            elif "PV" in bar.bar_type:
                self.npv += 1 

    def get_power_injection(self, bar):
        if bar.power_in:
            power_injection = bar.power_in['pu'].mag
        elif bar.power_out:
            power_injection = bar.power_out['pu'].mag
        else:
            power_injection = 0
        return power_injection

    def set_position_type_relations(self):
        bars = sc.Bars.get_bars()
        position_type_relations = {'SLACK': 1, 'PQ': [], 'PV': [], 'PQPV': []}
        for bar in bars[1:]:
            bar_type = bar.bar_type
            if "PQ" in bar_type:
                position_type_relations['PQ'].append(bar.id)
                position_type_relations['PQPV'].append(bar.id)
            elif "PV" in bar_type:
                position_type_relations['PV'].append(bar.id)
                position_type_relations['PQPV'].append(bar.id)
            else:
                position_type_relations['SLACK'] = bar.id
        position_type_relations['PQ'].sort()
        position_type_relations['PV'].sort()
        position_type_relations['PQPV'].sort()
        self.position_type_relations = position_type_relations

    def attribute_x_or_f_x(self, vector, value, current_bar, npq, npv):
        for position, bar_id in enumerate(self.position_type_relations[current_bar.bar_type]):
            if bar_id == current_bar.id:
                if "PV" in current_bar.bar_type:
                    # Posição para P e O nas PV
                    vector[position] = value['value']
                    break
                if "PQ" in current_bar.bar_type:
                    # Posição para P e O nas PQ
                    if 'theta' in value['type'] or 'P' in value['type']:
                        vector[npv + position] = value['value']
                    # Posição para Q e V nas PQ
                    else:
                        vector[position + npq + npv] = value['value']
                    break
        return vector
    

class PowerFluxOperations:
    instances = []

    def add_instance(self):
        PowerFluxOperations.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, a_matrix_cls) -> None:
        self.component_list = gam.ExcelToComponents.instances[-1].component_list
        self.bars = sc.Bars.get_bars()
        self.a_matrix_cls = a_matrix_cls
        self.slack_active_power = 0
        
        self.add_instance()

    def calculate_power_inj(self):
        self.calculate_active_power_inj()
        self.calculate_reactive_power_inj()

    def calculate_active_power_inj(self):
        a_mtx = self.a_matrix_cls.a_matrix
        aux = 0
        for bar in self.bars[1:]:
            bar.injected_power = 0
            k_idx = bar.id - 1
            # Bar voltage slow iteration
            vk, ok = cm.polar(self.bars[bar.id].voltage['pu'].mag)
            for adjacent_bar in bar.adjacents:
                if adjacent_bar != 0:
                    # adjacent_bar voltage
                    vm, om = cm.polar(self.bars[adjacent_bar].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[k_idx][adjacent_bar -1]
                    gkm, bkm = ykm.real, ykm.imag
                    # Termo do somatório kk
                    aux += vm * (gkm * np.cos(okm) + bkm * np.sin(okm))
            bar.injected_power = ((vk ** 2) * a_mtx[k_idx][k_idx].real) + (vk * aux)
                
    def calculate_reactive_power_inj(self):
        a_mtx = self.a_matrix_cls.a_matrix
        aux = 0
        for bar in self.bars[1:]:
            pk = bar.injected_power
            k_idx = bar.id - 1
            # Bar voltage slow iteration
            vk, ok = cm.polar(self.bars[bar.id].voltage['pu'].mag)
            for adjacent_bar in bar.adjacents:
                if adjacent_bar != 0:
                    m_idx = adjacent_bar -1
                    # adjacent_bar voltage
                    vm, om = cm.polar(self.bars[adjacent_bar].voltage['pu'].mag)
                    okm = ok - om
                    ykm = a_mtx[k_idx][m_idx]
                    gkm, bkm = ykm.real, ykm.imag
                    # Termo do somatório kk
                    aux += vm * (gkm * np.sin(okm) - bkm * np.cos(okm))
            qk = -((vk ** 2) * a_mtx[k_idx][k_idx].imag) + (vk * aux)
            if qk >= 0:
                bar.injected_power = complex(f'{pk}+{qk}j')
            else:
                bar.injected_power = complex(f'{pk}{qk}j')
    
    def calculate_flux(self):
        for component in self.component_list:
            if 'Série' in component.type:
                bar_k, bar_m = component.terminals

                vk, ok = cm.polar(self.bars[bar_k].voltage['pu'].mag)
                vm, om = cm.polar(self.bars[bar_m].voltage['pu'].mag)
                okm = ok - om

                ykm = self.get_component_admittance(component)
                gkm, bkm = ykm.real, ykm.imag

                shunt_km = self.check_for_shunt(bar_k, bar_m)
                shunt_mk = self.check_for_shunt(bar_m, bar_k)
                bkm_sh = self.get_component_admittance(shunt_km)
                bmk_sh = self.get_component_admittance(shunt_mk)

                pkm = ((vk ** 2) * gkm) - (vk * vm * gkm * np.cos(okm)) - (vk * vm * bkm * np.sin(okm))
                qkm = -((vk ** 2) * (bkm_sh + bkm)) - (vk * vm * gkm * np.sin(okm)) + (vk * vm * bkm * np.cos(okm))

                pmk = ((vm ** 2) * gkm) - (vk * vm * gkm * np.cos(okm)) + (vk * vm * bkm * np.sin(okm))
                qmk = -((vm ** 2) * (bmk_sh + bkm)) + (vk * vm * gkm * np.sin(okm)) + (vk * vm * bkm * np.cos(okm))
                
                component.flux_km = complex(pkm, qkm) * component.power['base'].mag
                component.flux_mk = complex(pmk, qmk) * component.power['base'].mag
                
    def check_for_shunt(self, bar_k, bar_m):
        shunt_list = []
        selected_shunt = None
        # Para cada componente
        for component in self.component_list:
            # Se o terminal k estiver nos terminais do componente e o componente for shunt
            if bar_k in component.terminals and 'Shunt' in component.type:
                shunt_list.append(component)

        # Para cada componente
        for component in self.component_list:
            # Se o terminal m estiver nos terminais do componente e o componente for shunt
            if bar_m in component.terminals and 'Shunt' in component.type:
                shunt_list.append(component)

        for shunt_compare in shunt_list[1:]:
            try:
                if shunt_list[0].impedance.is_equal(shunt_compare.impedance):
                    selected_shunt = shunt_compare
                    break
            except AttributeError:
                if shunt_list[0].admittance.is_equal(shunt_compare.admittance):
                    selected_shunt = shunt_compare
                    break
            try:
                if shunt_list[0].admittance.is_equal(shunt_compare.impedance):
                    selected_shunt = shunt_compare
                    break
            except AttributeError:
                if shunt_list[0].impedance.is_equal(shunt_compare.admittance):
                    selected_shunt = shunt_compare
                    break
        
        return selected_shunt
    
    def get_component_admittance(self, component):
        admittance = 0
        if component:
            if 'Impedância' in component.type:
                admittance = 1 / complex(component.impedance.mag)
            else:
                admittance = complex(component.admittance.mag)
        return admittance