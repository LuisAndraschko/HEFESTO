import pandas as pd
import numpy as np
import app.sys_primetives as sp
import app.sys_components as sc
import app.operations as op


################################## Leitura de dados e instanciação de objetos ####################################
class ExcelToComponents():
    instances = []

    def add_instance(self):
        ExcelToComponents.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, excel) -> None:
        self.excel = pd.read_excel(excel, sheet_name="Componentes")
        self.component_list = []
        self.create_all()
        self.add_instance()

    def create_all(self):
        df = pd.DataFrame(self.excel)
        component = None
        element_type_column_index = df.columns.get_loc('Tipo do Elemento')
        element_value_column_index = df.columns.get_loc('Valor do Elemento [pu]')
        t0_column_index = df.columns.get_loc('Terminal [0]')
        t1_column_index = df.columns.get_loc('Terminal [1]')

        for row_index, _ in df.iterrows():    
            element_type = df.iloc[row_index, element_type_column_index]
            mag = str(df.iloc[row_index, element_value_column_index]).replace(",", ".")
            if "Série" in element_type:
                # Series
                terminals = (df.iloc[row_index, t0_column_index], df.iloc[row_index, t1_column_index])
                if 'Impedância' in element_type:
                    component = sc.Generic(element_type, terminals, impedance=sp.Impedance(mag, '', 'pu', cnx_type='Série'))
                elif 'Admitância' in element_type:
                    component = sc.Generic(element_type, terminals, admittance=sp.Admittance(mag, '', 'pu', cnx_type='Série'))
            else:
                # Shunt
                terminals = (0, df.iloc[row_index, t1_column_index])
                if 'Impedância' in element_type:
                    component = sc.Generic(element_type, terminals, impedance=sp.Impedance(mag, '', 'pu', cnx_type='Shunt'))
                elif 'Admitância' in element_type:
                    component = sc.Generic(element_type, terminals, admittance=sp.Admittance(mag, '', 'pu', cnx_type='Shunt'))
            sc.Bars(terminals)
            self.component_list.append(component)
            

class ConvToComponents():
    instances = []

    def add_instance(self):
        ConvToComponents.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, component_list) -> None:
        self.component_list = component_list
        self.create_all()
        self.add_instance()

    def create_all(self):
        mc = op.MagConversion()
        aux = []
        for component in self.component_list:
            if component.name == 'Linha de Trasmissão Média':
                # Creating Components
                name_series = 'Admitância Série'
                name_shunt = 'Admitância Shunt'
                y_mag_series = mc.get_value(component.admittance[0])
                y_mag_shunt = mc.get_value(component.admittance[1])
                series = sc.Generic(name_series, component.terminals, admittance=y_mag_series)
                shunt_1 = sc.Generic(name_shunt, (0, component.terminals[0]), admittance=y_mag_shunt)
                shunt_2 = sc.Generic(name_shunt, (0, component.terminals[1]), admittance=y_mag_shunt)
                # Inserting new components in aux list
                for new_component in (series, shunt_1, shunt_2):
                    self.aux.append(new_component)
            else:
                aux.append(component)
        self.component_list = aux
                

class FormToComponents():
    instances = []

    def add_instance(self):
        FormToComponents.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self) -> None:
        self.component_list = None
        self.isnull = True
        self.add_instance()

    def not_null(self):
        self.isnull = False

    def add_component(self, temp_form, name) -> None:
        series_impedance_mag = complex(temp_form.series_impedance_mag.data)
        series_impedance_terminals = (temp_form.t0.data, temp_form.t1.data)
        series_impedance = Impedance(series_impedance_mag, series_impedance_terminals, 'Impedância Série')
        self.component_list['impedance']['series'].append(series_impedance)
        self.not_null()

    def add_series_impedance(self, temp_form) -> None:
        series_impedance_mag = complex(temp_form.series_impedance_mag.data)
        series_impedance_terminals = (temp_form.t0.data, temp_form.t1.data)
        series_impedance = Impedance(series_impedance_mag, series_impedance_terminals, 'Impedância Série')
        self.component_list['impedance']['series'].append(series_impedance)
        self.not_null()


    def add_shunt_impedance(self, temp_form) -> None:
        shunt_impedance_mag = complex(temp_form.shunt_impedance_mag.data)
        shunt_impedance_terminals = (0, temp_form.t1.data)
        shunt_impedance = Impedance(shunt_impedance_mag, shunt_impedance_terminals, 'Impedância Shunt')
        self.component_list['impedance']['shunt'].append(shunt_impedance)
        self.not_null()

    def add_series_admittance(self, temp_form) -> None:
        series_admittance_mag = complex(temp_form.series_admittance_mag.data)
        series_admittance_terminals = (temp_form.t0.data, temp_form.t1.data)
        series_admittance = Impedance(series_admittance_mag, series_admittance_terminals, 'Admitância Série')
        self.component_list['admittance']['series'].append(series_admittance)
        self.not_null()

    def add_shunt_admittance(self, temp_form) -> None:
        shunt_admittance_mag = complex(temp_form.shunt_admittance_mag.data)
        shunt_admittance_terminals = (0, temp_form.t1.data)
        shunt_admittance = Impedance(shunt_admittance_mag, shunt_admittance_terminals, 'Admitância Shunt')
        self.component_list['admittance']['shunt'].append(shunt_admittance)
        self.not_null()
                        
######################################################################################################            
class ComponentsToMatrix():
    instances = []

    def add_instance(self):
        ComponentsToMatrix.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, component_list) -> None:
        self.component_list = component_list
        self.a_matrix = None
        self.n = None
        self.matrix_iter = None
        self.isnull = True
        self.generate_admittance_matrix()
        self.add_instance()

    def not_null(self):
        self.isnull = False

    def generate_admittance_matrix(self):
        # Get bars
        bars = sc.Bars.get_bars()
        # Setting adjacent bars
        for bar in bars: 
            if bar.id != 0:
                bar.set_adjacent(self.component_list)
        self.matrix_iter = sc.Bars.get_bars_iter()[:-1]
        bars_iter = bars_iter[1:]
        self.n = len(bars_iter)
        self.a_matrix = np.zeros((self.n, self.n), dtype=complex)
        admittance_sum = complex(0)

        for i_bar in bars_iter:
            for j_bar in bars_iter:
                # If element in main diagonal
                if i_bar == j_bar:
                    # Get any component with i_bar in terminals
                    for component in self.component_list:
                        if i_bar in component.terminals:
                            if component.impedance:
                                admittance_sum += pow(complex(component.impedance.mag), -1)
                            elif component.admittance:
                                admittance_sum += complex(component.admittance)
                    self.a_matrix[i_bar - 1][j_bar - 1] = admittance_sum
                    admittance_sum = 0
                else:
                    # Get component which terminals are equal to i_bar, j_bar
                    for component in self.component_list:
                        if i_bar in component.terminals and j_bar in component.terminals:
                            if component.impedance: 
                                self.a_matrix[i_bar - 1][j_bar - 1] = -pow(complex(component.impedance.mag), -1)
                            elif component.admittance:
                                self.a_matrix[i_bar - 1][j_bar - 1] = -complex(component.admittance.mag)
        self.not_null()


######################################################################################################
    