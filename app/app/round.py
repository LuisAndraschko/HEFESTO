####################################### Rounding numbers ############################################
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

