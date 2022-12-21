import app.sys_primetives as sp
import app.operations as op

class Components():

    @classmethod
    def del_instances(cls):
        cls.instances = []

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
    instances = []

    def add_instance(self):
        Generators.instances.append(self)

    def get_id(self):
        return len(Generators.instances)

    def __init__(self, terminals=None, impedance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None, admittance=None) -> None:
        self.id = self.get_id()
        self.name = 'Gerador'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()
     
    @classmethod
    def del_instances(cls):
        cls.instances = []


class Transformers(Components):
    instances = []

    def get_id(self):
        return len(Transformers.instances)

    def add_instance(self):
        Transformers.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None, admittance=None) -> None:
        self.id = self.get_id()
        self.name = 'Transformador'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class ShortTLines(Components):
    instances = []
    
    def get_id(self):
        return len(ShortTLines.instances)

    def add_instance(self):
        ShortTLines.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None, admittance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None) -> None:
        self.id = self.get_id()
        self.name = 'Linha de Transmissão Pequena'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class MediumTLines(Components):
    instances = []
    
    def get_id(self):
        return len(MediumTLines.instances)

    def add_instance(self):
        MediumTLines.instances.append(self)
    
    def __init__(self, terminals=None, impedance=None, admittance=None,
                 power=None, voltage_t0=None, voltage_t1=None, pf=None, characteristic=None) -> None:
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
    instances = []
    
    def get_id(self):
        return len(Loads.instances)

    def add_instance(self):
        Loads.instances.append(self)
    
    def __init__(self, terminals=None, power=None, pf=None, characteristic=None, impedance=None, admittance=None, voltage_t0=None, voltage_t1=None) -> None:
        self.id = self.get_id()
        self.name = 'Carga'
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    @classmethod
    def del_instances(cls):
        cls.instances = []


class Bars():
    instances = []

    @classmethod
    def get_bars(cls):
        return cls.instances

    def add_instance(self):
        Bars.instances.append(self)
    
    def __init__(self, id=None, bar_type=None, adjacents=None, isVisited=None, voltage=None, 
                active_power_in=None, reactive_power_in=None) -> None:
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
        self.id = id

    def set_bar_type(self, bar_type) -> None:
        self.bar_type = bar_type

    def set_adjacent(self, components) -> None:
        self.adjacents = []
        for component in components:
            if self.id in component.terminals:
                if self.id != component.terminals[0]:
                    self.adjacents.append(component.terminals[0])
                else:
                     self.adjacents.append(component.terminals[1])

    def set_isVisited(self, isVisited) -> None:
        self.isVisited = isVisited

    def set_voltage(self, voltage, key=None) -> None:
        if key:
            self.voltage[key] = voltage
        else:
            self.voltage = voltage

    def set_active_power_in(self, active_power_in) -> None:
        self.active_power_in = active_power_in

    def set_reactive_power_in(self, reactive_power_in) -> None:
        self.reactive_power_in = reactive_power_in

    def set_voltages(self, components, bars) -> None:
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
        current_bar.voltage = d.get_primitive_struct(sp.Voltage(current_bar_voltage[0],
                                                                current_bar_voltage[1],
                                                                'V'), 'base')
        return current_bar.voltage

    def findFirstKnowVoltageBar(self, bars):
        for adjacent in self.adjacents:
            if bars[adjacent].id != 0 and bars[adjacent].voltage:
                return bars[adjacent]

    def get_bars_iter(self):
        return [i for i in range(len(Bars.instances) + 1)]

    @classmethod
    def del_instances(cls):
        cls.instances = []


class Generic():
    instances = []
    
    def get_id(self):
        return len(Generic.instances)

    def add_instance(self):
        Generic.instances.append(self)
    
    def __init__(self, type=None, terminals=None, power=None, pf=None, characteristic=None, impedance=None, admittance=None, voltage_t0=None, voltage_t1=None) -> None:
        self.id = self.get_id()
        self.type = type
        super().__init__(terminals, impedance, admittance, power, voltage_t0, voltage_t1, pf, characteristic)
        self.add_instance()

    def set_name(self, type):
        self.type = type

    @classmethod
    def del_instances(cls):
        cls.instances = []