import app.sys_primetives as sp
import app.operations as op

class Components():
    def __init__(self, terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic) -> None:
        self.terminals = terminals
        self.impedance = impedance
        self.admittance = admittance
        self.power = power
        self.voltage_t0 = voltage_t0
        self.voltage_t1 = voltage_t1
        self.pf = pf
        self.characteristic = characteristic

    def set_terminals(self, terminals):
        self.terminals = terminals

    def set_impedance(self, impedance, key=None):
        if key:
            self.impedance[key] = impedance
        else:
            self.impedance = impedance

    def set_admittance(self, admittance, key=None, append=None):
        if key:
            self.admittance[key] = admittance
        else:
            self.admittance = admittance
        
    def set_power(self, power, key=None):
        if key:
            self.power[key] = power
        else:
            self.power = power

    def set_voltage_t0(self, voltage_t0, key=None):
        if key:
            self.voltage_t0[key] = voltage_t0
        else:
            self.voltage_t0 = voltage_t0

    def set_voltage_t1(self, voltage_t1, key=None):
        if key:
            self.voltage_t1[key] = voltage_t1
        else:
            self.voltage_t1 = voltage_t1

    def set_pf(self, pf):
        self.pf = pf

    def set_characteristic(self, characteristic):
        self.characteristic = characteristic


class Generators(Components):
    """This class models the eletric component of eletric power systems know as generator.
    """
    instances = []

    def add_instance(self):
        Generators.instances.append(self)

    def get_id(self):
        return len(Generators.instances)

    def __init__(self, terminals=None, impedance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None, admittance=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.id = self.get_id()
        self.name = 'Gerador'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()
     
    @classmethod
    def del_instances(cls):
        cls.instances = []


class Transformers(Components):
    """This class models the eletric component of eletric power systems know as transformer.
    """
    instances = []

    def get_id(self):
        return len(Transformers.instances)

    def add_instance(self):
        Transformers.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None, admittance=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.id = self.get_id()
        self.name = 'Transformador'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class ShortTLines(Components):
    """This class models the eletric component of eletric power systems know as short transmission line.
    """
    instances = []
    
    def get_id(self):
        return len(ShortTLines.instances)

    def add_instance(self):
        ShortTLines.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None, admittance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.id = self.get_id()
        self.name = 'Linha de Transmissão Pequena'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class MediumTLines(Components):
    """This class models the eletric component of eletric power systems know as medium transmission line.
    """
    instances = []
    
    def get_id(self):
        return len(MediumTLines.instances)

    def add_instance(self):
        MediumTLines.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None, admittance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.id = self.get_id()
        self.name = 'Linha de Trasmissão Média'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    def set_impedance(self, impedance, cnx_type=None, key=None):
        if cnx_type == 'Série':
            if key:
                self.impedance[0][key] = impedance
            else:
                self.impedance[0] = impedance
        elif cnx_type == 'Shunt':
            if key:
                self.impedance[1][key] = impedance
            else:
                self.impedance[1] = impedance

    def set_admittance(self, admittance, cnx_type=None, key=None):
        if not self.admittance:
            self.admittance = [None, None]
        if cnx_type == 'Série':
            if key:
                self.admittance[0][key] = admittance
            else:
                self.admittance[0] = admittance
        elif cnx_type == 'Shunt':
            if key:
                self.admittance[1][key] = admittance
            else:
                self.admittance[1] = admittance


    @classmethod
    def del_instances(cls):
        cls.instances = []


class Loads(Components):
    """This class models the eletric component of eletric power systems know as load.
    """
    instances = []
    
    def get_id(self):
        return len(Loads.instances)

    def add_instance(self):
        Loads.instances.append(self)
    
    def __init__(self, terminals=None, power=None, pf=None, characteristic=None, impedance=None, admittance=None, voltage_t0=None, voltage_t1=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.id = self.get_id()
        self.name = 'Carga'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class Bars():
    """This class models the eletric element of eletric power systems know as bar.
    """
    instances = []

    @classmethod
    def get_bars(cls):
        return cls.instances

    def add_instance(self):
        Bars.instances.append(self)
    
    def __init__(self, id=None, bar_type=None, adjacents=None, isVisited=None, voltage=None, 
                active_power_in=None, reactive_power_in=None) -> None:
        """Constructor method.
        """
        self.id = id
        self.name = 'Barra'
        self.bar_type = bar_type
        self.adjacents = adjacents
        self.isVisited = isVisited
        self.voltage = voltage
        self.active_power_in = active_power_in
        self.reactive_power_in = reactive_power_in
        self.check_existance()

    def check_existance(self):
        exist = False
        for bar in Bars.instances:
            if self.id == bar.id:
                exist = True
        if not exist:
            self.add_instance()
                
    def set_id(self, id) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.id = id

    def set_bar_type(self, bar_type) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.bar_type = bar_type

    def set_adjacent(self, components) -> None:
        """This method sets a list of adjacent bars to each bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        self.adjacents = []
        for component in components:
            if self.id in component.terminals:
                if self.id != component.terminals[0]:
                    self.adjacents.append(component.terminals[0])
                else:
                     self.adjacents.append(component.terminals[1])

    def set_isVisited(self, isVisited) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.isVisited = isVisited

    def set_voltage(self, voltage, key=None) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        if key:
            self.voltage[key] = voltage
        else:
            self.voltage = voltage

    def set_active_power_in(self, active_power_in) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.active_power_in = active_power_in

    def set_reactive_power_in(self, reactive_power_in) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.reactive_power_in = reactive_power_in

    def set_voltages(self, components, bars) -> None:
        """This method works recursively in order to visit all bars and set their base voltage.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: Since this is a recursive method it returns itself ultil reaches a base case.
        :rtype: itself
        """
        aux = self 
        while(aux != None):
            aux.isVisited = True
            for adjacent in aux.adjacents:
                if adjacent != 0: # Não fazer nada para barra 0; 
                    if aux.voltage == None:
                        aux.voltage = aux.calcVoltage(components, bars)
                    if not bars[adjacent].isVisited:
                        return bars[adjacent].set_voltages(components, bars)
            # Verifying process end
            visited = [bar.isVisited for bar in bars if bar.id != 0]
            if None in visited:
                for i, visited in enumerate(visited):
                    if visited == None:
                        aux = bars[i + 1]
                        break
            else:
                break
            
    def calcVoltage(self, components, bars):
        """This method returns the calculation of the bar voltage given the first known voltage connected to the bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: A float representing the bar base voltage.
        :rtype: float.
        """
        mc = op.MagConversion()
        d = op.DefaultDictFormat()
        current_bar = self
        knownVoltageBar = current_bar.findFirstKnowVoltageBar(bars)
        knownVoltage = mc.get_value(knownVoltageBar.voltage, 'base')
        terminals = (current_bar.id, knownVoltageBar.id)
        selected_component = None
        for component in components:
            if terminals[0] in component.terminals and terminals[1] in component.terminals:
                selected_component = component
                break
        if isinstance(selected_component, Transformers):
            transformer = selected_component
            voltage_h = (mc.get_value(transformer.voltage_t0, 'nominal'), transformer.terminals[0])
            voltage_l = (mc.get_value(transformer.voltage_t1, 'nominal'), transformer.terminals[1])
            transf_relation = voltage_h[0] / voltage_l[0]
            if current_bar.id == voltage_h[1]:
                current_bar.voltage = knownVoltage * transf_relation
            else:
                current_bar.voltage = knownVoltage / transf_relation
        elif isinstance(selected_component, ShortTLines) or isinstance(selected_component, MediumTLines):
            current_bar.voltage = knownVoltage
        current_bar_voltage = mc.get_eng_notation(current_bar.voltage.real)
        current_bar.voltage = d.get_primetive_struct(sp.Voltage(current_bar_voltage[0],
                                                                current_bar_voltage[1],
                                                                'V'), 'base')
        return current_bar.voltage

    def findFirstKnowVoltageBar(self, bars):
        """This method returns the first known voltage of a adjacent bar of the current bar.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: Returns the voltage of the first adjacente bar with a known voltage.
        :rtype: float.
        """
        for adjacent in self.adjacents:
            if bars[adjacent].id != 0 and bars[adjacent].voltage:
                return bars[adjacent]

    @classmethod
    def del_instances(cls):
        cls.instances = []
