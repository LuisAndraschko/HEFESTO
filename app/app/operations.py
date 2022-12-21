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
        """Returns the corresponding float value given a dict with the key 'nominal' and object in value field with the attribute .multiplier which should correspond with this class instance attribute .multipliers.

        :param eng_notation: Received dict with object of type Voltage(), Impedance() or Power() in the format: {'nominal': object, ...}.
        :type eng_notation: Dict.
        :return: A float corresponding to the given engineering notetion.
        :rtype: float.
        """
        if key:
            if pd.isnull(eng_notation[key].multiplier):
                eng_notation[key].multiplier = ''
            return self.multipliers[eng_notation[key].multiplier] * eng_notation[key].mag
        else:
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
