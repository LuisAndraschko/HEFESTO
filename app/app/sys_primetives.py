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
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.name = 'Potência'


class Voltage(Primitives):
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        self.name = 'Tensão'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)


class Impedance(Primitives):
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        self.name = 'Impedância'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.check_format()


class Admittance(Primitives):
    def __init__(self, mag=None, multiplier=None, measurement_unit=None, lenght=None, cnx_type=None) -> None:
        self.name = 'Admitância'
        super().__init__(mag, multiplier, measurement_unit, lenght, cnx_type)
        self.check_format()
