from ETS_logging import text_formatter as gui
import pyvisa as visa
import time

# class EquipmentSettingFailed(Exception):
#     pass

class SigGen_SMB():

    def __init__(self, sig_gen_config=None):
        self.sig_gen_config_failed = False
        if sig_gen_config:
            ip_address = sig_gen_config['IP']
        else:
            # Option to manually enter IP Address if running in manual mode (i.e. standalone)
            ip_address = '10.0.22.83'

        address = 'TCPIP0::' + ip_address + '::inst0::INSTR'
        self.init_sig_gen(address=address)
        self.inst.write(f"*RST")

        self._rf_frequency = None
        self._rf_power_on = False
        self._lfo_frequency = None
        self._lfo_voltage_mv = None
        self._pow_dbuv = None
        self._pow_dbm = None
        self._pow_offset_db = None
        self._fm_dev_hz = None
        self._lfo_output_on = None
        self._fm_dev_on = None
        self._rf_power_units = None


        #self.reset()

    def init_sig_gen(self, address):
        attempts = 0
        while attempts < 3:
            try:
                self.inst = None
                self.rm = visa.ResourceManager('@py')
                self.inst = self.rm.open_resource(address)
                self.sig_gen_config_failed = False

                break
            except visa.errors.VisaIOError as e:
                print('Exception :', e)
                self.sig_gen_config_failed = True
                attempts += 1
                continue

    # Sets the instrument to a defined default status.
    # The default settings are indicated in the description of commands.
    def reset(self):
        self.inst.write(f"*RST")
        # Wait a second for the reset to complete
        time.sleep(1)

#Writing in a comment...

    def screen_on(self):
        self.inst.write("SYST:DISP:UPD ON")

    @property
    def rf_frequency(self):
        self._rf_frequency = float(self.inst.query(f"FREQ?"))
        return self._rf_frequency

    @rf_frequency.setter
    def rf_frequency(self, freq_mhz):
        self.inst.write(f"FREQ {float(freq_mhz)}MHz")
        self._rf_frequency = freq_mhz
        # if float(self.inst.query(f"FREQ?")) != float(freq_mhz)/1e6:
        #     gui.print_red('Failed To Set Frequency [Need to configure exceptions]')
        #     raise EquipmentSettingFailed

    @property
    def rf_power_on(self):
        self._rf_power_on = bool(self.inst.query(f"OUTP?"))
        return self._rf_power_on

    @rf_power_on.setter
    def rf_power_on(self, is_on):
        if is_on:
            self.inst.write(f"OUTP ON")
            self._rf_power_on = True
        elif not is_on:
            self.inst.write(f"OUTP OFF")
            self._rf_power_on = False

    @property
    def lfo_frequency(self):
        self._lfo_frequency = float(self.inst.query(f"LFO:FREQ?"))
        return self._lfo_frequency

    @lfo_frequency.setter
    def lfo_frequency(self, freq_khz):
        freq_khz = freq_khz/1e3
        self.inst.write(f"LFO:FREQ {float(freq_khz)}kHz")
        self._lfo_frequency = freq_khz

    @property
    def lfo_voltage_mv(self):
        self._lfo_voltage_mv = 1000 * float(self.inst.query(f"lFO:VOLT?"))
        return self._lfo_voltage_mv

    @lfo_voltage_mv.setter
    def lfo_voltage_mv(self, af_volts):
        if af_volts < 3000:
            self.inst.write(f"LFO:VOLT {float(af_volts)}mV")
            time.sleep(0.1)
        else:
            gui.print_red("Requested AF Exceeds 3000mV - Aborting")
            raise EquipmentSettingFailed
        self._lfo_voltage_mv = af_volts

    @property
    def lfo_output_on(self):
        self._lfo_output_on = bool(self.inst.query(f"LFO?"))
        return self._lfo_output_on

    @lfo_output_on.setter
    def lfo_output_on(self, is_on):
        if is_on:
            self.inst.write(f"LFO ON")
        elif not is_on:
            self.inst.write(f"LFO OFF")
        self._lfo_output_on = is_on


    @property
    def power_dbuv(self):
        return self._pow_dbuv

    @power_dbuv.setter
    def power_dbuv(self, dbuv_level):
        self.inst.write(f":UNIT:POW dBuV")
        self.inst.write(f":POW {float(dbuv_level)}dBuV")
        time.sleep(0.02)
        self._pow_dbuv = dbuv_level

    @property
    def power_dbm(self):
        return self._pow_dbm

    @power_dbuv.setter
    def power_dbuv(self, dbm_level):
        self.inst.write(f":UNIT:POW dBm")
        self.inst.write(f":POW {float(dbm_level)}dBm")
        time.sleep(0.02)
        self._pow_dbm = dbm_level

    @property
    def power_dbm(self):
        self._pow_dbm = self.inst.query(f":POW?")
        #self._pow_dbm = self.inst.query(f":UNIT:POW?")
        return self._pow_dbm


    @power_dbm.setter
    def power_dbm(self, dbm_level):
        if dbm_level > 15:
            gui.print_red('Power Set Above 0dBM. Set to 0 [Safety]')
            dbm_level = 15
        self.inst.write(f":UNIT:POW dBm")
        self.inst.write(f":POW {float(dbm_level)}dBm")
        time.sleep(0.02)
        self._pow_dbm = dbm_level

    @property
    def power_offset_db(self):
        return self._power_offset_db

    @power_offset_db.setter
    def power_offset_db(self, offset_level):
        self.inst.write(f":POW:OFFS {float(offset_level)}")
        self._power_offset_db = offset_level



    @property
    def rf_power_units(self):
        return self._rf_power_units

    @rf_power_units.setter
    def rf_power_units(self, units):
        if units == 'dbm':
            self._rf_power_units = units
        elif units == 'dbuv':
            self._rf_power_units = units
        else:
            gui.print_red('INVALID RF POWER UNITS - NOT SET')

    @property
    def fm_dev_hz(self):
        print('untested...')
        self._fm_dev_hz = float(self.inst.query(f"FM?"))
        return self._fm_dev_hz

    @fm_dev_hz.setter
    def fm_dev_hz(self, fm_dev_hz):
        fm_dev_kh = fm_dev_hz #/1e3
        self.inst.write(f"FM {float(fm_dev_hz)}Hz")
        self._fm_dev_hz = fm_dev_hz

    @property
    def fm_dev_on(self):
        return self._fm_dev_on

    @fm_dev_on.setter
    def fm_dev_on(self, is_on):
        if is_on:
            self.inst.write(f"FM:STAT ON")
        else:
            self.inst.write(f"FM:STAT OFF")

        self._fm_dev_on = True
        # fm_dev_on

    def transmit_from_sig_gen(self, rf_freq=None, rf_on=None, rf_power=None, rf_power_units=None, lfo_freq=None,
                              lfo_voltage_mv=None, lfo_on=None, fm_dev=None, fm_dev_on=None):
        if rf_freq is not None:
            self.rf_frequency = rf_freq/1e6
        if rf_power_units is not None:
            self.rf_power_units = rf_power_units
        if rf_power is not None:
            if self._rf_power_units == 'dbuv':
                self.power_dbuv = rf_power
            elif self._rf_power_units == 'dbm':
                self.power_dbm = rf_power
            else:
                gui.print_red('POWER UNITS NOT SET!!')
        if rf_on is not None:
            self.rf_power_on = rf_on
        if lfo_freq is not None:
            self.lfo_frequency = lfo_freq
        if lfo_voltage_mv is not None:
            self.lfo_voltage_mv = lfo_voltage_mv
        if lfo_on is not None:
            self.lfo_output_on = lfo_on
        if fm_dev is not None:
            self.fm_dev_hz = fm_dev
        if fm_dev_on is not None:
            self.fm_dev_on = fm_dev_on


    def close(self):
        if self.rf_power_on:
            self.rf_power_on = False
        if self.fm_dev_on:
            self.fm_dev_on = False
        if self.lfo_output_on:
            self.lfo_output_on = False
        self.inst.close()

    def all_off(self):
        if self.rf_power_on:
            self.rf_power_on = False
        if self.fm_dev_on:
            self.fm_dev_on = False
        if self.lfo_output_on:
            self.lfo_output_on = False



if __name__ == "__main__":

   # Unit Test/ Sanity Check Code...

    smb100A = SigGen_SMB()

    # smb100A.rf_power_on = True
    #
    # print(smb100A.fm_dev_hz)
    #
    # print('Done')
