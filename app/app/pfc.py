import pandas as pd


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
        struct_model = {'pu': None, 'nominal': None}
        return struct_model


class Impedance():
    instances = []

    def add_instance(self):
        Impedance.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, mag, terminals, name) -> None:
        self.id = len(Impedance.instances)
        self.name = name
        self.mag = mag
        self.terminals = terminals
        self.add_instance()


class Admittance():
    instances = []

    def add_instance(self):
        Admittance.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, mag, terminals, name) -> None:
        self.id = len(Admittance.instances)
        self.name = name
        self.mag = mag
        self.terminals = terminals
        self.add_instance()


class Components():
    instances = []
    
    def add_instance(self):
        Components.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self) -> None:
        self.id = len(Components.instances)
        self.type = None
        self.terminals = None
        self.series_impedance = None
        self.series_admittance = None
        self.shunt_impedance = None
        self.shunt_admittance = None
        self.active_power_flux = None
        self.reactive_power_flux = None
        self.active_power_losses = None
        self.reactive_power_losses = None
        self.add_instance()

    def set_type(self, type):
        self.type = type

    def set_terminals(self, terminals):
        self.terminals = terminals

    def set_series_impedance(self, series_impedance):
        self.series_impedance = series_impedance
        
    def set_series_admittance(self, series_admittance):
        self.series_admittance = series_admittance
        
    def set_shunt_impedance(self, shunt_impedance):
        self.shunt_impedance = shunt_impedance
        
    def set_shunt_admittance(self, shunt_admittance):
        self.shunt_admittance = shunt_admittance
        
    def set_active_power_flux(self, active_power_flux):
        self.active_power_flux = active_power_flux
        
    def set_reactive_power_flux(self, reactive_power_flux):
        self.reactive_power_flux = reactive_power_flux
        
    def set_active_power_losses(self, active_power_losses):
        self.active_power_losses = active_power_losses
        
    def set_reactive_power_losses(self, reactive_power_losses):
        self.reactive_power_losses = reactive_power_losses


class Bars():
    instances = []
    
    def add_instance(self):
        Bars.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self) -> None:
        self.id = None
        self.type = None
        self.adjacent = None
        self.active_power_injection = None
        self.reactive_power_injection = None
        self.absolute_voltage = None
        self.voltage_phase = None
        self.add_instance()

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type
        
    def set_adjacent(self, adjacent):
        self.adjacent = adjacent
        
    def set_active_power_injection(self, active_power_injection):
        self.active_power_injection = active_power_injection
        
    def set_reactive_power_injection(self, reactive_power_injection):
        self.reactive_power_injection = reactive_power_injection
        
    def set_absolute_voltage(self, absolute_voltage):
        self.absolute_voltage = absolute_voltage
        
    def set_voltage_phase(self, voltage_phase):
        self.voltage_phase = voltage_phase


class ExcelToValues():
    instances = []

    def add_instance(self):
        ExcelToValues.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, excel) -> None:
        self.components = pd.read_excel(excel, sheet_name="Componentes")
        self.bars = pd.read_excel(excel, sheet_name="Barras")
        self.component_struct = DefaultDictFormat().get_dict_struct()
        self.create_all()
        self.add_instance()

    def create_all(self):
        self.create_components()
        self.create_bars()

    def create_components(self):
        df = pd.DataFrame(self.components)
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
                    self.component_struct['pu'].append(Impedance(mag, terminals, element_type))
                elif 'Admitância' in element_type:
                    self.component_struct['pu'].append(Admittance(mag, terminals, element_type))
            else:
                # Shunt
                terminals = (0, df.iloc[row_index, t1_column_index])
                if 'Impedância' in element_type:
                    self.component_struct['pu'].append(Impedance(mag, terminals, element_type))
                elif 'Admitância' in element_type:
                    self.component_struct['pu'].append(Admittance(mag, terminals, element_type))

    def create_bars(self):
        df = pd.DataFrame(self.bars)
        zs_column_index = df.columns.get_loc('Impedância')
        t0_column_index = df.columns.get_loc('Terminal [0]')
        t1_column_index = df.columns.get_loc('Terminal [1]')
        self.set_values(df, 'impedance', 'series', zs_column_index, t0_column_index, t1_column_index)
    

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
        element_value_column_index = df.columns.get_loc('Valor do Elemento')
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
            
            