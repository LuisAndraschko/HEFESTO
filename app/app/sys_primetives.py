########################################### Objects #################################################
########################################## Grandezas ################################################
class Primitives():
    def __init__(self, mag, multiplier, measurement_unit, lenght, cnx_type) -> None:
        self.mag = mag
        self.multiplier = multiplier
        self.measurement_unit = measurement_unit
        self.lenght = lenght
        self.cnx_type = cnx_type

    def set_mag(self, mag):
        self.mag = mag

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

    def set_measurement_unit(self, measurement_unit):
        self.measurement_unit = measurement_unit

    def set_cnx_type(self, cnx_type):
        self.cnx_type = cnx_type

    def check_format(self):
        """This method checks if the Impedance was specified as a distributed parameter, if It has this method converts to a concentrated parameter aproprieate for calculations.
        """
        if self.measurement_unit == 'ohm/km':
            self.mag *= self.lenght
            self.measurement_unit = 'ohm'
        elif self.measurement_unit == 'kohm*km':
            if self.mag.imag > 0:
                self.mag = -self.mag * 1000 / self.lenght
            else:
                self.mag = self.mag * 1000 / self.lenght
            self.measurement_unit = 'ohm'
        

class Power(Primitives):
    """This class represents the eletric characteristic know as power.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """

    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.name = 'Potência'


class Voltage(Primitives):
    """This class represents the eletric characteristic know as voltage.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        self.name = 'Tensão'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)


class Impedance(Primitives):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        self.name = 'Impedância'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.check_format()


class Admittance(Primitives):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        self.name = 'Admitância'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.check_format()
