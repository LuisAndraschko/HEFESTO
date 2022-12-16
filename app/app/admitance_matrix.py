import pandas as pd
import numpy as np


class DefaultDictFormat():
    """This class is responsable for hosting the static method get_dict_struct."""
    @staticmethod
    def get_dict_struct():
        """This method returns a dictionary in the following structure: {'nominal': nominal, 'base': None, 'pu': None} when just the nominal parameter is given and the folowing: {'nominal': nominal, 'base': Base, 'pu': None} when the optional parameter is given.

        :param nominal: Object to be used as value under the key 'nominal'.
        :type nominal: Object can be a instance of 1 of these 3: Voltage(), Impedance() or Power().
        :param base: When parameter nominal is an instance of Power() the base is given as the system power base, defaults to None.
        :type base: Power(), optional.
        :return: Dictionary as described in method description .
        :rtype: Dict.
        """
        keys_outer = ['impedance', 'admittance']
        keys_inner = ['series', 'shunt']
        struct_model = {}
        for key_o in keys_outer:
            struct_model[key_o] = {}
            for key_i in keys_inner:
                struct_model[key_o][key_i] = []
    
        return struct_model


class Impedance():
    instances = []

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, mag, terminals, name) -> None:
        Impedance.instances.append(self)
        self.id = len(Impedance.instances)
        self.name = name
        self.mag = mag
        self.terminals = terminals


class Admittance():
    instances = []

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, mag, terminals, name) -> None:
        Admittance.instances.append(self)
        self.id = len(Admittance.instances)
        self.name = name
        self.mag = mag
        self.terminals = terminals


class Bars():
    instances = []

    def add_instance(self):
        Bars.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    """This class models the eletric element of eletric power systems know as bar.
    """
    def __init__(self) -> None:
        """Constructor method.
        """
        self.name = 'Barra'
        self.id = None
        self.adjacent = []
        self.add_instance()

    def set_id(self, id) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.id = id

    def get_bars_iter(self, struct):
        t_list = []
        for a_z in struct.values():
            for a_z_cnx in a_z.values():
                for element in a_z_cnx:
                    for terminal in element.terminals:
                        t_list.append(terminal)
        max_terminal = sorted(t_list)[-1]
        bars_iter = [i for i in range(max_terminal + 1)]
        return bars_iter

    def set_adjacent(self, struct) -> None:
        """This method sets a list of adjacent bars to each bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        # Select component
        for a_z in struct.values():
            for a_z_cnx in a_z.values():
                for element in a_z_cnx:
                    # Match bar and component
                    if self.id in element.terminals:
                        if self.id != element.terminals[0]:
                            self.adjacent.append(element.terminals[0])
                        else:
                            self.adjacent.append(element.terminals[1])


class Validation():
    @staticmethod
    def validate_system_connections(component_list):
        continuity_check = False
        used = []
        unused = []

        for a_z in component_list.values():
            for a_z_cnx in a_z.values():
                for element in a_z_cnx:
                    unused.append(element.terminals)
                
        
        terminal_pair_count = len(unused)
        used.append(unused[0])
        unused.remove(unused[0])

        for used_pair in used:
            for used_pair_terminal in used_pair:
                if used_pair_terminal != 0:
                    for unused_pair in unused:
                        if used_pair_terminal in unused_pair:
                            used.append(unused_pair)
                            unused.remove(unused_pair)
                            break
            if len(used) == terminal_pair_count:
                continuity_check = True
                break
        return continuity_check


#################################################   SAÍDA   ##########################################################

class ValuesToMatrix():
    instances = []

    def add_instance(self):
        ValuesToMatrix.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, struct) -> None:
        self.struct = struct
        self.a_matrix = None
        self.n = None
        self.matrix_iter = None
        self.isnull = True
        self.generate_admittance_matrix()
        self.add_instance()

    def not_null(self):
        self.isnull = False

    def generate_admittance_matrix(self):
        # instantiate bars
        bars_iter = Bars().get_bars_iter(self.struct)
        bars = [Bars() for i in bars_iter]
        # Setting bars Id's
        for i, _ in enumerate(bars): bars[i].set_id(i)
        # Setting adjacent bars
        for bar in bars: bar.set_adjacent(self.struct)

        self.matrix_iter = bars_iter[:-1]
        bars_iter = bars_iter[1:]
        self.n = len(bars_iter)
        self.a_matrix = np.zeros((self.n, self.n), dtype=complex)
        admittance_sum = complex(0)
        adjacent = None

        for i_bar in bars_iter:
            for j_bar in bars_iter:
                # Get all adjacent bars to bar i
                adjacent = bars[i_bar].adjacent
                # If element in main diagonal
                if i_bar == j_bar:
                    for a_z_type, a_z in self.struct.items():
                        for a_z_cnx, value_list in a_z.items():
                            for element in value_list:
                                if 'impedance' in a_z_type and i_bar in element.terminals:
                                    admittance_sum += pow(complex(element.mag), -1)
                                elif 'admittance' in a_z_type and i_bar in element.terminals:
                                    admittance_sum += complex(element.mag)
                    self.a_matrix[i_bar - 1][j_bar - 1] = admittance_sum
                    admittance_sum = 0
                else:
                    # Get component which terminals are equal to i_bar, j_bar
                    for a_z_type, a_z in self.struct.items():
                        for a_z_cnx, value_list in a_z.items():
                            for element in value_list:
                                if i_bar in element.terminals and j_bar in element.terminals:
                                    if 'impedance' in a_z_type:
                                        self.a_matrix[i_bar - 1][j_bar - 1] = -pow(complex(element.mag), -1)
                                    elif 'admittance' in a_z_type:
                                        self.a_matrix[i_bar - 1][j_bar - 1] = -complex(element.mag)
                        
        self.not_null()


class ConvToValues():
    instances = []

    def add_instance(self):
        ConvToValues.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, component_list) -> None:
        self.component_list = component_list
        self.struct = DefaultDictFormat.get_dict_struct()
        self.create_all()
        self.add_instance()

    def create_all(self):
        for component in self.component_list:
            for attr, value in component.__dict__.items():
                if 'series_admittance' in attr:
                    # Generator case
                    if 0 in component.terminals:
                        shunt_admittance = Admittance(component.series_admittance['pu'].mag, component.terminals, 'Admitância Shunt')
                        self.struct['admittance']['shunt'].append(shunt_admittance)
                    # Other cases
                    else:
                        series_admittance = Admittance(component.series_admittance['pu'].mag, component.terminals, 'Admitância Séries')
                        self.struct['admittance']['series'].append(series_admittance)
                elif 'shunt_admittance_per_side' in attr:
                    shunt_element_1, shunt_element_2 = (0, component.terminals[0]), (0,component.terminals[1])
                    shunt_admittance_1 = Admittance(component.shunt_admittance_per_side['pu'].mag, shunt_element_1, 'Admitância Shunt')
                    shunt_admittance_2 = Admittance(component.shunt_admittance_per_side['pu'].mag, shunt_element_2, 'Admitância Shunt')
                    self.struct['admittance']['shunt'].append(shunt_admittance_1)
                    self.struct['admittance']['shunt'].append(shunt_admittance_2)


class FormToValues():
    instances = []

    def add_instance(self):
        FormToValues.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self) -> None:
        self.struct = DefaultDictFormat.get_dict_struct()
        self.isnull = True
        self.add_instance()

    def not_null(self):
        self.isnull = False

    def add_series_impedance(self, temp_form) -> None:
        series_impedance_mag = complex(temp_form.series_impedance_mag.data)
        series_impedance_terminals = (temp_form.t0.data, temp_form.t1.data)
        series_impedance = Impedance(series_impedance_mag, series_impedance_terminals, 'Impedância Série')
        self.struct['impedance']['series'].append(series_impedance)
        self.not_null()


    def add_shunt_impedance(self, temp_form) -> None:
        shunt_impedance_mag = complex(temp_form.shunt_impedance_mag.data)
        shunt_impedance_terminals = (0, temp_form.t1.data)
        shunt_impedance = Impedance(shunt_impedance_mag, shunt_impedance_terminals, 'Impedância Shunt')
        self.struct['impedance']['shunt'].append(shunt_impedance)
        self.not_null()

    def add_series_admittance(self, temp_form) -> None:
        series_admittance_mag = complex(temp_form.series_admittance_mag.data)
        series_admittance_terminals = (temp_form.t0.data, temp_form.t1.data)
        series_admittance = Impedance(series_admittance_mag, series_admittance_terminals, 'Admitância Série')
        self.struct['admittance']['series'].append(series_admittance)
        self.not_null()

    def add_shunt_admittance(self, temp_form) -> None:
        shunt_admittance_mag = complex(temp_form.shunt_admittance_mag.data)
        shunt_admittance_terminals = (0, temp_form.t1.data)
        shunt_admittance = Impedance(shunt_admittance_mag, shunt_admittance_terminals, 'Admitância Shunt')
        self.struct['admittance']['shunt'].append(shunt_admittance)
        self.not_null()


class ExcelToValues():
    instances = []

    def add_instance(self):
        ExcelToValues.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, excel) -> None:
        self.componentes = pd.read_excel(excel, sheet_name="Componentes")
        self.struct = DefaultDictFormat.get_dict_struct()
        self.populate_struct()
        self.add_instance()

    def populate_struct(self):
        df = pd.DataFrame(self.componentes)
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
                    self.struct['impedance']['series'].append(Impedance(mag, terminals, element_type))
                elif 'Admitância' in element_type:
                    self.struct['admittance']['series'].append(Admittance(mag, terminals, element_type))
            else:
                # Shunt
                terminals = (0, df.iloc[row_index, t1_column_index])
                if 'Impedância' in element_type:
                    self.struct['impedance']['shunt'].append(Impedance(mag, terminals, element_type))
                elif 'Admitância' in element_type:
                    self.struct['admittance']['shunt'].append(Admittance(mag, terminals, element_type))
            
            

class ClearObjects():
    @classmethod
    def clear_all(cls):
        Impedance.del_instances()
        Admittance.del_instances()
        Bars.del_instances()
        ValuesToMatrix.del_instances()
        ConvToValues.del_instances()
        FormToValues.del_instances()
        ExcelToValues.del_instances()

        