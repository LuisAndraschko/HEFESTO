""" This module is responsible for getting user input and determine system pu equivalent

:return: Default return of python script.
:rtype: None
"""
from typing import List
import copy as cp
import pandas as pd
from IPython.display import display
import pandas as pd
import app.operations as op
import app.sys_primetives as sp
import app.sys_components as sc


####################################### Leitura de dados ############################################
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
        ValuesToComponents.sb(sb_values)

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
        
        ValuesToComponents.generator(generators)

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

        ValuesToComponents.transformer(transformers)

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
        
        ValuesToComponents.short_tline(short_tlines)

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
        
        ValuesToComponents.medium_tline(medium_tlines)

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
        
        ValuesToComponents.load(loads)


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
        ValuesToComponents.sb(sb_values)

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
        ValuesToComponents.pu_conv_generator(gen_values)
        
    @staticmethod
    def transformer_form_to_value(form):
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
        ValuesToComponents.transformer(tran_values)

    @staticmethod
    def short_tline_form_to_value(form):
        # Packing Values
        short_tline_values = {
            't0': form.t0.data,
            't1': form.t1.data,
            'series_impedance_mag': form.series_impedance_mag.data,
            'series_impedance_mult': form.series_impedance_mult.data,
            'series_impedance_measure': form.series_impedance_measure.data,
            'lenght': form.lenght.data
        }
        ValuesToComponents.short_tlin_form_to_value(short_tline_values)

    @staticmethod
    def medium_tline_form_to_value(form):
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
        ValuesToComponents.medium_tline(medium_tline_values)

    @staticmethod
    def load_form_to_value(form): 
        # Packing Values
        load_values = {
            'power_mag': form.power_mag.data,
            'power_mult': form.power_mult.data,
            'power_measure': form.power_measure.data,
            't1': form.t1.data,
            'power_factor_mag': form.power_factor_mag.data,
            'power_factor_characteristic': form.power_factor_characteristic.data
        }
        ValuesToComponents.load(load_values)


####################################### Obj Instantiation ###########################################
class ValuesToComponents():
    component_list = []

    @staticmethod
    def bar(terminals):
        for bar in terminals:
            sc.Bars(bar)

    @staticmethod
    def sb(sb_values):
        d = op.DefaultDictFormat()
        power_sb = d.get_primitive_struct(sp.Power(complex(sb_values['power_mag']), sb_values['power_mult'], sb_values['power_measure']), 'base')
        voltage_sb = d.get_primitive_struct(sp.Voltage(complex(sb_values['voltage_mag']), sb_values['voltage_mult'], sb_values['voltage_measure']), 'base')
        bar_sb = sb_values['bar']
        pu_conv = PuConvesions(power_sb, voltage_sb, bar_sb) 
        ValuesToComponents.bar((0, bar_sb))
        ValuesToComponents.component_list.append(pu_conv)

    @staticmethod
    def generator(generators):
        d = op.DefaultDictFormat()
        for gen in generators:
            tg = (0, gen['bar'])
            pg = d.get_primitive_struct(sp.Power(complex(gen['power_mag']), gen['power_mult'], gen['power_measure']), 'nominal')
            vg = d.get_primitive_struct(sp.Voltage(complex(gen['voltage_mag']), gen['voltage_mult'], gen['voltage_measure']), 'nominal')
            zpug = d.get_primitive_struct(sp.Impedance(complex(gen['impedance_mag']), gen['impedance_mult'], gen['impedance_measure'], 'Série'), 'nominal')
            g = sc.Generators(tg, zpug, pg, vg)
            ValuesToComponents.bar(tg)
            ValuesToComponents.component_list.append(g)

    @staticmethod
    def transformer(transformers):
        d = op.DefaultDictFormat()
        for tran in transformers:
            tt = (tran['t0'], tran['t1'])
            zput = d.get_primitive_struct(sp.Impedance(complex(tran['impedance_mag']), tran['impedance_mult'], tran['impedance_measure'], 'Série'), 'nominal')
            pt = d.get_primitive_struct(sp.Power(complex(tran['power_mag']), tran['power_mult'], tran['power_measure']), 'nominal')
            vht = d.get_primitive_struct(sp.Voltage(complex(tran['high_voltage_mag']), tran['high_voltage_mult'], tran['high_voltage_measure']), 'nominal')
            vlt = d.get_primitive_struct(sp.Voltage(complex(tran['low_voltage_mag']), tran['low_voltage_mult'], tran['low_voltage_measure']), 'nominal')
            t = sc.Transformers(tt, zput, pt, vht, vlt)
            ValuesToComponents.bar(tt)
            ValuesToComponents.component_list.append(t)

    @staticmethod
    def short_tline(short_tlines):
        d = op.DefaultDictFormat()
        for line in short_tlines:
            tstl = (line['t0'], line['t1'])
            zsstl = d.get_primitive_struct(sp.Impedance(complex(line['series_impedance_mag']), 
                                                line['series_impedance_mult'], 
                                                line['series_impedance_measure'], 
                                                float(line['lenght']), 
                                                'Série'), 'nominal')
            stl = sc.ShortTLines(tstl, zsstl)
            ValuesToComponents.bar(tstl)
            ValuesToComponents.component_list.append(stl)

    @staticmethod
    def medium_tline(medium_tlines):
        d = op.DefaultDictFormat()
        for line in medium_tlines:
            tmtl = (line['t0'], line['t1'])
            zsmtl = d.get_primitive_struct(sp.Impedance(complex(line['series_impedance_mag']), 
                                                line['series_impedance_mult'], 
                                                line['series_impedance_measure'], 
                                                float(line['lenght']), 
                                                'Série'), 'nominal')
            zshmtl = d.get_primitive_struct(sp.Impedance(complex(line['shunt_impedance_mag']), 
                                                line['shunt_impedance_mult'], 
                                                line['shunt_impedance_measure'], 
                                                float(line['lenght']), 
                                                'Shunt'), 'nominal')
            mtl = sc.MediumTLines(tmtl, [zsmtl, zshmtl])
            ValuesToComponents.bar(tmtl)
            ValuesToComponents.component_list.append(mtl)

    @staticmethod
    def load(loads):
        d = op.DefaultDictFormat()
        for load in loads:
            tld = (0, load['bar'])
            pld = d.get_primitive_struct(sp.Power(complex(load['power_mag']), load['power_mult'], load['power_measure']), 'nominal')
            pf = load['power_factor_mag']
            pf_char = load['power_factor_characteristic']
            ld = sc.Loads(tld, pld, pf, pf_char)
            ValuesToComponents.bar(tld)
            ValuesToComponents.component_list.append(ld)

    @staticmethod
    def get_components():
        return ValuesToComponents.component_list
    
    @classmethod
    def del_component_list(cls):
        cls.component_list = []


####################################### Pu Calculations #############################################
class PuConvesions():
    instances = []

    def __init__(self, sys_power, sys_voltage, bar) -> None:
        """Constructor method.

        :param base_power: The inputed power base of the system in float format.
        :type base_power: float.
        """
        self.name = 'Classe Conversão PU'
        PuConvesions.instances.append(self)
        self.id = len(PuConvesions.instances)
        self.power = sys_power
        self.voltage = sys_voltage
        self.bar = bar

    def generator_to_pu(self, bars, components):
        """This method converts the generator nominal voltage and impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        generators = [component for component in components if isinstance(component, sc.Generators)]
        mc = op.MagConversion()
        d = op.DefaultDictFormat()
        for gen in generators: 
            # Get Generator nominal values and system power base
            system_bs = mc.get_value(self.power, 'base')
            gen_ns_value = mc.get_value(gen.power, 'nominal')
            gen_nv_value = mc.get_value(gen.voltage_t0, 'nominal')
            gen_nz_value = mc.get_value(gen.impedance, 'nominal')
            for bar in bars:
                if bar.id == gen.terminals[1] and bar.id != 0:
                    # Get match Bar Voltage Value
                    bar_voltage_value = mc.get_value(bar.voltage, 'base')
                    # Creating power struct and converting power to pu
                    gen_sb = sp.Power(complex(system_bs), '', 'VA')
                    gen_spu = sp.Power(complex(gen_ns_value / system_bs), '', 'pu')
                    # Setting base and pu power in Generator
                    gen.set_power(gen_sb, 'base')
                    gen.set_power(gen_spu, 'pu')
                    # Creating voltage struct and converting voltage to pu
                    gen_vb = sp.Voltage(complex(bar_voltage_value), '', 'V')
                    gen_vpu = sp.Voltage(complex(gen_nv_value / bar_voltage_value), '', 'pu')
                    # Setting base and pu voltage in Generator
                    gen.set_voltage_t0(gen_vb, 'base')
                    gen.set_voltage_t0(gen_vpu, 'pu')
                    # Calculating Generator base impedance
                    gen_zb_value = complex(0, (bar_voltage_value ** 2) / system_bs)
                    gen_zb = sp.Impedance(gen_zb_value, '', 'ohm', cnx_type='Série')
                    # Setting Generator base impedance
                    gen.set_impedance(gen_zb, 'base')
                    # Calculating Generator pu impedance
                    gen_puz_value = complex(0, gen_nz_value * pow(gen_nv_value / bar_voltage_value, 2) * (system_bs / gen_ns_value))
                    gen_zpu = sp.Impedance(gen_puz_value, '', 'pu', cnx_type='Série')
                    # Setting Generator Pu Impedance
                    gen.set_impedance(gen_zpu, 'pu')
                    #### Converting nominal impedance to nominal admittance
                    # Invert nominal impedance and atributte it to nominal admittance
                    gen_yn = mc.get_inverse_eng_notation(gen.impedance, 'nominal', sp.Admittance, 'Siemens')
                    gen_yn.set_cnx_type(cnx_type='Série')
                    gen_yn = d.get_primitive_struct(gen_yn, 'nominal')
                    gen.set_admittance(gen_yn)
                    #### Setting base and pu admittance in Generator
                    # Invert base and pu impedance and atributte it to base and pu admittance, respectively
                    gen_yb = mc.get_inverse_eng_notation(gen.impedance, 'base', sp.Admittance, 'Siemens')
                    gen_ypu = mc.get_inverse_eng_notation(gen.impedance, 'pu', sp.Admittance, 'pu')
                    # Setting base and pu admittance in Generator
                    gen.set_admittance(gen_yb, 'base')
                    gen.set_admittance(gen_ypu, 'pu')       

    def transformer_to_pu(self, bars, components):
        """This method converts the transformer nominal impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        transformers = [component for component in components if isinstance(component, sc.Transformers)]
        mc = op.MagConversion()
        d = op.DefaultDictFormat()
        for tran in transformers: 
            # Get Transformer nominal values and system power base
            system_bs = mc.get_value(self.power, 'base')
            tran_npower_value = mc.get_value(tran.power, 'nominal')
            tran_nhv_value = mc.get_value(tran.voltage_t0, 'nominal')
            tran_nlv_value = mc.get_value(tran.voltage_t1, 'nominal')
            tran_nz_value = mc.get_value(tran.impedance, 'nominal')
            # Creating power struct and converting power to pu
            tran_sb = sp.Power(complex(system_bs), '', 'VA')
            tran_spu = sp.Power(complex(tran_npower_value / system_bs), '', 'pu')
            # Setting base and pu power in Transformer
            tran.set_power(tran_sb, 'base')
            tran.set_power(tran_spu, 'pu')
            for bar in bars:
                if bar.id in tran.terminals:
                    # Getting base voltages from matching bars
                    if bar.id == tran.terminals[0]:
                        h_voltage = bar.voltage['base']
                        h_voltage_base_value = mc.get_value(bar.voltage, 'base')
                        l_voltage = bars[tran.terminals[1]].voltage
                        l_voltage_base_value = mc.get_value(bars[tran.terminals[1]].voltage, 'base')
                    elif bar.id == tran.terminals[1]:
                        h_voltage = bars[tran.terminals[0]].voltage
                        h_voltage_base_value = mc.get_value(bars[tran.terminals[0]].voltage, 'base')
                        l_voltage = bar.voltage['base']
                        l_voltage_base_value = mc.get_value(bar.voltage, 'base')
                    # Setting Transformer base voltages
                    tran.set_voltage_t0(h_voltage, 'base')
                    tran.set_voltage_t1(l_voltage, 'base')
                    #### Handling Transformer Pu Voltages
                    # Calculating pu voltages
                    tran_puhv_value = complex(tran_nhv_value / h_voltage_base_value)
                    tran_pulv_value = complex(tran_nlv_value / l_voltage_base_value)
                    tran_puhv = sp.Voltage(tran_puhv_value, '', 'pu')
                    tran_pulv = sp.Voltage(tran_pulv_value, '', 'pu')
                    # Setting pu voltages
                    tran.set_voltage_t0(tran_puhv, 'pu')
                    tran.set_voltage_t1(tran_pulv, 'pu')
                    #### Handling Transformer base impedance
                    # Calculating base impedance ref high
                    tran_bzh_value = (h_voltage_base_value ** 2) / system_bs
                    tran_bzh = sp.Impedance(tran_bzh_value, '', 'ohm')
                    # Setting base impedance
                    tran.set_impedance(tran_bzh, 'base')
                    #### Handling Transformer pu impedance
                    # Calculating impedance for base change calcutations
                    tran_calc_zh = (tran_nhv_value ** 2) / tran_npower_value
                    # Calculating pu impedance value
                    tran_puz_value = complex(0, tran_nz_value * (tran_calc_zh / tran_bzh_value))
                    # Setting pu impedance
                    tran_puz = sp.Impedance(tran_puz_value, '', 'pu', cnx_type='Série')
                    tran.set_impedance(tran_puz, 'pu')
                    #### Handling Transformer nominal admittance
                    ## Converting nominal impedance to nominal admittance
                    # Invert nominal impedance and atributte it to nominal admittance
                    tran_ny = mc.get_inverse_eng_notation(tran.impedance, 'nominal', sp.Admittance, 'Siemens')
                    # Setting nominal admittance
                    tran_ny.set_cnx_type(cnx_type='Série')
                    tran_ny = d.get_primitive_struct(tran_ny, 'nominal')
                    tran.set_admittance(tran_ny)
                    #### Handling Transformer base admittance
                    # Getting base admittance
                    tran_by = mc.get_inverse_eng_notation(tran.impedance, 'base', sp.Admittance, 'Siemens')
                    tran_by.set_cnx_type(cnx_type='Série')
                    # Setting base admittance
                    tran.set_admittance(tran_by, 'base')
                    #### Handling Transformer pu admittance
                    # Getting pu admittance
                    tran_puy = mc.get_inverse_eng_notation(tran.impedance, 'pu', sp.Admittance, 'pu')
                    tran_puy.set_cnx_type(cnx_type='Série')
                    # Setting pu admittance
                    tran.set_admittance(tran_puy, 'pu')

    def tlines_to_pu(self, bars, components):
        tlines = [component for component in components if isinstance(component, sc.ShortTLines) or isinstance(component, sc.MediumTLines)]
        mc = op.MagConversion()
        d = op.DefaultDictFormat()
        # Getting system power base value
        system_bs_value = mc.get_value(self.power, 'base')
        for line in tlines:
            for bar in bars:
                # Match current bar with transmission line
                if bar.id in line.terminals:
                    #### Handling Line base impedance
                    # Get Line base voltage
                    line_bv_value = mc.get_value(bar.voltage, 'base')
                    # Calculating Line base impedance
                    line_bz_value = pow(line_bv_value, 2) / system_bs_value
                    line_bz = sp.Impedance(line_bz_value, '', 'Siemens')
                    # Identify line type
                    if line.name == 'Linha de Transmissão Pequena':
                        # Set Line base impedance
                        line.set_impedance(line_bz, 'base')
                        # Getting line series nominal impedance
                        line_nsz_value = mc.get_value(line.impedance, 'nominal')
                        #### Handling Line pu impedance
                        # Calculating pu impedance
                        line_puz_value = line_nsz_value / line_bz_value
                        # Setting pu impedance
                        line_puz = sp.Impedance(line_puz_value, '', 'pu', cnx_type='Série')
                        line.set_impedance(line_puz, 'pu')
                        #### Handling Line Admittance
                        # Get Line nominal Admittance
                        line_ny = mc.get_inverse_eng_notation(line.impedance, 'nominal', sp.Admittance, 'Siemens')
                        line_ny_struct = d.get_primitive_struct(line_ny, 'nominal')
                        # Set Line nominal Admittance
                        line.set_admittance(line_ny_struct)
                        # Get Line base Admittance
                        line_by = mc.get_inverse_eng_notation(line.impedance, 'base', sp.Admittance, 'Siemens')
                        # Set Line base Admittance
                        line.set_admittance(line_by, 'base')
                        # Get Line pu Admittance
                        line_puy = mc.get_inverse_eng_notation(line.impedance, 'pu', sp.Admittance, 'pu')
                        # Set Line pu Admittance
                        line.set_admittance(line_puy, 'pu')
                    else: 
                        # Set Line base impedances
                        line.set_impedance(line_bz, 'Série', 'base')
                        line.set_impedance(line_bz, 'Shunt', 'base')
                        # Getting line series and shunt nominal impedances
                        line_nsz_value = mc.get_value(line.impedance[0], 'nominal')
                        line_nshz_value = mc.get_value(line.impedance[1], 'nominal')
                        #### Handling Line pu impedance
                        # Calculating line series and shunt pu impedances
                        line_pusz_value = line_nsz_value / line_bz_value
                        line_pushz_value = (2 * line_nshz_value) / line_bz_value
                        # Setting line series and shunt pu impedances
                        line_pusz = sp.Impedance(line_pusz_value, '', 'pu', cnx_type='Série')
                        line_pushz = sp.Impedance(line_pushz_value, '', 'pu', cnx_type='Shunt')
                        line.set_impedance(line_pusz, 'Série', 'pu')
                        line.set_impedance(line_pushz, 'Shunt', 'pu')
                        #### Handling Line Admittance
                        # Get Line nominal Admittances
                        line_nsy = mc.get_inverse_eng_notation(line.impedance[0], 'nominal', sp.Admittance, 'Siemens')
                        line_nshy = mc.get_inverse_eng_notation(line.impedance[1], 'nominal', sp.Admittance, 'Siemens')
                        line_nsy_struct = d.get_primitive_struct(line_nsy, 'nominal')
                        line_nshy_struct = d.get_primitive_struct(line_nshy, 'nominal')
                        # Set Line nominal Admittances
                        line.set_admittance(line_nsy_struct, 'Série')
                        line.set_admittance(line_nshy_struct, 'Shunt')
                        # Get Line base Admittance
                        line_by = mc.get_inverse_eng_notation(line.impedance[0], 'base', sp.Admittance, 'Siemens')
                        # Set Line base Admittances
                        line.set_admittance(line_by, 'Série', 'base')
                        line.set_admittance(line_by, 'Shunt', 'base')
                        # Get Line pu Admittances
                        line_pusy = mc.get_inverse_eng_notation(line.impedance[0], 'pu', sp.Admittance, 'pu')
                        line_pushy = mc.get_inverse_eng_notation(line.impedance[1], 'pu', sp.Admittance, 'pu')
                        # Set Line pu Admittances
                        line.set_admittance(line_pusy, 'Série', 'pu')
                        line.set_admittance(line_pushy, 'Shunt', 'pu')

    def loads_to_pu(self, bars, components):
        """This method converts the loads nominal power to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        loads = [component for component in components if isinstance(component, sc.Loads)]
        mc = op.MagConversion()
        
        for load in loads:
            load_power = mc.get_value(load.power, 'nominal')
            load_base_power = mc.get_value(self.power, 'base')
            load.set_power(load_base_power, 'base')
            load.set_power(sp.Power(load_power / load_base_power, '', 'pu'), 'pu')

    @classmethod
    def del_instances(cls):
        cls.instances = []


####################################### Solve algorithm ##############################################
class Run():
    instances = []

    def __init__(self, conv_components) -> None:
        self.conv_components = conv_components
        self.bars = sc.Bars.get_bars()

    def prep_bars(self, components):
        # Setting adjacent bars
        for bar in self.bars: 
            if bar.id != 0:
                bar.set_adjacent(components)

    def set_base_voltages(self, conv, components):
        d = op.DefaultDictFormat()
        # Specifying groung and head bar
        head = self.bars[conv.bar]
        ground_bar = self.bars[0]
        # Getting voltage in dict struct format
        head_voltage = conv.voltage
        groung_bar_voltage = d.get_primitive_struct(sp.Voltage(complex(0), 'k', 'V'), 'base')
        # Setting base voltages for ground and head bar
        self.bars[head.id].set_voltage(head_voltage)       
        ground_bar.set_voltage(groung_bar_voltage)
        # Algorithm to set all remaining base voltages
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





