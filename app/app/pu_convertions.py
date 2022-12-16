""" This module is responsible for getting user input and determine system pu equivalent

:return: Default return of python script.
:rtype: None
"""
from typing import List
import copy as cp
import pandas as pd
from IPython.display import display
import pandas as pd
from IPython.display import display


class DefaultDictFormat():
    """This class is responsable for hosting the static method get_dict_struct."""
    @staticmethod
    def get_dict_struct(nominal, base=None):
        """This method returns a dictionary in the following structure: {'nominal': nominal, 'base': None, 'pu': None} when just the nominal parameter is given and the folowing: {'nominal': nominal, 'base': Base, 'pu': None} when the optional parameter is given.

        :param nominal: Object to be used as value under the key 'nominal'.
        :type nominal: Object can be a instance of 1 of these 3: Voltage(), Impedance() or Power().
        :param base: When parameter nominal is an instance of Power() the base is given as the system power base, defaults to None.
        :type base: Power(), optional.
        :return: Dictionary as described in method description .
        :rtype: Dict.
        """
        keys = ['nominal', 'base', 'pu']
        struct = {key: None for key in keys}
        struct['nominal'] = nominal
        if base is not None:
            struct['base'] = base
        return struct


class MagConversion():
    """This class is responsable for converting to and from engineering notation with the methods: get_value() and get_eng_notation().
    """
    def __init__(self) -> None:
        """Constructor method. Atributtes predetermined dictionary to instance variable multipliers.
        """
        self.multipliers = {
            'p': pow(10, -12),
            'n': pow(10, -9),
            'u': pow(10, -6),
            'm': pow(10, -3),
            '': pow(10, 0),
            'k': pow(10, 3),
            'M': pow(10, 6),
            'G': pow(10, 9),
            'T': pow(10, 12),
            '%': pow(10, -2),
            '1/%': pow(10, 2)
        }


    def get_value(self, eng_notation):
        """Returns the corresponding float value given a dict with the key 'nominal' and object in value field with the attribute .multiplier which should correspond with this class instance attribute .multipliers.

        :param eng_notation: Received dict with object of type Voltage(), Impedance() or Power() in the format: {'nominal': object, ...}.
        :type eng_notation: Dict.
        :return: A float corresponding to the given engineering notetion.
        :rtype: float.
        """       
        if isinstance(eng_notation, dict):
            if pd.isnull(eng_notation['nominal'].multiplier):
                eng_notation['nominal'].multiplier = ''
            return self.multipliers[eng_notation['nominal'].multiplier] * eng_notation['nominal'].mag
        else:
            if pd.isnull(eng_notation.multiplier):
                eng_notation.multiplier = ''
            return self.multipliers[eng_notation.multiplier] * eng_notation.mag

    def get_eng_notation(self, value):
        """Returns the engineering notation of a given value in the form of a tuple where the 1st element is the string representing the multiplier in the notation and the 2nd element the value associated with the multiplier.

        :param value: A float or int to be converted to engineering notation.
        :type value: float, int.
        :return: A tuple containg like (multiplier, value).
        :rtype: (str, float).
        """
        for multiplier, meq in self.multipliers.items():
            if value / meq >= 1 and value / meq < 1000:
                return (multiplier, value / meq)

    def get_inverse_multiplier(self, multiplier):  
        if pd.isnull(multiplier):
            return ''
        inv_m_value = pow(self.multipliers[multiplier], -1)
        for key, value in self.multipliers.items():
            if inv_m_value == value:
                return key


class Number():
    """This class purpose is to be inherited by other classes.
    """
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Generator method.

        :param mag: Magnitude of a number in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: String representing the unit of the measurement i.e 'V' for 'volts', 'W' for active power, etc.
        :type measurement_unit: str.
        """
        self.mag = mag
        self.multiplier = multiplier
        self.measurement_unit = measurement_unit
    
    def __str__(self):
        formatted = f'{PrepareForTemplate().get_rounded_string(self.mag)} {self.multiplier}{self.measurement_unit}'
        return formatted
        

class Power(Number):
    """This class represents the eletric characteristic know as power.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """

    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        self.name = 'Potência'
        super().__init__(mag, multiplier, measurement_unit)


class Voltage(Number):
    """This class represents the eletric characteristic know as voltage.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit, bar) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameter bar.

        :param mag: Magnitude of voltage in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A voltage is measured in volts which is specified in this parameter.
        :type measurement_unit: str.
        :param bar: Since voltage is measured in a bar this parameter was added. A bar is identified by it's number.
        :type bar: int.
        """
        self.name = 'Tensão'
        super().__init__(mag, multiplier, measurement_unit)
        self.bar = bar


class Impedance(Number):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit, characteristic, lenght=None) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameteres characteristic and length (optional).

        :param mag: Magnitude of impedance in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A impedance can be measured in 'ohm', 'ohm/km', 'kohm*km' or '%'. Which one is specified in this parameter.
        :type measurement_unit: str.
        :param characteristic: A impedance can be in series or shunt, which one is specified in this parameter.
        :type characteristic: str.
        :param lenght: When a impedance measurement unit is given in 'ohm/km' or 'kohm*km' a length is needed in order to get the concentraded parameter, defaults to None.
        :type lenght: float or int, optional.
        """
        self.name = 'Impedância'
        super().__init__(mag, multiplier, measurement_unit)
        self.characteristic = characteristic
        self.len = lenght
        self.check_format()

    def check_format(self):
        """This method checks if the Impedance was specified as a distributed parameter, if It has this method converts to a concentrated parameter aproprieate for calculations.
        """
        if self.measurement_unit == 'ohm/km':
            self.mag *= self.len
            self.measurement_unit = 'ohm'
        elif self.measurement_unit == 'kohm*km':
            if self.mag.imag > 0:
                self.mag = -self.mag * 1000 / self.len
            else:
                self.mag = self.mag * 1000 / self.len
            self.measurement_unit = 'ohm'


class Admittance(Number):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameteres characteristic and length (optional).

        :param mag: Magnitude of impedance in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A impedance can be measured in 'ohm', 'ohm/km', 'kohm*km' or '%'. Which one is specified in this parameter.
        :type measurement_unit: str.
        """
        self.name = 'Admitância'
        super().__init__(mag, multiplier, measurement_unit)


class Generators():
    """This class models the eletric component of eletric power systems know as generator.
    """
    instances = []

    def __init__(self, series_impedance, terminals, power=None, voltage=None) -> None:
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
        self.name = 'Gerador'
        Generators.instances.append(self)
        self.id = len(Generators.instances)
        self.power = power
        self.voltage = voltage
        self.series_impedance = series_impedance
        self.terminals = terminals
        self.series_admittance = None
        self.autoset_series_admittance()
    
    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power

    def set_voltage(self, key, voltage):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage[key] = voltage

    def set_series_impedance(self, key, impedance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = impedance
    
    def set_series_admittance(self, key, admittance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_admittance[key] = admittance

    def autoset_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)
        
    @classmethod
    def del_instances(cls):
        cls.instances = []


class Transformers():
    """This class models the eletric component of eletric power systems know as transformer.
    """
    instances = []

    def __init__(self, impedance, terminals, power=None, voltage_h=None, voltage_l=None) -> None:
        """Constructor method.

        :param impedance: A transformer is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A transformer has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A transformer has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage_h: A transformer has a high voltage side, when is of interest this parameter specifies that voltage value, defaults to None.
        :type voltage_h: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        :param voltage_l: A transformer has a low voltage side, when is of interest this parameter specifies that voltage value, defaults to None.
        :type voltage_l: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.name = 'Transformador'
        Transformers.instances.append(self)
        self.id = len(Transformers.instances)
        self.power = power
        self.voltage_h = voltage_h
        self.voltage_l = voltage_l
        self.series_impedance = impedance
        self.terminals = terminals
        self.series_admittance = None
        self.autoset_series_admittance()
    
    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power

    def set_voltage_h(self, key, voltage_h):
        """This method sets the voltage of the transformer. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage_h[key] = voltage_h
    
    def set_voltage_l(self, key, voltage_l):
        """This method sets the voltage of the transformer. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage_l[key] = voltage_l

    def set_series_impedance(self, key, impedance):
        """This method sets the impedance of the transformer. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = impedance
    
    def set_series_admittance(self, key, admittance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_admittance[key] = admittance

    def autoset_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)

    @classmethod
    def del_instances(cls):
        cls.instances = []


class ShortTLines():
    """This class models the eletric component of eletric power systems know as short transmission line.
    """
    instances = []

    def __init__(self, series_impedance, terminals) -> None:
        """Constructor method.

        :param series_impedance: A short transmission line is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type series_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals:  A short transmission line has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        """
        self.name = 'Linha de Transmissão Pequena'
        ShortTLines.instances.append(self)
        self.id = len(ShortTLines.instances)
        self.series_impedance = series_impedance
        self.terminals = terminals
        self.series_admittance = None
        self.autoset_series_admittance()
    
    def set_series_impedance(self, key, series_impedance):
        """This method sets the series impedance of the short transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = series_impedance
    
    def set_series_admittance(self, key, series_admittance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_admittance[key] = series_admittance

    def autoset_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)

    @classmethod
    def del_instances(cls):
        cls.instances = []


class MediumTLines():
    """This class models the eletric component of eletric power systems know as medium transmission line.
    """
    instances = []

    def __init__(self, series_impedance, shunt_impedance, terminals) -> None:
        """Constructor method.

        :param series_impedance: A medium transmission line is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type series_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param shunt_impedance: A medium transmission line is modeled as having a shunt impedance. This parameter specifies the impedance chacteristics.
        :type shunt_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals:  A medium transmission line has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        """
        self.name = 'Linha de Transmissão Média'
        MediumTLines.instances.append(self)
        self.id = len(MediumTLines.instances)
        self.series_impedance = series_impedance
        self.shunt_impedance = shunt_impedance
        self.shunt_impedance_per_side = cp.deepcopy(shunt_impedance)
        self.terminals = terminals
        self.correct_shunt_impedance_per_side()
        self.series_admittance = None
        self.autoset_series_admittance()
        self.shunt_admittance = None
        self.autoset_shunt_admittance()
        self.shunt_admittance_per_side = None
        self.autoset_shunt_admittance_per_side()
    
    def set_series_impedance(self, key, impedance):
        """This method sets the series impedance of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = impedance
    
    def set_shunt_impedance(self, key, shunt_impedance):
        """This method sets the shunt impedance of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_impedance[key] = shunt_impedance
    
    def set_shunt_impedance_per_side(self, key, shunt_impedance_per_side):
        """This method sets the shunt impedance per side of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_impedance_per_side[key] = shunt_impedance_per_side

    def correct_shunt_impedance_per_side(self):
        """This method corrects the value of shunt impedance per side.
        """
        self.shunt_impedance_per_side['nominal'].mag = 2 * self.shunt_impedance['nominal'].mag
        self.shunt_impedance_per_side['nominal'].characteristic = 'Shunt/lado'

    def set_series_admittance(self, key, series_admittance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_admittance[key] = series_admittance

    def autoset_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)
    
    def set_shunt_admittance(self, key, shunt_admittance):
        """This method sets the shunt impedance of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_admittance[key] = shunt_admittance

    def autoset_shunt_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.shunt_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.shunt_admittance['nominal'].mag = pow(self.shunt_impedance['nominal'].mag, -1)
        self.shunt_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.shunt_impedance['nominal'].multiplier)

    def set_shunt_admittance_per_side(self, key, shunt_admittance_per_side):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_admittance_per_side[key] = shunt_admittance_per_side

    def autoset_shunt_admittance_per_side(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.shunt_admittance_per_side = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.shunt_admittance_per_side['nominal'].mag = pow(self.shunt_impedance_per_side['nominal'].mag, -1)
        self.shunt_admittance_per_side['nominal'].multiplier = mc.get_inverse_multiplier(self.shunt_impedance_per_side['nominal'].multiplier)

    @classmethod
    def del_instances(cls):
        cls.instances = []


class PowerFactor():
    """This class models the eletric characteristic of eletric power know as power factor.
    """
    def __init__(self, pf, characteristic) -> None:
        """Constructor method.

        :param pf: Power factor value ranging between ]0, 1].
        :type pf: float.
        :param characteristic: _description_
        :type characteristic: _type_
        """
        self.name = 'Fator de Potência'
        self.pf = pf
        self.characteristic = characteristic
    
    def __str__(self):
        formatted = f'{self.pf} {self.characteristic}'
        return formatted


class Loads():
    """This class models the eletric component of eletric power systems know as load.
    """
    instances = []

    def __init__(self, terminals, power=None, power_factor=None, impedance = None) -> None:
        """Constructor method.

        :param terminals: A load has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A load can be specified by it's power and power factor, this parameter specifies it's power, defaults to None.
        :type power: dict {'nominal': Power(), 'base': None, 'pu': None}, optional.
        :param power_factor: A load can be specified by it's power and power factor, this parameter specifies it's power factor, defaults to None.
        :type power_factor: PowerFactor(), optional.
        :param impedance: A load can be specified by it's impedance, this parameter specifies that, defaults to None.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}, optional.
        """
        self.name = 'Carga'
        Loads.instances.append(self)
        self.id = len(Loads.instances)
        self.power = power
        self.pf = power_factor
        self.terminals = terminals
        self.correct_const_power()

    def correct_const_power(self):
        if self.power['nominal'].measurement_unit == 'VA':
            apparent_power = self.power['nominal'].mag
            active_power = apparent_power * float(self.pf.pf)
            reactive_power = ((apparent_power ** 2) - (active_power ** 2)) ** 0.5
            self.power['nominal'].mag = complex(active_power, reactive_power)
        else:
            active_power = self.power['nominal'].mag
            apparent_power = active_power / float(self.pf.pf)
            reactive_power = ((apparent_power ** 2) - (active_power ** 2)) ** 0.5
            self.power['nominal'].mag = complex(active_power, reactive_power) 

    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power

    @classmethod
    def del_instances(cls):
        cls.instances = []


class Bars():
    """This class models the eletric element of eletric power systems know as bar.
    """
    instances = []

    def __init__(self) -> None:
        """Constructor method.
        """
        self.name = 'Barra'
        Bars.instances.append(self)
        self.id = None
        self.adjacent = []
        self.isVisited = False
        self.voltage = None

    def set_id(self, id) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.id = id

    def get_bars(self, components) -> List:
        """This method returns a list to be iterated over when instatiating the bars.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :return: A list of integers from 0 up to the higher terminal.
        :rtype: List.
        """
        t_list = [terminals for component in components for terminals in component.terminals]
        max_terminal = sorted(t_list)[-1]
        bar_list = [i for i in range(max_terminal + 1)]
        return bar_list

    def set_adjacent(self, components) -> None:
        """This method sets a list of adjacent bars to each bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        for component in components:
            if self.id in component.terminals:
                if self.id != component.terminals[0]:
                    self.adjacent.append(component.terminals[0])
                else:
                     self.adjacent.append(component.terminals[1])

    def set_isVisited(self, isVisited) -> None:
        """This method sets the isVisited attribute of the caller instance to true.

        :param isVisited: This parameter is used as part of algorithm to go through all the bars.
        :type isVisited: bool
        """
        self.isVisited = isVisited
    
    def set_voltage(self, voltage) -> None:
        """This method sets the bar voltage attribute.

        :param voltage: Voltage value to be set. 
        :type voltage: float
        """
        self.voltage = MagConversion().get_value(voltage)

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
            for adjacent in aux.adjacent:
                if adjacent != 0: # Não fazer nada para barra 0; 
                    if aux.voltage == None:
                        aux.voltage = aux.calcVoltage(components, bars)
                    if not bars[adjacent].isVisited:
                        return bars[adjacent].set_voltages(components, bars)
            # Verifying process end
            visited = [bar.isVisited for bar in bars if bar.id != 0]
            if False in visited:
                for i, visited in enumerate(visited):
                    if visited == False:
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
        current_bar = self
        knowVoltageBar = current_bar.findFirstKnowVoltageBar(bars)
        terminals = (current_bar.id, knowVoltageBar.id)
        selected_component = None
        for component in components:
            if terminals[0] in component.terminals and terminals[1] in component.terminals:
                selected_component = component
                break
        if isinstance(selected_component, Transformers):
            transformer = selected_component
            voltage_h = (MagConversion().get_value(transformer.voltage_h), transformer.voltage_h['nominal'].bar)
            voltage_l = (MagConversion().get_value(transformer.voltage_l), transformer.voltage_l['nominal'].bar)
            transf_relation = voltage_h[0] / voltage_l[0]
            if current_bar.id == voltage_h[1]:
                current_bar.voltage = knowVoltageBar.voltage * transf_relation
            else:
                current_bar.voltage = knowVoltageBar.voltage / transf_relation
        elif isinstance(selected_component, ShortTLines) or isinstance(selected_component, MediumTLines):
            current_bar.voltage = knowVoltageBar.voltage
        return current_bar.voltage

    def findFirstKnowVoltageBar(self, bars):
        """This method returns the first known voltage of a adjacent bar of the current bar.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: Returns the voltage of the first adjacente bar with a known voltage.
        :rtype: float.
        """
        for adjacent in self.adjacent:
            if bars[adjacent].id != 0 and bars[adjacent].voltage != None:
                return bars[adjacent]

    @classmethod
    def del_instances(cls):
        cls.instances = []


class PuConvesions():
    """This class is responsable for converting all power system inputed components to pu.
    """
    instances = []

    def __init__(self, sys_power, sys_voltage) -> None:
        """Constructor method.

        :param base_power: The inputed power base of the system in float format.
        :type base_power: float.
        """
        self.name = 'Classe Conversão PU'
        PuConvesions.instances.append(self)
        self.id = len(PuConvesions.instances)
        self.sys_power = sys_power
        self.sys_voltage = sys_voltage

    def generator_to_pu(self, bars, components):
        """This method converts the generator nominal voltage and impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        generators = [component for component in components if isinstance(component, Generators)]
        mc = MagConversion()
        for gen in generators: 
            base_p = mc.get_value(self.sys_power)
            gen_npower = mc.get_value(gen.power)
            for bar in bars:
                if bar.id == gen.terminals[1] and bar.id != 0:
                    # Converting power to pu
                    gen.set_power('base', base_p)
                    gen.set_power('pu', Power(complex(gen_npower / base_p), '', 'pu'))
                    # Converting voltage to pu
                    gen_nvoltage = mc.get_value(gen.voltage['nominal'])
                    gen.set_voltage('base', bar.voltage)
                    gen.set_voltage('pu', Voltage(complex(gen_nvoltage / bar.voltage), '', 'pu', gen.terminals[1]))
                    # Converting impedance to pu
                    gen_nimpedance = mc.get_value(gen.series_impedance['nominal'])
                    gen.set_series_impedance('base', pow(gen_nvoltage, 2) / gen_npower)
                    impedance = complex(gen_nimpedance * gen.series_impedance['base'] * (base_p / pow(bar.voltage, 2)))
                    gen.set_series_impedance('pu', Impedance(impedance, '', 'pu', 'Série'))
                    # Setting Admittance
                    gen.set_series_admittance('base', gen_npower / pow(gen_nvoltage, 2))
                    admittance = complex(pow(bar.voltage, 2) / (gen_nimpedance * gen.series_impedance['base'] * base_p))
                    gen.set_series_admittance('pu', Admittance(admittance, '', 'pu'))          

    def transformer_to_pu(self, bars, components):
        """This method converts the transformer nominal impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        transformers = [component for component in components if isinstance(component, Transformers)]
        mc = MagConversion()
        for tran in transformers: 
            # Getting power values
            base_p = mc.get_value(self.sys_power)
            tran_npower = mc.get_value(tran.power)
            # Converting power to pu
            tran.set_power('base', base_p)
            tran.set_power('pu', Power(complex(tran_npower / base_p), '', 'pu'))
            # Getting transformer nominal values
            tran_nhv = mc.get_value(tran.voltage_h['nominal'])
            tran_nlv = mc.get_value(tran.voltage_l['nominal'])  
            tran_nz = mc.get_value(tran.series_impedance['nominal'])  
            # Setting high and low voltage bars
            bar_h = tran.voltage_h['nominal'].bar
            bar_l = tran.voltage_l['nominal'].bar
            # Setting high and low voltages basys
            h_voltage_base = bars[bar_h].voltage
            l_voltage_base = bars[bar_l].voltage
            for bar in bars:
                # Match current trasformer terminal with bar
                if bar.id in tran.terminals:
                    # Converting voltage high to pu
                    tran.set_voltage_h('base', h_voltage_base)
                    tran.set_voltage_h('pu', Voltage(complex(tran_nhv / h_voltage_base), '', 'pu', tran.terminals[0]))
                    # Converting voltage low to pu
                    tran.set_voltage_l('base', l_voltage_base)
                    tran.set_voltage_l('pu', Voltage(complex(tran_nlv / l_voltage_base), '', 'pu', tran.terminals[1]))
                    # Converting impedance to pu
                    tran.set_series_impedance('base', pow(tran_nhv, 2) / tran_npower)
                    impedance = complex(tran_nz * tran.series_impedance['base'] * (base_p / pow(h_voltage_base, 2)))
                    tran.set_series_impedance('pu', Impedance(impedance, '', 'pu', 'Série'))
                    # Setting Admittance
                    tran.set_series_admittance('base', tran_npower / pow(tran_nhv, 2))
                    admittance = complex(pow(h_voltage_base, 2) / (tran_nz * tran.series_impedance['base'] * base_p))
                    tran.set_series_admittance('pu', Admittance(admittance, '', 'pu'))         
            
    def tlines_to_pu(self, bars, components):
        """This method converts the transmission lines nominal impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        tlines = [component for component in components if isinstance(component, ShortTLines) or isinstance(component, MediumTLines)]
        mc = MagConversion()
        # Getting power base values
        base_p = mc.get_value(self.sys_power)
        
        for line in tlines:
            for bar in bars:
                # Match current bar with transmission line in question
                if bar.id in line.terminals and not line.series_impedance['base']:
                    # Getting voltage and impedance base values
                    base_v = bar.voltage
                    # Setting base impedance
                    base_z = pow(base_v, 2) / base_p
                    ######################################################################## Converting impedance to pu
                    # Get nominal series impedance value
                    line_sz = mc.get_value(line.series_impedance['nominal'])
                    # print(f'line_sz = {line_sz}', file=sys.stderr)
                    # Setting base series impedance
                    line.set_series_impedance('base', base_z)
                    # Setting pu series impedance
                    series_impedance = complex(line_sz / line.series_impedance['base'])
                    line.set_series_impedance('pu', Impedance(series_impedance, '', 'pu', 'Série'))
                    # Setting base series admittance
                    line.set_series_admittance('base', pow(base_z, -1))
                    # Setting pu series admittance
                    series_admittance = complex(line.series_impedance['base'] / line_sz)  
                    line.set_series_admittance('pu', Admittance(series_admittance, '', 'pu'))    


                    if isinstance(line, MediumTLines):
                        # Get nominal shunt and shunt per side impedance values
                        line_shz = mc.get_value(line.shunt_impedance['nominal'])
                        line_shzps = mc.get_value(line.shunt_impedance_per_side['nominal'])
                        # Set shunt and shunt per side base impedance values
                        line.set_shunt_impedance('base', base_z)
                        line.set_shunt_impedance_per_side('base', base_z)
                        # Set shunt and shunt per side base admittance values
                        line.set_shunt_admittance('base', pow(base_z, -1))
                        line.set_shunt_admittance_per_side('base', pow(base_z, -1))
                        # Set shunt and shunt per side pu impedance values
                        shunt_impedance = complex(line_shz / line.shunt_impedance['base'])  
                        line.set_shunt_impedance('pu', Impedance(shunt_impedance, '', 'pu', 'Shunt'))
                        shunt_impedance_per_side = complex(line_shzps / line.shunt_impedance_per_side['base'])  
                        line.set_shunt_impedance_per_side('pu', Impedance(shunt_impedance_per_side, '', 'pu', 'Shunt'))
                        # Set shunt and shunt per side pu admittance values
                        shunt_admittance = complex(line.shunt_impedance['base'] / line_shz)  
                        line.set_shunt_admittance('pu', Admittance(shunt_admittance, '', 'pu'))
                        shunt_admittance_per_side = complex(line.shunt_impedance_per_side['base'] / line_shzps)  
                        line.set_shunt_admittance_per_side('pu', Admittance(shunt_admittance_per_side, '', 'pu'))

    def loads_to_pu(self, bars, components):
        """This method converts the loads nominal power to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        loads = [component for component in components if isinstance(component, Loads)]
        mc = MagConversion()
        
        for load in loads:
            load_power = mc.get_value(load.power['nominal'])
            load_base_power = mc.get_value(self.sys_power)
            load.set_power('base', load_base_power)
            load.set_power('pu', Power(load_power / load_base_power, '', 'pu'))

    @classmethod
    def del_instances(cls):
        cls.instances = []


class ExcelToValues():
    def __init__(self, excel) -> None:
        self.system_basis = pd.read_excel(excel, sheet_name="Bases do Sistema")
        self.generators = pd.read_excel(excel, sheet_name="Geradores")
        self.transformers = pd.read_excel(excel, sheet_name="Transformadores")
        self.short_tlines = pd.read_excel(excel, sheet_name="LT Curtas")
        self.medium_tlines = pd.read_excel(excel, sheet_name="LT Médias")
        self.loads = pd.read_excel(excel, sheet_name="Cargas")

    def create_all(self):
        self.pu_conv_sb()
        self.pu_conv_gen()
        self.pu_conv_tran()
        self.pu_conv_short_tline()
        self.pu_conv_medium_tline()
        self.pu_conv_load()

    def get_mag_mult_measure(self, df, row_index, column_index):
        mag = str(df.iloc[row_index, column_index]).replace(",", ".")
        mult = df.iloc[row_index, column_index + 1]
        measure = df.iloc[row_index, column_index + 2]
        return (mag, mult, measure)

    def get_power_factor_values(self, df, row_index, column_index):
        mag = str(df.iloc[row_index, column_index]).replace(",", ".")
        characteristic = df.iloc[row_index, column_index + 1]
        return (mag, characteristic)

    def pu_conv_sb(self):
        df = pd.DataFrame(self.system_basis)
        # Reading Power
        i_power = df.columns.get_loc('Potência de base')
        power = self.get_mag_mult_measure(df, 0, i_power)
        # Reading Voltage
        i_voltage = df.columns.get_loc('Tensão de base')
        voltage = self.get_mag_mult_measure(df, 0, i_voltage)
        # Reading bar
        bar = df.loc[0, 'Barra']
        # Packing Values
        sb_values = {
            'power_mag': power[0], 
            'power_mult': power[1], 
            'power_measure': power[2], 
            'voltage_mag': voltage[0], 
            'voltage_mult': voltage[1], 
            'voltage_measure': voltage[2], 
            'bar': bar       
            }
        ValuesToObj.sb(sb_values)

    def pu_conv_gen(self):
        df = pd.DataFrame(self.generators)
        generators = []
        
        i_power = df.columns.get_loc('Potência')
        i_voltage = df.columns.get_loc('Tensão')
        i_impedance = df.columns.get_loc('Impedância')
        
        for index, row in df.iterrows():
            # Reading Power
            power = self.get_mag_mult_measure(df, index, i_power)
            # Reading Voltage
            voltage = self.get_mag_mult_measure(df, index, i_voltage)
            # Reading Impedance
            impedance = self.get_mag_mult_measure(df, index, i_impedance)
            # Reading bar
            bar = row['Barra']
            # Packing Values
            gen_values = {
                'power_mag': power[0], 
                'power_mult': power[1], 
                'power_measure': power[2], 
                'voltage_mag': voltage[0], 
                'voltage_mult': voltage[1], 
                'voltage_measure': voltage[2], 
                'impedance_mag': impedance[0], 
                'impedance_mult': impedance[1], 
                'impedance_measure': impedance[2], 
                'bar': bar
                }
            generators.append(gen_values)
        
        ValuesToObj.generator(generators)

    def pu_conv_tran(self):
        df = pd.DataFrame(self.transformers)
        transformers = []
        
        i_power = df.columns.get_loc('Potência')
        i_hvoltage = df.columns.get_loc('Tensão Alta')
        i_lvoltage = df.columns.get_loc('Tensão Baixa')
        i_impedance = df.columns.get_loc('Impedância')
        i_t_high = df.columns.get_loc('Terminal Alta')
        i_t_low = df.columns.get_loc('Terminal Baixa')

        for index, row in df.iterrows():
            # Reading Power
            power = self.get_mag_mult_measure(df, index, i_power)
            # Reading High Voltage
            hvoltage = self.get_mag_mult_measure(df, index, i_hvoltage)
            # Reading Low Voltage
            lvoltage = self.get_mag_mult_measure(df, index, i_lvoltage)
            # Reading Impedance
            impedance = self.get_mag_mult_measure(df, index, i_impedance)
            # Reading Terminas
            t0, t1 = row['Terminal Alta'], row['Terminal Baixa']
            # Packing Values
            gen_values = {
                'power_mag': power[0], 
                'power_mult': power[1], 
                'power_measure': power[2], 
                'high_voltage_mag': hvoltage[0], 
                'high_voltage_mult': hvoltage[1], 
                'high_voltage_measure': hvoltage[2],  
                'low_voltage_mag': lvoltage[0], 
                'low_voltage_mult': lvoltage[1], 
                'low_voltage_measure': lvoltage[2], 
                'impedance_mag': impedance[0], 
                'impedance_mult': impedance[1], 
                'impedance_measure': impedance[2], 
                't0': t0,
                't1': t1
                }
            transformers.append(gen_values)

        ValuesToObj.transformer(transformers)

    def pu_conv_short_tline(self):
        df = pd.DataFrame(self.short_tlines)
        short_tlines = []
        
        i_series_impedance = df.columns.get_loc('Impedância Série')
        
        for index, row in df.iterrows():
            # Reading Series Impedance
            series_impedance = self.get_mag_mult_measure(df, index, i_series_impedance)
            # Reading Terminals
            t0, t1 = row['Terminal 1'], row['Terminal 2']
            # Reading lenght
            lenght = row['Comprimento da LT (km)']
            # Packing Values
            short_tline_values = {
                'series_impedance_mag': series_impedance[0], 
                'series_impedance_mult': series_impedance[1], 
                'series_impedance_measure': series_impedance[2], 
                't0': t0,
                't1': t1,
                'lenght': lenght
                }
            short_tlines.append(short_tline_values)
        
        ValuesToObj.short_tline(short_tlines)

    def pu_conv_medium_tline(self):
        df = pd.DataFrame(self.medium_tlines)
        medium_tlines = []
        
        i_series_impedance = df.columns.get_loc('Impedância Série')
        i_shunt_impedance = df.columns.get_loc('Impedância Shunt')
        
        for index, row in df.iterrows():
            # Reading Series Impedance
            series_impedance = self.get_mag_mult_measure(df, index, i_series_impedance)
            # Reading Shunt Impedance
            shunt_impedance = self.get_mag_mult_measure(df, index, i_shunt_impedance)
            # Reading Terminals
            t0, t1 = row['Terminal 1'], row['Terminal 2']
            # Reading lenght
            lenght = row['Comprimento da LT (km)']
            # Packing Values
            medium_tline_values = {
                'series_impedance_mag': series_impedance[0], 
                'series_impedance_mult': series_impedance[1], 
                'series_impedance_measure': series_impedance[2],
                'shunt_impedance_mag': shunt_impedance[0], 
                'shunt_impedance_mult': shunt_impedance[1], 
                'shunt_impedance_measure': shunt_impedance[2], 
                't0': t0,
                't1': t1,
                'lenght': lenght
                }
            medium_tlines.append(medium_tline_values)
        
        ValuesToObj.medium_tline(medium_tlines)

    def pu_conv_load(self):
        df = pd.DataFrame(self.loads)
        loads = []
        
        i_power = df.columns.get_loc('Potência')
        i_power_factor = df.columns.get_loc('Fator de Potência')
        
        for index, row in df.iterrows():
            # Reading Power
            power = self.get_mag_mult_measure(df, index, i_power)
            # Reading Power Factor
            power_factor = self.get_power_factor_values(df, index, i_power_factor)
            # Reading bar
            bar = row['Barra']
            # Packing Values
            load_values = {
                'power_mag': power[0], 
                'power_mult': power[1], 
                'power_measure': power[2], 
                'power_factor_mag': power_factor[0], 
                'power_factor_characteristic': power_factor[1], 
                'bar': bar
                }
            loads.append(load_values)
        
        ValuesToObj.load(loads)


class FormToValues():
    @staticmethod
    def sb_form_to_value(form):
        # Packing Values
        sb_values = {
        'power_mag': form.power_mag.data,
        'power_mult': form.power_mult.data,
        'power_measure': form.power_measure.data,
        'voltage_mag': form.voltage_mag.data,
        'voltage_mult': form.voltage_mult.data,
        'voltage_measure': form.voltage_measure.data,
        'bar': form.bar.data
        }
        ValuesToObj.sb(sb_values)

    @staticmethod
    def generator_form_to_value(form):
        # Packing Values
        gen_values = {
        'power_mag': form.power_mag.data,
        'power_mult': form.power_mult.data,
        'power_measure': form.power_measure.data,
        't1': form.t1.data,
        'voltage_mag': form.voltage_mag.data,
        'voltage_mult': form.voltage_mult.data,
        'voltage_measure': form.voltage_measure.data,
        'impedance_mag': form.impedance_mag.data,
        'impedance_mult': form.impedance_mult.data,
        'impedance_measure': form.impedance_measure.data
        }
        ValuesToObj.pu_conv_generator(gen_values)
        
    @staticmethod
    def transformer(form):
        # Packing Values
        tran_values = {
            'power_mag': form.power_mag.data,
            'power_mult': form.power_mult.data,
            'power_measure': form.power_measure.data,
            't0': form.t0.data,
            't1': form.t1.data,
            'high_voltage_mag': form.high_voltage_mag.data,
            'high_voltage_measure': form.high_voltage_measure.data,
            't0': form.t0.data,
            'low_voltage_mag': form.low_voltage_mag.data,
            'low_voltage_mult': form.low_voltage_mult.data,
            'low_voltage_measure': form.low_voltage_measure.data,
            't1': form.t1.data,
            'impedance_mag': form.impedance_mag.data,
            'impedance_mult': form.impedance_mult.data,
            'impedance_measure': form.impedance_measure.data
        }
        ValuesToObj.transformer(tran_values)

    @staticmethod
    def short_tline(form):
        # Packing Values
        short_tline_values = {
            't0': form.t0.data,
            't1': form.t1.data,
            'series_impedance_mag': form.series_impedance_mag.data,
            'series_impedance_mult': form.series_impedance_mult.data,
            'series_impedance_measure': form.series_impedance_measure.data,
            'lenght': form.lenght.data
        }
        ValuesToObj.short_tline(short_tline_values)

    @staticmethod
    def medium_tline(form):
        # Packing Values
        medium_tline_values = {
            't0': form.t0.data,
            't1': form.t1.data,
            'series_impedance_mag': form.series_impedance_mag.data,
            'shunt_impedance_mag': form.shunt_impedance_mag.data,
            'series_impedance_mult': form.series_impedance_mult.data,
            'series_impedance_measure': form.series_impedance_measure.data,
            'lenght': form.lenght.data,
            'shunt_impedance_mult': form.shunt_impedance_mult.data,
            'shunt_impedance_measure': form.shunt_impedance_measure.data,
            'lenght': form.lenght.data
        }
        ValuesToObj.medium_tline(medium_tline_values)

    @staticmethod
    def load(form): 
        # Packing Values
        load_values = {
            'power_mag': form.power_mag.data,
            'power_mult': form.power_mult.data,
            'power_measure': form.power_measure.data,
            't1': form.t1.data,
            'power_factor_mag': form.power_factor_mag.data,
            'power_factor_characteristic': form.power_factor_characteristic.data
        }
        ValuesToObj.load(load_values)


class ValuesToObj():
    component_list = []

    @staticmethod
    def sb(sb_values):
        d = DefaultDictFormat()
        power_sb = Power(complex(sb_values['power_mag']), sb_values['power_mult'], sb_values['power_measure'])
        voltage_sb = d.get_dict_struct(Voltage(complex(sb_values['voltage_mag']), sb_values['voltage_mult'], sb_values['voltage_measure'], sb_values['bar']))
        pu_conv = PuConvesions(power_sb, voltage_sb) 
        ValuesToObj.component_list.append(pu_conv)

    @staticmethod
    def generator(generators):
        d = DefaultDictFormat()
        for gen in generators:
            pg = d.get_dict_struct(Power(complex(gen['power_mag']), gen['power_mult'], gen['power_measure']))
            tg = (0, gen['bar'])
            vg = d.get_dict_struct(Voltage(complex(gen['voltage_mag']), gen['voltage_mult'], gen['voltage_measure'], gen['bar']))
            zg = ValuesToObj.check_impedance(gen['impedance_mag'])
            zpug = d.get_dict_struct(Impedance(zg, gen['impedance_mult'], gen['impedance_measure'], 'Série'))
            g = Generators(zpug, tg, pg, vg)
            ValuesToObj.component_list.append(g)
    
    @staticmethod
    def transformer(transformers):
        d = DefaultDictFormat()
        for tran in transformers:
            pt = d.get_dict_struct(Power(complex(tran['power_mag']), tran['power_mult'], tran['power_measure']))
            tt = (tran['t0'], tran['t1'])
            vht = d.get_dict_struct(Voltage(complex(tran['high_voltage_mag']), tran['high_voltage_mult'], tran['high_voltage_measure'], tran['t0']))
            vlt = d.get_dict_struct(Voltage(complex(tran['low_voltage_mag']), tran['low_voltage_mult'], tran['low_voltage_measure'], tran['t1']))
            zt = ValuesToObj.check_impedance(tran['impedance_mag'])
            zput = d.get_dict_struct(Impedance(zt, tran['impedance_mult'], tran['impedance_measure'], 'Série'))
            t = Transformers(zput, tt, pt, vht, vlt)
            ValuesToObj.component_list.append(t)

    @staticmethod
    def short_tline(short_tlines):
        d = DefaultDictFormat()
        for line in short_tlines:
            tstl = (line['t0'], line['t1'])
            lsz = ValuesToObj.check_impedance(line['series_impedance_mag'])
            if line['lenght']:
                zsstl = d.get_dict_struct(Impedance(lsz, line['series_impedance_mult'], line['series_impedance_measure'], 'Série', float(line['lenght'])))
            else:
                zsstl = d.get_dict_struct(Impedance(lsz, line['series_impedance_mult'], line['series_impedance_measure'], 'Série'))
            stl = ShortTLines(zsstl, tstl)
            ValuesToObj.component_list.append(stl)

    @staticmethod
    def medium_tline(medium_tlines):
        d = DefaultDictFormat()
        for line in medium_tlines:
            tmtl = (line['t0'], line['t1'])
            lsz = ValuesToObj.check_impedance(line['series_impedance_mag'])
            lshz =  ValuesToObj.check_impedance(line['shunt_impedance_mag'])
            if line['lenght']:
                zsmtl = d.get_dict_struct(Impedance(lsz, line['series_impedance_mult'], line['series_impedance_measure'], 'Série', float(line['lenght'])))
                zshmtl = d.get_dict_struct(Impedance(lshz, line['shunt_impedance_mult'], line['shunt_impedance_measure'], 'Shunt', float(line['lenght'])))
            else:
                zsmtl = d.get_dict_struct(Impedance(lsz, line['series_impedance_mult'], line['series_impedance_measure'], 'Série'))
                zshmtl = d.get_dict_struct(Impedance(lshz, line['shunt_impedance_mult'], line['shunt_impedance_measure'], 'Shunt'))
            mtl = MediumTLines(zsmtl, zshmtl, tmtl)
            ValuesToObj.component_list.append(mtl)

    @staticmethod
    def load(loads):
        d = DefaultDictFormat()
        for load in loads:
            pld = d.get_dict_struct(Power(complex(load['power_mag']), load['power_mult'], load['power_measure']))
            tld = (0, load['bar'])
            pfld = PowerFactor(load['power_factor_mag'], load['power_factor_characteristic'])
            ld = Loads(tld, pld, pfld)
            ValuesToObj.component_list.append(ld)

    @staticmethod
    def check_impedance(impedance):
        if not complex(impedance).imag:
            impedance = complex(0, float(impedance))
        else:
            impedance = complex(impedance)
        return impedance

    @staticmethod
    def get_components():
        return ValuesToObj.component_list
    
    @classmethod
    def del_component_list(cls):
        cls.component_list = []


class Validation():
    @staticmethod
    def validate_system_connections(component_list):
        continuity_check = False
        used = []
        unused = []
        for component in component_list:
            if not isinstance(component, PuConvesions):
                unused.append(component.terminals)
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


class PrepareForTemplate():            
    @staticmethod
    def get_rounded_string(complex_number):
        # Prepare (+-real + 0j) format
        if not complex_number.imag:
            complex_number_str = f'{round(complex_number.real, 4):.4f}'
        # Prepare (+-real +- imag j) format   
        elif complex_number.imag and complex_number.real:
            # Prepare real
            real = f'{round(complex_number.real, 4):.4f}'
            # Prepare +- imag j
            imag = f'{round(complex_number.imag, 4):.4f}' + 'j'
            # Prepare rounded and formatted number
            if '+' in str(complex_number):
                complex_number_str = real + '+' + imag
            else:
                complex_number_str = real + imag
        else:
            # Prepare +- imag j
            complex_number_str = f'{round(complex_number.imag, 4):.4f}' + 'j'
        return complex_number_str


class Run():
    instances = []

    def __init__(self, conv_components) -> None:
        self.conv_components = conv_components
        self.bars = None

    def prep_bars(self, components):
        # Instantiating bars
        self.bars = [Bars() for i in Bars().get_bars(components)]
        # Setting bars Id's
        for i in range(len(self.bars)): self.bars[i].set_id(i)
        # Setting adjacent bars
        for bar in self.bars: bar.set_adjacent(components)
    
    def set_base_voltages(self, conv, components):
        # Defining groung and head bar
        ground_bar = self.bars[0]
        ground_bar.set_voltage(Voltage(0, 'k', 'V', 0))
        head = self.bars[conv.sys_voltage['nominal'].bar]
        self.bars[head.id].set_voltage(conv.sys_voltage['nominal'])
        head.set_voltages(components, self.bars)

    def conv_to_pu(self):
        """The main functions execute the method calls in order to get the script output.
        """
        # try:
        # Get Pu Conversion class
        conv = self.conv_components[0]
        # Get system components only
        components = self.conv_components[1:]
        # Setting Id and adjacent bars
        self.prep_bars(components)
        # Setting system base voltages
        self.set_base_voltages(conv, components)

        # Converting system components to pu
        conv.generator_to_pu(self.bars, components)
        conv.transformer_to_pu(self.bars, components)
        conv.tlines_to_pu(self.bars, components)
        conv.loads_to_pu(self.bars, components)

        # Grouping results to return
        components.insert(0, conv)
        Run.instances = self.bars

        return components

    @classmethod
    def del_instances(cls):
        cls.instances = []


class ClearObjects():
    @classmethod
    def clear_all(cls):
        Generators.del_instances()
        Transformers.del_instances()
        ShortTLines.del_instances()
        MediumTLines.del_instances()
        Loads.del_instances()
        Bars.del_instances()
        PuConvesions.del_instances()
        ValuesToObj.del_component_list()
        Run.del_instances()