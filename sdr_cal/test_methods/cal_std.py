import yaml
import sys
import time
from datetime import datetime
from ETS_logging import text_formatter as gui
from equipment.sig_gen_functions import *
from equipment.spec_an_functions import *
from equipment.sdr_functions import *
import json
import math
import numpy as np

class EquipmentCalibrationFailed(Exception):
    pass


class Cal_Std():
    def __init__(self, test_results):
        # super().__init__(equip_config, test_equipment, radio_eeprom, radio_param, radio_ctrl, test_results=test_results)
        # self.standard_id = 'CAL_STD'
        # self.first_test_loop = True



        with open('config/beacon_sdr_cal/beacon_sdr_cal.yaml', "r") as file_descriptor:
            self.beacon_sdr_cal = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        with open('config/run_config.yaml', "r") as file_descriptor:
            self.run_config = yaml.load(file_descriptor, Loader=yaml.FullLoader)




        self.centre_freq = self.beacon_sdr_cal['test_attribute']['centre_freq']
        # self.centre_freq_offset = float(self.beacon_sdr_cal['test_attribute']['centre_freq_offset'])
        self.samp_rate = float(self.beacon_sdr_cal['test_attribute']['samp_rate'])
        self.rx_duration = self.beacon_sdr_cal['test_attribute']['rx_duration']
        self.ip = self.beacon_sdr_cal['usrp_setup']['ip']
        self.total_samples = int(self.rx_duration * self.samp_rate)

        self.rx = RF_ReceiVer(self.samp_rate, self.total_samples, self.ip)


        self.rf_freq = self.beacon_sdr_cal['sig_gen_1']['rf_frequency']
        self.level_dbm = self.beacon_sdr_cal['sig_gen_1']['level_dbm']

        self.signal_gen_1 = SigGen_SMB()

        self.total_to_measure = self.beacon_sdr_cal['test_attribute']['total_to_measure']
        self.pass_data_in_file = self.beacon_sdr_cal['test_attribute']['pass_data_in_file']
        self.cutoff = self.beacon_sdr_cal['test_attribute']['cutoff']
        self.first_filter_iq = self.beacon_sdr_cal['test_attribute']['first_filter_iq']
        self.first_decimate_iq = self.beacon_sdr_cal['test_attribute']['first_decimate_iq']

        self.test_results = test_results

        self.FSV = SpecAn_FSV(test_results=self.test_results )




    def calculate_carrier_freq(self, z, samp_rate):
        #print_w_timestamp("calculate_carrier_freq start")

        chk_thd = True
        blen = len(z)
        z_win = z
        amplitude = np.average(np.absolute(z_win))
        relative_power = 20 * np.log10(amplitude) # in dB

        # Calculate Phase
        inst_phase_s = np.angle(z_win)  # instantaneous phase
        inc_phase_s = inst_phase_s[1:] - inst_phase_s[:-1]

        # np.unwrap tries to correct Vn+1 to (Vn +- pi) range,
        # If 1st point is phase jumping point, 1st value can be close to 2*pi, and thus later values are unwrapped
        # based on it, bringing a phase floor as 6.2x(2*pi)
        if inc_phase_s[0] >= math.pi:
            inc_phase_s[0] -= 2 * math.pi

        # Note: If the window starts right around phase jumping point, the first couples values of inc_phase_i may
        #       be around 2*pi, and then unwrap will be based on the starting big values. Finally leading to unexpected
        #       frequency calculation.
        #       It will affect the S1 because no sliding window is used for F0, and F0 set the standards for S2 and S3
        #       Solution: Pop the big values out
        i = 0
        if chk_thd:
            phase_jmp_thd = 6
            for i in range(blen):
                if np.abs(inc_phase_s[i]) < phase_jmp_thd:
                    break
            if i != 0:
                print("Phase jump at beginning, pop out till idx %d" % i)
                phase_s1 = np.unwrap(inc_phase_s)
                freq_offset1 = np.sum(phase_s1) / (2 * np.pi * (blen / samp_rate))
                print("If NOT pop out, freq = %f" % freq_offset1)

        phase_s = np.unwrap(inc_phase_s[i:])

        ''' freq = delta_P / 2*pi*delta_t '''
        freq_offset = np.sum(phase_s) / (2 * np.pi * (blen / samp_rate))

        #print_w_timestamp("calculate_carrier_freq end")
        return freq_offset, amplitude, relative_power


    def read_iq_from_file(self, file, highfreq, filter_ena=False, deci_ena=False):
        with open(self.test_results.top_level_dir_path+"/"+file, "rb") as fh:
            samples = fh.read()

        fh.close()

        iq_array = []
        for i in range(len(samples) // 4 - 1):
            iq_array.append(struct.unpack('hh', samples[i * 4: (i * 4 + 4)]))

        rx_data = np.array(iq_array)

        # Get I/Q, apply Low pass filter
        x = rx_data[..., 0]
        y = rx_data[..., 1]

        if filter_ena:
            highcut = highfreq
            nyq = 0.5 * samp_rate
            high = highcut / nyq
            order = 9
            b, a = signal.butter(order, high, btype='low')
            x1 = signal.filtfilt(b, a, x)
            y1 = signal.filtfilt(b, a, y)
        else:
            x1 = x
            y1 = y

        if deci_ena:
            factor = decimation_factor

            x2 = signal.decimate(x1, factor, 3, zero_phase=True)
            y2 = signal.decimate(y1, factor, 3, zero_phase=True)
            z = x2 + 1j * y2
        else:
            z = x1 + 1j * y1

        return z


    def read_iq_from_data(self, iq_captured, highfreq, filter_ena=False, deci_ena=False):
        x = []
        y = []
        for d in iq_captured[0]:
            x.append(np.int16(d & 0xFFFF))
            y.append(np.int16((d >> 16) & 0xFFFF))

        if filter_ena:
            highcut = highfreq
            nyq = 0.5 * samp_rate
            high = highcut / nyq
            order = 9
            b, a = signal.butter(order, high, btype='low')
            x1 = signal.filtfilt(b, a, x)
            y1 = signal.filtfilt(b, a, y)
        else:
            x1 = x
            y1 = y

        if deci_ena:
            factor = decimation_factor

            x2 = signal.decimate(x1, factor, 3, zero_phase=True)
            y2 = signal.decimate(y1, factor, 3, zero_phase=True)
            z = np.array(x2) + 1j * np.array(y2)
        else:
            z = np.array(x1) + 1j * np.array(y1)

        return z

    def print_w_timestamp(self, s):
        milli_sec = int(round(time.time() * 1000)) % 1000
        print(time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '-' + str(milli_sec) + ': ' + str(s))
        return




    def beacon_sdr_test(self):
        self.print_w_timestamp(f"Starting to capture at {self.samp_rate} sampling rate")

        self.signal_gen_1.rf_frequency = self.rf_freq
        self.signal_gen_1.screen_on()

        self.signal_gen_1.power_offset_db = self.set_siggen_offset_level(self.rf_freq)

        self.signal_gen_1.rf_power_units = 'dbm'
        self.signal_gen_1.power_dbm = self.level_dbm

        self.signal_gen_1.rf_power_on = True

        # self.total_to_measure = self.beacon_sdr_cal['test_attribute']['total_to_measure']
        # self.pass_data_in_file = self.beacon_sdr_cal['test_attribute']['pass_data_in_file']
        # self.cutoff = self.beacon_sdr_cal['test_attribute']['cutoff']
        # self.first_filter_iq = self.beacon_sdr_cal['test_attribute']['first_filter_iq']
        # self.first_decimate_iq = self.beacon_sdr_cal['test_attribute']['first_decimate_iq']

        self.test_results.log_dict = {"Test[]": [],
                                      "Sigen_Frequency[MHz]": [],
                                      "SDR_Frequency[MHz]": [],
                                      "Frequency_Error_InTheory[Hz]" : [],
                                      "Frequency_Error[Hz]" : [],
                                      "Frequency_Error_Result[Hz]" : [],
                                      "Frequency_Error_Result[ppb]" : [],
                                      # "Amplitude[]" : [],
                                      "Timestamp": []
                                      }

        for freq in self.centre_freq:

            for freq_cnt in range(self.total_to_measure):
                self.rx.set_rx_freq(float(freq))
                # print("\nBurst counter: %d" % freq_cnt)
                if self.pass_data_in_file:

                    filename, iq_complex = self.rx.get_rx_samps(self.test_results.top_level_dir_path, self.total_samples, ret_val='infile')
                    # print_w_timestamp(filename)
                    if filename is None:
                        break
                    z = self.read_iq_from_file(filename, self.cutoff, filter_ena=self.first_filter_iq, deci_ena=self.first_decimate_iq)
                else:
                    filename, iq_complex = self.rx.get_rx_samps(self.test_results.top_level_dir_path, self.total_samples, ret_val='indata')
                    #print_w_timestamp(filename)
                    if filename is None:
                        break

                    z = self.read_iq_from_data(iq_complex, self.cutoff, filter_ena=self.first_filter_iq, deci_ena=self.first_decimate_iq)
                    # relative_power = 10 * np.log10(np.sum(z.real ** 2 + z.imag ** 2) / len(z)) # in dB

                #print_w_timestamp("Read data, Filter is %s, Decimate is %s" % (first_filter_iq, first_decimate_iq))

                if self.first_decimate_iq:
                    rate = self.samp_rate / self.decimation_factor
                else:
                    rate = self.samp_rate
                freq_oft, amp, power_dB = self.calculate_carrier_freq(z, rate)

                self.print_w_timestamp("Freq offset %.4f, Amplitude %d, Relative_power %.4f" % (freq_oft, amp, power_dB ))
                Frequency_Error_InTheory = float(str(self.rf_freq)+'e6') - float(freq)

                date_time ='{:%d-%b-%Y %H:%M:%S}'.format(datetime.now())
                self.test_results.log_dict["Test[]"].append(freq_cnt)

                self.test_results.log_dict["Sigen_Frequency[MHz]"].append(self.rf_freq)
                self.test_results.log_dict["SDR_Frequency[MHz]"].append(float(freq)/1e6)
                self.test_results.log_dict["Frequency_Error_InTheory[Hz]"].append(Frequency_Error_InTheory)

                self.test_results.log_dict["Frequency_Error[Hz]"].append(freq_oft)

                self.test_results.log_dict["Frequency_Error_Result[Hz]"].append(abs(Frequency_Error_InTheory-freq_oft))
                self.test_results.log_dict["Frequency_Error_Result[ppb]"].append(abs((Frequency_Error_InTheory)/float(freq)*1e3))
                self.test_results.log_dict["Timestamp"].append(date_time)

        self.test_results.save_log()
        self.signal_gen_1.rf_power_on = False

    def test_executor(self, verify_level=False):
        freq_start = self.beacon_sdr_cal['test_attribute']['start']
        freq_stop = self.beacon_sdr_cal['test_attribute']['stop']
        freq_step = self.beacon_sdr_cal['test_attribute']['step']
        freq_offset = self.beacon_sdr_cal['test_attribute']['offset']

        level_start = self.beacon_sdr_cal['sig_gen_1']['start']
        level_stop = self.beacon_sdr_cal['sig_gen_1']['stop']
        level_step = self.beacon_sdr_cal['sig_gen_1']['step']

        self.print_w_timestamp(f"Starting to capture at {self.samp_rate} sampling rate")

        self.signal_gen_1.screen_on()
        self.signal_gen_1.rf_power_units = 'dbm'

        self.signal_gen_1.rf_power_on = True

        if verify_level:
            self.test_results.log_dict = {"Frequency[MHz]": [],
                                          "Siggen_level[dBm]": [],
                                          "Verified_level[dBm]" : [],
                                          "level_offset[dB]" : [],
                                          "Pass_or_Fail": []
                                         }
        else:
            self.test_results.log_dict = {"Sigen_Frequency[MHz]": [],
                                          "SDR_Frequency[MHz]": [],
                                          "Siggen_level[dBm]": [],
                                          "Frequency_Error[Hz]" : [],
                                          "Frequency_Error_InTheory[Hz]" : [],
                                          "Frequency_Error_Result[Hz]" : [],
                                          "Frequency_Error_Result[ppb]" : [],
                                          "Amplitude[]" : [],
                                          "Relative_power[dB]" : [],
                                          "Relative_power_increment[dB]" : [],
                                          "Siggen_Increment[dB]": [],
                                          "Power_error_result[dB]": [],
                                          "Timestamp": []
                                          }

        if verify_level:
            self.FSV.reset(True)
            self.FSV.disp_on = True
            self.FSV.rbw = 10000
            self.FSV.vbw = 10000
            # self.FSV.freq_centre = freq
            self.FSV.freq_span = 0
            self.FSV.attn_internal = 20
            self.FSV.rf_level = 0


        for freq in range(freq_start, freq_stop+freq_step, freq_step):
            self.signal_gen_1.rf_frequency = freq
            self.signal_gen_1.power_offset_db = self.set_siggen_offset_level(freq)

            if verify_level:
                self.FSV.freq_centre = freq
                time.sleep(0.1)
                # self.FSV.screen_on = True

            self.rx.set_rx_freq((freq+freq_offset)*1e6)
            previous_power_dB = 0

            for level in range(level_start, level_stop+level_step, level_step):
                self.signal_gen_1.power_dbm = level
                # time.sleep(0.5)

                if verify_level:
                    self.test_results.log_dict["Frequency[MHz]"].append(freq)
                    self.test_results.log_dict["Siggen_level[dBm]"].append(level)

                    verified_level = self.FSV.read_mark()
                    level_offset = verified_level - level
                    self.test_results.log_dict["Verified_level[dBm]"].append(verified_level)
                    self.test_results.log_dict["level_offset[dB]"].append(level_offset)
                    print(verified_level, level_offset)

                    if abs(level_offset)>=0.3:
                        self.test_results.log_dict["Pass_or_Fail"].append("Fail")
                        raise EquipmentCalibrationFailed
                    else:
                        self.test_results.log_dict["Pass_or_Fail"].append("Pass")

                else:


                    if self.pass_data_in_file:

                        filename, iq_complex = self.rx.get_rx_samps(self.test_results.top_level_dir_path, self.total_samples, ret_val='infile')
                        # print_w_timestamp(filename)
                        if filename is None:
                            break
                        z = self.read_iq_from_file(filename, self.cutoff, filter_ena=self.first_filter_iq, deci_ena=self.first_decimate_iq)
                    else:
                        filename, iq_complex = self.rx.get_rx_samps(self.test_results.top_level_dir_path, self.total_samples, ret_val='indata')
                        #print_w_timestamp(filename)
                        if filename is None:
                            break

                        z = self.read_iq_from_data(iq_complex, self.cutoff, filter_ena=self.first_filter_iq, deci_ena=self.first_decimate_iq)
                        # relative_power = 10 * np.log10(np.sum(z.real ** 2 + z.imag ** 2) / len(z)) # in dB

                    #print_w_timestamp("Read data, Filter is %s, Decimate is %s" % (first_filter_iq, first_decimate_iq))

                    if self.first_decimate_iq:
                        rate = self.samp_rate / self.decimation_factor
                    else:
                        rate = self.samp_rate
                    freq_oft, amp, power_dB = self.calculate_carrier_freq(z, rate)
                    # self.print_w_timestamp("Freq offset %.4f, Amplitude %d, Relative_power %.4f" % (freq_oft, amp, power_dB ))

                    self.print_w_timestamp("Freq offset %.4f, Amplitude %d, Relative_power %.4f" % (freq_oft, amp, power_dB ))
                    power_dB_increment = power_dB - previous_power_dB
                    previous_power_dB = power_dB
                    # freq_stability = freq_oft -

                    # date_time = datetime.now().strftime("%Y_%m_%d_%H%Mh")
                    date_time ='{:%d-%b-%Y %H:%M:%S}'.format(datetime.now())
                    self.test_results.log_dict["Sigen_Frequency[MHz]"].append(freq)
                    self.test_results.log_dict["SDR_Frequency[MHz]"].append(freq+freq_offset)

                    self.test_results.log_dict["Siggen_level[dBm]"].append(level)
                    self.test_results.log_dict["Frequency_Error[Hz]"].append(freq_oft)
                    self.test_results.log_dict["Frequency_Error_InTheory[Hz]"].append(-0.01e6)
                    self.test_results.log_dict["Frequency_Error_Result[Hz]"].append(abs(-0.01e6-freq_oft))
                    self.test_results.log_dict["Frequency_Error_Result[ppb]"].append(abs((-0.01e6-freq_oft)/freq)*1000)
                    self.test_results.log_dict["Amplitude[]"].append(amp)
                    self.test_results.log_dict["Relative_power[dB]"].append(power_dB)
                    self.test_results.log_dict["Relative_power_increment[dB]"].append(power_dB_increment)
                    self.test_results.log_dict["Siggen_Increment[dB]"].append(level_step)
                    self.test_results.log_dict["Power_error_result[dB]"].append(abs(level_step-power_dB_increment))
                    self.test_results.log_dict["Timestamp"].append(date_time)

        self.test_results.save_log()
        self.signal_gen_1.rf_power_on = False



    def set_siggen_offset_level(self, freq):
        freq = float(str(freq)+'e6') # add 'e6' to represent MHz

        inter_rf_level_offset = 0

        for attenuator in self.run_config['attenuators']:
            if attenuator['used']:
                inter_rf_level_offset -= \
                np.interp(freq, attenuator['xp'], attenuator['yp'])

        for cable in self.run_config['cables']:
            if cable['used']:
                inter_rf_level_offset -= \
                np.interp(freq, cable['xp'], cable['yp'])

        return inter_rf_level_offset

    def rx_receiver_dynamic_range(self):
        pass
