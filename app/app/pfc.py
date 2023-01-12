import pandas as pd
import numpy as np
import app.sys_primetives as sp
import app.sys_components as sc
import app.operations as op
import cmath as cm


class ExcelToBars:
    bars_list = []

    def add_instance(self):
        ExcelToBars.bars_list.append(self)

    @classmethod
    def del_instances(cls):
        cls.bars_list = []

    def __init__(self, excel) -> None:
        self.excel = pd.read_excel(excel, sheet_name="Barras")
        self.create_all()
        self.add_instance()

    def create_all(self):
        d = op.DefaultDictFormat()
        df = pd.DataFrame(self.excel).fillna('')
        
        # Get the list of all column names from headers
        column_names = df.columns.values.tolist()
        # Getting bars excel data index columns
        bars_data_indexes = [df.columns.get_loc(column) for column in column_names]
        
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
            for col_index in bars_data_indexes:
                try:
                    df.iloc[row_index, col_index] = float(str((df.iloc[row_index, col_index])).replace(",", "."))
                except ValueError:
                    df.iloc[row_index, col_index] = str((df.iloc[row_index, col_index])).replace(",", ".")
                except:
                    df.iloc[row_index, col_index] = "ERRO NÃO PREVISTO"  

            # Getting bars data
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
            
            # Setting bar values in Bar instances
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
            

class PowerEquations:
    instances = []

    def add_instance(self):
        PowerEquations.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, a_matrix_cls) -> None:
        self.a_matrix_cls = a_matrix_cls
        self.add_instance()

    def get_power_injection(self, bar):
        if bar.power_in:
            power_injection = bar.power_in['pu'].mag
        elif bar.power_out:
            power_injection = bar.power_out['pu'].mag
        else:
            power_injection = 0
        return power_injection


    def evaluate(self):
        bars = sc.Bars.get_bars()
        bars_df = sc.Bars.get_bars_df()
        npq = 0
        npv = 0

        for _row_index, row in bars_df.iterrows():
            if row['Tipo de Barra'] == 'PQ':
                npq += 1
            elif row['Tipo de Barra'] == 'PV':
                npv += 1

        
        f_x = np.zeros(2 * npq + npv)
        x = np.zeros(2 * npq + npv)
        g_matrix, b_matrix = self.split_a_matrix()
        power_injection = 0
        p_sum, q_sum = 0, 0
        p_index, q_index = 0, 0
        for bar in bars[1:]:
            bar_type = bar.bar_type
            if "SLACK" not in bar_type:
                bar_k = bar.id - 1
                vk, ok = cm.polar(bar.voltage['pu'].mag)
                for adjacent in bar.adjacents:
                    if adjacent != bar.id:
                        bar_m = adjacent - 1
                        vm, om = cm.polar(bars[adjacent].voltage['pu'].mag)
                        p_sum -= vm * (g_matrix[bar_k][bar_m] * np.cos(ok - om) + b_matrix[bar_k][bar_m] * np.sin(ok - om))
                        if "PQ" in bar_type:
                            q_sum -= vm * (g_matrix[bar_k][bar_m] * np.sin(ok - om) - b_matrix[bar_k][bar_m] * np.cos(ok - om))
                p_sum *= vk
                power_injection = self.get_power_injection(bar)
                p_sum += power_injection.real - (vk ** 2) * g_matrix[bar_k][bar_k]
                f_x[p_index] = p_sum
                x[p_index] = ok

                if "PQ" in bar_type:
                    q_sum *= vk
                    q_sum += power_injection.imag + (vk ** 2) * b_matrix[bar_k][bar_k]
                    f_x[q_index + (npv + npq)] = q_sum
                    x[q_index + (npv + npq)] = vk
                    q_index += 1
                else:
                    #PV
                    x[p_index] = ok
                p_index += 1
                p_sum = 0
                q_sum = 0
        print("")



        #Pesp e Qesp nas barras.power_in ou power_out - shape(13,)
        #G e B em g_matrix, b_matrix                  - shape(8, 8)

        #Para cada Pesp Qesp (barra) rodar por todas adjacentes
        
        #Adjacentes sobrando zeros

        



    def split_a_matrix(self):
        a_matrix_dim = self.a_matrix_cls.a_matrix.shape
        g_matrix = np.zeros(a_matrix_dim)
        b_matrix = np.zeros(a_matrix_dim)
        for index, value in np.ndenumerate(self.a_matrix_cls.a_matrix):
            if value.real:
                g_matrix[index[0], index[1]] = value.real
            if value.imag:
                b_matrix[index[0], index[1]] = value.imag
        return g_matrix, b_matrix