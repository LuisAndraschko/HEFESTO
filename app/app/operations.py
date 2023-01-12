import pandas as pd

######################################### Operations ################################################
class DefaultDictFormat():
    """This class is responsable for hosting the static method get_dict_struct."""
    @staticmethod
    def get_primitive_struct(value, key=None):
        """This method returns a dictionary in the following structure: {'nominal': nominal, 'base': None, 'pu': None} when just the nominal parameter is given and the folowing: {'nominal': nominal, 'base': Base, 'pu': None} when the optional parameter is given.

        :param nominal: Object to be used as value under the key 'nominal'.
        :type nominal: Object can be a instance of 1 of these 3: Voltage(), Impedance() or Power().
        :param base: When parameter nominal is an instance of Power() the base is given as the system power base, defaults to None.
        :type base: Power(), optional.
        :return: Dictionary as described in method description .
        :rtype: Dict.
        """
        keys = ['nominal', 'base', 'pu']
        struct = {s_key: None for s_key in keys}
        if key:
            struct[key] = value
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

    def get_value(self, eng_notation, key=None):
        given_mag = None
        given_mult = None
        try:
            given_mag = eng_notation[key].mag
            given_mult = eng_notation[key].multiplier
        except TypeError:
            given_mag = eng_notation.mag
            given_mult = eng_notation.multiplier
        return self.multipliers[given_mult] * given_mag
            
    def get_eng_notation(self, value):
        for multiplier, meq in self.multipliers.items():
            if value / meq >= 1 and value / meq < 1000:
                return (value / meq, multiplier)

    def get_inverse_eng_notation(self, struct, key, out_class, out_measurement_unit):
        # Invert Mag
        inverted_mag = self.get_value(struct, key) ** -1
        # Invert Multiplier
        inverted_multiplier = self.get_inverse_multiplier(struct[key].multiplier)
        return out_class(inverted_mag, inverted_multiplier, out_measurement_unit)

    def get_inverse_multiplier(self, multiplier):  
        if pd.isnull(multiplier):
            return ''
        inv_m_value = pow(self.multipliers[multiplier], -1)
        for key, value in self.multipliers.items():
            if inv_m_value == value:
                return key
