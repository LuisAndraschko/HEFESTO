import pandas as pd
import numpy as np
import app.sys_primetives as sp
import app.sys_components as sc
import app.operations as op
import copy


############################################### Leitura de dados ########################################################
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

    def create_all(self):
        df = pd.DataFrame(self.excel).fillna('')
        component = None
        element_type_column_index = df.columns.get_loc('Tipo do Elemento')
        element_value_column_index = df.columns.get_loc('Valor do Elemento [pu]')
        t0_column_index = df.columns.get_loc('Terminal [0]')
        t1_column_index = df.columns.get_loc('Terminal [1]')

        # Assuring ground bar
        sc.Bars(0)
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
            component.add_instance()
            sc.Bars(terminals)
            

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
        copy_components = copy.deepcopy(self.component_list)
        for component in self.component_list:
            if component.name == 'Linha de Trasmissão Média':
                # Creating Components
                name_series = 'Admitância Série'
                name_shunt = 'Admitância Shunt'
                y_series = component.admittance[0]['pu']
                y_shunt = component.admittance[1]['pu']
                series = sc.Generic(terminals=component.terminals, admittance=y_series, type=name_series)
                shunt_1 = sc.Generic(terminals=(0, component.terminals[0]), admittance=y_shunt, type=name_shunt)
                shunt_2 = sc.Generic(terminals=(0, component.terminals[1]), admittance=y_shunt, type=name_shunt)
                copy_components.remove(component)
                # Inserting new components in aux list
                for new_component in (series, shunt_1, shunt_2):
                    copy_components.append(new_component)
        self.component_list = copy_components
                

class FormToComponents():
    instances = []

    def add_instance(self):
        FormToComponents.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self) -> None:
        self.isnull = True

    def not_null(self):
        self.isnull = False

    def add_component(self, temp_form) -> None:
        if temp_form.__class__.__name__ == 'PuSeriesImpedanceForm':
            series_impedance_mag = complex(temp_form.series_impedance_mag.data)
            series_impedance_terminals = (temp_form.t0.data, temp_form.t1.data)
            component = sc.Generic('Impedância Série', 
                                    series_impedance_terminals, 
                                    impedance=sp.Impedance(series_impedance_mag, '', 'pu', cnx_type='Série'))
            component.add_instance()
            sc.Bars(series_impedance_terminals)
        elif temp_form.__class__.__name__ == 'PuShuntImpedanceForm':
            shunt_impedance_mag = complex(temp_form.shunt_impedance_mag.data)
            shunt_impedance_terminals = (0, temp_form.t1.data)
            component = sc.Generic('Impedância Shunt', 
                                    shunt_impedance_terminals, 
                                    impedance=sp.Impedance(shunt_impedance_mag, '', 'pu', cnx_type='Shunt'))
            component.add_instance()
            sc.Bars(shunt_impedance_terminals)
        elif temp_form.__class__.__name__ == 'PuSeriesAdmittanceForm':
            series_admittance_mag = complex(temp_form.series_admittance_mag.data)
            series_admittance_terminals = (temp_form.t0.data, temp_form.t1.data)
            component = sc.Generic('Admitância Série', 
                                    series_admittance_terminals, 
                                    admittance=sp.Admittance(series_admittance_mag, '', 'pu', cnx_type='Série'))
            component.add_instance()
            component.add_instance()
            sc.Bars(series_admittance_terminals)            
        elif temp_form.__class__.__name__ == 'PuShuntAdmittanceForm':
            shunt_admittance_mag = complex(temp_form.shunt_admittance_mag.data)
            shunt_admittance_terminals = (0, temp_form.t1.data)
            component = sc.Generic('Admitância Shunt', 
                                    shunt_admittance_terminals, 
                                    admittance=sp.Admittance(shunt_admittance_mag, '', 'pu', cnx_type='Shunt'))
            component.add_instance()
            sc.Bars(shunt_admittance_terminals)     
        self.not_null()
                        
############################################### instanciação de objetos  #######################################################            
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
        mc = op.MagConversion()
        # Get bars
        bars = sc.Bars.get_bars()
        # Set Adjacent bars
        for bar in bars:
            bar.set_adjacent(self.component_list)
        # Set Matrix
        bar_id_list = sc.Bars.get_bars_iter()
        self.matrix_iter = bar_id_list[:-1]
        bars_iter = bar_id_list[1:]
        self.n = len(bars_iter)
        self.a_matrix = np.zeros((self.n, self.n), dtype=complex)
        admittance_sum = complex(0)
        # Generate admittance matrix
        for i_bar in bars_iter:
            for j_bar in bars_iter:
                # If element in main diagonal
                if i_bar == j_bar:
                    # Get any component with i_bar in terminals
                    for component in self.component_list:
                        if i_bar in component.terminals:
                            if component.impedance:
                                component_mag = mc.get_value(component.impedance, 'pu')
                                admittance_sum += pow(complex(component_mag), -1)
                            elif component.admittance:
                                component_mag = mc.get_value(component.admittance)
                                admittance_sum += complex(component_mag)
                    self.a_matrix[i_bar - 1][j_bar - 1] = admittance_sum
                    admittance_sum = 0
                else:
                    # Get component which terminals are equal to i_bar, j_bar
                    for component in self.component_list:
                        if i_bar in component.terminals and j_bar in component.terminals:
                            if component.impedance: 
                                component_mag = mc.get_value(component.impedance, 'pu')
                                self.a_matrix[i_bar - 1][j_bar - 1] = -pow(complex(component_mag), -1)
                            elif component.admittance:
                                component_mag = mc.get_value(component.admittance)
                                self.a_matrix[i_bar - 1][j_bar - 1] = -complex(component_mag)
                            break
        self.not_null()


######################################################################################################
    