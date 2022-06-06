import pyvisa as visa
import time
import re
from ETS_logging import text_formatter as gui

class EquipmentSettingFailed(Exception):
    pass

class SpecAn_FSV(object):

    def __init__(self, test_results, spec_an_config=None):
        self.spec_an_config_failed = False
        self.test_results = test_results
        if spec_an_config:
            ip_address = spec_an_config['IP']
        else:
            # Option to manually enter IP Address if running in manual mode (i.e. standalone)
            ip_address = '10.0.22.89'
        address = 'TCPIP0::' + ip_address + '::inst0::INSTR'

        self.init_spec_an(address)
        self._disp_on = None
        self._freq_centre = None
        self._freq_span = None
        self._rbw = None
        self._vbw = None
        self._attn_internal = None
        self._ref_level_offset = None
        self._trace_peak = None
        self._sweep_points = None
        self._rf_level = None
        self._ref_level_offset = None
        self._analog_demod_on = None
        self._analog_demod_af_coupling = None
        self._analog_demod_meas_time = None
        self._deviation_per_div_trace_y = None
        self._demod_bw = None
        self._transducer = None




    def init_spec_an(self, address):
        attempts = 0
        while attempts < 3:
            try:
                self.inst = None
                self.rm = visa.ResourceManager('@py')
                self.inst = self.rm.open_resource(address)
                self.spec_an_config_failed = False
                break
            except visa.errors.VisaIOError as e:
                print('Exception :', e)
                self.spec_an_config_failed = True
                attempts += 1
                continue

    def read_mark(self):
        self.inst .write("CALC:MARK1:MAX")
        # f = self.inst .query("CALC:MARK1:X?")
        level = float(self.inst .query("CALC:MARK1:Y?"))
        return level

    def spec_an_receive(self, rf_freq=None, attenuation=None, display_on=None, rbw=None, vbw=None):

        if rf_freq:
            self.freq_centre = rf_freq
        if attenuation:
            self.attn_internal = attenuation
        if display_on:
            self.disp_on = display_on
        if rbw:
            self.rbw = rbw
        if vbw:
            self.vbw = vbw


    def all_commands_set(self):
        resp = self.inst.query("*OPC?")
        return resp


    def screenshot(self, filename=None):
        gui.print_yellow('Saving Screenshot...')
        self.inst.write("HCOP:DEV:LANG PNG") # set file type to .png
        self.inst.write("HCOP:CMAP:DEF4")
        self.inst.write(f"MMEM:NAME \'C:\\temp\\Dev_Screenshot.png\'")
        self.inst.write("HCOP:IMM") # perform copy and save .png file on SpecAn
        self.inst.query("*OPC?")

        save_path = self.test_results.current_test_path + '/' +  self.test_results.log_id + filename + ".png"
        file_data = self.inst.query_binary_values(f"MMEM:DATA? \'C:\\temp\\Dev_Screenshot.png\'", datatype='s',)[0] # query binary data and save
        new_file = open(save_path, "wb")# open a new file as "binary/write" on PC
        #new_file = open(f"c:\\Temp\\{filename}.png", "wb")# open a new file as "binary/write" on PC
        new_file.write(file_data) # copy data to the file on PC
        new_file.close()
        #gui.print_red("Screenshot path not set. Saving to default location...")
        gui.print_green(f"Screenshot saved to PC {save_path}\n ")
        return True







    def meas_analog_demod_fm_dev(self):
        self.continuous_sweep = False
        peak_dev_avg = float(self.inst.query("CALC:MARK:FUNC:ADEM:FM? MIDD"))
        peak_dev_plus = float(self.inst.query("CALC:MARK:FUNC:ADEM:FM? PPE"))
        peak_dev_minus = float(self.inst.query("CALC:MARK:FUNC:ADEM:FM? MPE"))
        self.inst.query("*OPC?")
        self.continuous_sweep = True

        return peak_dev_avg, peak_dev_plus, peak_dev_minus

    def meas_acp(self, span, rbw, vbw, trace_rms, tx_chbw, aj_chbw, at_chbw, \
                 aj_chnum, aj_space, at_space, power_mode, ave_number):
        self.inst.write("CALC:MARK:FUNC:POW:SEL ACP")
        self.inst.write(f"FREQ:SPAN {span}kHz")
        self.inst.write(f"BAND {rbw}Hz")
        self.inst.write(f"BAND:VID {vbw}Hz")
        self.inst.write(f"{trace_rms}")
        self.inst.write(f"POW:ACH:BWID:CHAN1 {tx_chbw}kHz")
        self.inst.write(f"POW:ACH:BWID:ACH {aj_chbw}kHz")
        self.inst.write(f"POW:ACH:BWID:ALT1 {at_chbw}kHz")
        self.inst.write(f"POW:ACH:ACP {aj_chnum}")
        self.inst.write(f"POW:ACH:SPAC {aj_space}kHz")
        self.inst.write(f"POW:ACH:SPAC:ALT1 {at_space}kHz")
        self.inst.write(f"POW:ACH:MODE {power_mode}")
        self.inst.write(f"SWE:COUN {ave_number}")
        self.inst.write(f"CALC:MARK:FUNC:POW:MODE WRIT")
        self.inst.write(f"DISP:TRAC:MODE MAXH")
        time.sleep(5)
        acp = self.inst.query("CALC:MARK:FUNC:POW:RES? ACP")
        acp_list = re.findall(r'-?\d+\.\d+', acp)
        return acp_list

    def reset(self, val):
        if val:
            # print('Resetting...')
            self.inst.write(f"*RST")
            # print('Resetting and sleeping...')
            # time.sleep(2)
        else:
            pass

    # @property
    # def trigger_hold(self):
    #     return self._trigger_hold
    #
    # @trigger_hold.setter
    # def trigger_hold(self, trigger_offset):
    #     self.inst.write(f"TRIG:HOLD {trigger_offset}ms")
    #     self._trigger_hold = trigger_offset


    @property
    def continuous_sweep(self):
        return self._continous_sweep

    @continuous_sweep.setter
    def continuous_sweep(self, is_on):
        if is_on:
            self.inst.write(f"INIT:CONT ON")
        else:
            self.inst.write(f"INIT:CONT OFF")

    @property
    def analog_demod_on(self):
        return self._analog_demod_on

    @analog_demod_on.setter
    def analog_demod_on(self, val):
        if val:
            self.inst.write("ADEM ON")
        else:
            self.inst.write("ADEM OFF")
        self._analog_demod_on = val

    @property
    def analog_demod_af_coupling(self):
        return self._analog_demod_af_coupling

    @analog_demod_af_coupling.setter
    def analog_demod_af_coupling(self, val):
        self.inst.write(f"ADEM:AF:COUP {val}")
        self._analog_demod_af_coupling = val

    @property
    def analog_demod_meas_time(self):
        return self._analog_demod_meas_time

    @analog_demod_meas_time.setter
    def analog_demod_meas_time(self, val):
        self.inst.write(f"ADEM:MTIM {val}ms")
        self._analog_demod_meas_time = val

    @property
    def demod_bw(self):
        return self._demod_bw

    @demod_bw.setter
    def demod_bw(self, demod_bw):
        self.inst.write(f"BAND:DEM {demod_bw}Hz")
        self._demod_bw = demod_bw

    @property
    def deviation_per_div_trace_y(self):
        return self._deviation_per_div_trace_y

    @deviation_per_div_trace_y.setter
    def deviation_per_div_trace_y(self, dev_per_division):
        self.inst.write(f"DISP:TRAC:Y:PDIV {dev_per_division}Hz")
        self._deviation_per_div_trace_y = dev_per_division


    @property
    def disp_on(self):
        self._disp_on = self.inst.query("SYST:DISP:UPD?")
        return self._disp_on

    @disp_on.setter
    def disp_on(self, is_on):
        if is_on:
            self.inst.write("SYST:DISP:UPD ON")
            self._disp_on = True
        elif not is_on:
            print('off')
            self.inst.write("SYST:DISP:UPD OFF")
            self._disp_on = False

    @property
    def freq_centre(self):
#        self.inst.query('INIT: IMM; *WAI')
        self._freq_centre = self.inst.query("FREQ:CENT?")
        return float(self._freq_centre)

    @freq_centre.setter
    def freq_centre(self, freq_mhz):
        self.inst.write(f"FREQ:CENT {freq_mhz}MHz")
        if not freq_mhz == float(self.inst.query("FREQ:CENT?"))/1e6:
            raise EquipmentSettingFailed
        self._freq_centre = freq_mhz


    @property
    def freq_span(self):
        self._freq_span = self.inst.query("FREQ:SPAN?")
        return self._freq_span

    @freq_span.setter
    def freq_span(self, freq_hz):
        self.inst.write(f"FREQ:SPAN {freq_hz}Hz")

        if not freq_hz == float(self.inst.query("FREQ:SPAN?")):
            gui.print_red('freq_hz did not set correctly...')
            raise EquipmentSettingFailed
        self._freq_span = freq_hz



    @property
    def rbw(self):
        self._freq_span = self.inst.query("BAND?")
        return self._rbw

    @rbw.setter
    def rbw(self, rbw_hz):
        self.inst.write(f"BAND {rbw_hz}Hz")

        if not rbw_hz == float(self.inst.query("BAND?")):
            gui.print_red('rbw_hz did not set correctly...')
            raise EquipmentSettingFailed
        self._rbw = rbw_hz



    @property
    def vbw(self):
        self._vbw = self.inst.query("BAND:VID?")
        return self._vbw

    @vbw.setter
    def vbw(self, vbw_hz):
        self.inst.write(f"BAND:VID {vbw_hz}Hz")

        if not vbw_hz == float(self.inst.query("BAND:VID?")):
            gui.print_red('vbw_hz did not set correctly...')
            raise EquipmentSettingFailed
        self._vbw = vbw_hz

    @property
    def attn_internal(self):
        self._attn_internal = self.inst.query("INP:ATT?")
        return self._attn_internal

    @attn_internal.setter
    def attn_internal(self, attn_dBm):
        self.inst.write(f"INP:ATT {attn_dBm}")

        if not attn_dBm == float(self.inst.query("INP:ATT?")):
            gui.print_red('attn_dBm did not set correctly...')
            raise EquipmentSettingFailed
        self._attn_internal = attn_dBm


    @property
    def trace_peak(self):
        return self._trace_peak

    @trace_peak.setter
    def trace_peak(self, trace_peak):
        self.inst.write(f"{trace_peak}")
        self._trace_peak = trace_peak

    @property
    def ref_level_offset(self):
        self._ref_level_offset = self.inst.query("DISP:TRAC:Y:RLEV:OFFS?")
        return self._ref_level_offset

    @ref_level_offset.setter
    def ref_level_offset(self, ref_level_offset_dbm):
        self.inst.write(f"DISP:TRAC:Y:RLEV:OFFS {ref_level_offset_dbm}")
        self.inst.write(f"{ref_level_offset_dbm}") # Apparently necessary to write this?

        if not ref_level_offset_dbm == float(self.inst.query("DISP:TRAC:Y:RLEV:OFFS?")):
            gui.print_red('Ref Level Offset Did not set correctly...')
            raise EquipmentSettingFailed

        self._ref_level_offset = ref_level_offset_dbm

    @property
    def sweep_points(self):
        self._sweep_points = self.inst.query("SWE:POIN?")

        return self._sweep_points

    @sweep_points.setter
    def sweep_points(self, no_sweep_points):
        self.inst.write(f"SWE:POIN {no_sweep_points}")

        if not no_sweep_points == float(self.inst.query("SWE:POIN?")):
            gui.print_red('Ref Level Offset Did not set correctly...')
            raise EquipmentSettingFailed

        self._sweep_points = no_sweep_points

    @property
    def rf_level(self):
        self._rf_level = self.inst.query("DISP:TRAC:Y:RLEV?")
        return self._rf_level

    @rf_level.setter
    def rf_level(self, rf_level_db):
        self.inst.write(f"DISP:TRAC:Y:RLEV {rf_level_db}")

        if not rf_level_db == float(self.inst.query("DISP:TRAC:Y:RLEV?")):
            gui.print_red('Ref Level did not set correctly...')
            raise EquipmentSettingFailed

        self._rf_level = rf_level_db

    @property
    def marker_1(self):

        x = float(self.inst.query("CALC:MARK1:X?"))
        y = float(self.inst.query("CALC:MARK1:Y?"))
        return x, y

    @marker_1.setter
    def marker_1(self, option='MAX'):
        self.inst.write("CALC:MARK1:" + option)
        #self.inst.query('INIT: IMM; *WAI')

    @property
    def transducer(self):
        return self._transducer

    @transducer.setter
    def transducer(self, val):
        name, status = val

        self.inst.write(f"CORR:TRAN:SEL '{name}'")
        self.inst.write(f"CORR:TRAN {status}")


    def close(self):
        self.inst.close()

class SpecAn:

    def __new__(cls, test_results, spec_an_config):
        spec_an_class = SpecAn_FSV(test_results, spec_an_config)
        if spec_an_class.spec_an_config_failed:
            if spec_an_config['must_init']:
                return False
            else:
                return True

        return spec_an_class

if __name__ == "__main__":

    # Unit Test/ Sanity Check Code...

    fsv = SpecAn_FSV()
    fsv.screenshot("hehe")
    # fsv.disp_on = True
    # fsv.freq_centre = 156e6
    # fsv.ref_level_offset = 30
    # fsv.attn_internal = 45
    # fsv.rf_level = 50
    # fsv.rbw = 1e6
    # time.sleep(2)
    # fsv.close()
    # print('Done')
