import yaml
import sys
import time
from datetime import datetime
from ETS_logging import text_formatter as gui
from test_methods.radio_tests_common import RadioTest
import json
import math
import numpy as np

class ETSI_EN301025(RadioTest):
    def __init__(self, equip_config, test_equipment, radio_eeprom, radio_param, radio_ctrl, test_results):
        super().__init__(equip_config, test_equipment, radio_eeprom, radio_param, radio_ctrl, test_results=test_results)
        self.standard_id = 'ETSI_EN301025'
        self.first_test_loop = True

    def test_1(self):
        self.test_results.test_id = 'ETSI_EN301025 Test 1'
        print('Testing ETSI_EN301025 Test 1...')
        return True

    def test_2(self):
        self.test_results.test_id = 'ETSI_EN301025 Test 2'
        print('Testing ETSI_EN301025 Test 2...')
        return False


    def tx_frequency_error(self, test_config_opt):
        test_id = 'tx_frequency_error'
        self.test_equip.rf_switch.state_tx_rx = 'TX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.radio_power_on()
        self.check_radio_serial_comms()
        self.radio_tx_off()

        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        self.setup_spec_an(config=test_config['spec_an'])

        screenshot = test_config['spec_an']['screenshot']
        looping_arrays = self.get_looping_arrays(test_config=test_config)

        self.test_results.log_dict = {"Frequency[Hz]" : [],
                                      "Frequency_Error[Hz]" : [],
                                      "Power[dBm]" : [],
                                      "Voltage[V]" : [],
                                      "Radio_Power_Mode": [],
                                      "Timestamp": [],
                                      "Temperature[C]": [],
                                      }

        test_result = self.tx_test_executor(looping_arrays=looping_arrays, test_function=self._tx_frequency_error, screenshot=screenshot)
        self.test_results.save_log()

        return test_result

    def _tx_frequency_error(self, freq, voltage, temp, radio_power, screenshot, test_config=None):

        self.test_equip.psu.voltage = voltage


        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        self.test_equip.psu.current_limit = self.radio_param.tx_on_current_max[radio_power]
        self.test_equip.spec_an.freq_centre = freq
        self.radio_transmit(freq=freq, power_level=radio_power)
        time.sleep(0.5) # allow some time for spec an to act

        start = time.perf_counter()
        self.test_equip.spec_an.marker_1 = "MAX"

        # print(self.test_equip.spec_an.all_commands_set())
        finish_a = time.perf_counter()
        freq, power = self.test_equip.spec_an.marker_1
        finish_b = time.perf_counter()
        #print(f'Time Elapsed: {finish_a-start/1e3:.2f}ms') #, B: {finish_b-start/1e3:.2f}ms')

        freq_error = freq - self.test_equip.spec_an.freq_centre

        # self.test_equip.
        print(f'Frequency: {self.test_equip.spec_an.freq_centre/1e6:.3f} MHz, Freq Error: {freq_error:.2f} Hz, Power: {power:.2f} dBm, '
              f'Power Mode: {radio_power}, Temp: {temp}, Voltage: {voltage}')

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.test_results.log_dict["Frequency[Hz]"].append(freq)
        self.test_results.log_dict["Frequency_Error[Hz]"].append(freq_error)
        self.test_results.log_dict["Power[dBm]"].append(power)
        self.test_results.log_dict["Voltage[V]"].append(voltage)
        self.test_results.log_dict["Radio_Power_Mode"].append(radio_power)
        self.test_results.log_dict["Timestamp"].append(date_time)
        self.test_results.log_dict["Temperature[C]"].append(temp)

        if screenshot:
            date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
            self.test_equip.spec_an.screenshot(filename=date_time)
        self.radio_tx_off()

        return True




    def tx_frequency_deviation(self, test_config_opt):
        test_id = 'tx_frequency_deviation'
        self.test_equip.rf_switch.state_tx_rx = 'TX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.radio_power_on()
        self.check_radio_serial_comms()
        self.radio_tx_off()

        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        self.setup_spec_an(config=test_config['spec_an'])

        screenshot = test_config['spec_an']['screenshot']
        looping_arrays = self.get_looping_arrays(test_config=test_config)

        self.test_results.log_dict = {"Frequency[Hz]" : [],
                                      "Mod_Freq[Hz]" : [],
                                      "LF_Power_nom[mV]":[],
                                      "FM_Dev_nom[Hz]" : [],
                                      "LF_Power[mV]": [],
                                      "FM_Dev_max_permissible[Hz]": [],
                                      "FM_Dev_pk_avg[Hz]": [],
                                      "FM_Dev_pk_plus[Hz]": [],
                                      "FM_Dev_pk_minus[Hz]": [],
                                      #"TX_Power[dBm]" : [],
                                      "Radio_Voltage[V]" : [],
                                      "Radio_Power_Mode": [],
                                      "Temperature[C]": [],
                                      "Timestamp": [],
                                      "Test_Passed": [],
                                      }

        test_result = self.tx_test_executor(looping_arrays=looping_arrays, test_function=self._tx_frequency_deviation,
                                            screenshot=screenshot, test_config=test_config)
        self.test_results.save_log()

        return test_result

    def _tx_frequency_deviation(self, freq, voltage, temp, radio_power, screenshot, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage
        self.test_equip.psu.current_limit = self.radio_param.tx_on_current_max[radio_power]


        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.lf_set_power_mv = test_config['sig_gen_1']['power']['start_mv']
            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)
            self.first_test_loop = False

        else:
            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)
        # Find 3k deviation at nominal frequency
        self.test_equip.signal_gen_1.lfo_frequency = test_config['normal_test_mod']


        self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv
        self.test_equip.signal_gen_1.lfo_output_on = True

        fm_dev_pk_avg = float(self.test_equip.spec_an.meas_analog_demod_fm_dev()[0])
        target_fm_dev = float(test_config['normal_fm_dev'])
        found_target_fm_dev = False
        #lf_power_nominal = None
        fm_dev_nominal = None
        max_permissible_fm_dev = None

        while not found_target_fm_dev:
            print(f'Searching for Target FM Dev. LF_set_mv: {self.lf_set_power_mv}')

            if (fm_dev_pk_avg >= target_fm_dev + float(test_config['tolerance_fm_dev'])) and self.lf_set_power_mv > test_config['sig_gen_1']['power']['min_mv']:
                self.lf_set_power_mv -= float(test_config['sig_gen_1']['power']['step'])
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv


            elif fm_dev_pk_avg < target_fm_dev and self.lf_set_power_mv < test_config['sig_gen_1']['power']['max_mv']:
                self.lf_set_power_mv += test_config['sig_gen_1']['power']['step']
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv

            fm_dev_pk_avg = self.test_equip.spec_an.meas_analog_demod_fm_dev()[0]

            if target_fm_dev <=  fm_dev_pk_avg <= target_fm_dev + float(test_config['tolerance_fm_dev']):
                gui.print_green(f"Found {fm_dev_pk_avg} fm_dev @ {test_config['normal_test_mod']}kHz")
                found_target_fm_dev = True
                if screenshot:
                    date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
                    # self.test_equip.spec_an.screenshot(filename=str(test_config['normal_test_mod']) + '_hz_' + date_time)
                    self.test_equip.spec_an.screenshot(filename='_' + str(freq) + 'Hz_ ' + str(test_config['normal_test_mod']) + '_hz_' + date_time)

                fm_dev_nominal = fm_dev_pk_avg
                #self.lf_set_power_mv = self.lf_set_power_mv * 10 # Increase output by 20 dB
                lf_power_set = self.lf_set_power_mv * 10
                #print('Debug new lf_set_power_mv ', lf_power_set)


        mod_frequencies = test_config['lfo_frequency']

        idx = 0
        for mod_freq in mod_frequencies:
            mod_freq = float(mod_freq)
            self.test_equip.signal_gen_1.lfo_frequency = mod_freq
            self.test_equip.signal_gen_1.lfo_voltage_mv = lf_power_set
            fm_dev_pk_avg, fm_dev_pk_plus, fm_dev_pk_minus = self.test_equip.spec_an.meas_analog_demod_fm_dev()

            if screenshot:
                date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
                self.test_equip.spec_an.screenshot(filename='_' + str(freq) + 'Hz_ ' + str(mod_freq) + '_hz_' + date_time)

            if float(test_config['lf_freq_normal_range'][0]) <= mod_freq <= (float(test_config['lf_freq_normal_range'][1])):
                max_permissible_fm_dev = test_config['max_fm_dev_normal_range']

            elif float(test_config['lf_freq_high_range'][0]) <= mod_freq <= float(test_config['lf_freq_high_range'][1]):
                # attn_per_octave = 14 # Attenuation per octave

                log_base_volt = 10
                log_const_volt = 20 # Gain for Voltage is 20 * log_10_(f2/f1)

                gain_per_octave = test_config['gain_per_octave_dB'] # # Gain per octave


                no_octaves = math.log(mod_freq/float(test_config['lf_freq_high_range'][0]), 2)

                max_permissible_fm_dev = log_base_volt**(gain_per_octave*no_octaves/log_const_volt)*test_config['max_fm_dev_high_range']

                print(f'Max Permissible FM_Dev: {max_permissible_fm_dev:.2f} No_Octaves: {no_octaves:.2f} ')

            if fm_dev_pk_avg <= max_permissible_fm_dev:
                test_passed.append(True)
            else:
                test_passed.append(False)

            print(
                f'Frequency: {freq / 1e6:.3f} MHz, Mod_Freq {mod_freq:.2f} Hz, LF_Power_nom: {self.lf_set_power_mv:.2f} mV, '
                f'LF_Set_Power[mV] {lf_power_set:.2f}, fm_dev_pk_avg {fm_dev_pk_avg:.2f}, '
                f'Power Mode: {radio_power}, Temp: {temp}, Voltage: {voltage} Test_Passed: {test_passed[idx]}')

            date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.test_results.log_dict["Frequency[Hz]"].append(freq)
            self.test_results.log_dict["Mod_Freq[Hz]"].append(mod_freq)
            self.test_results.log_dict["LF_Power_nom[mV]"].append(self.lf_set_power_mv)
            self.test_results.log_dict["FM_Dev_nom[Hz]"].append(fm_dev_nominal)
            self.test_results.log_dict["LF_Power[mV]"].append(lf_power_set)
            self.test_results.log_dict["FM_Dev_max_permissible[Hz]"].append(max_permissible_fm_dev)
            self.test_results.log_dict["FM_Dev_pk_avg[Hz]"].append(fm_dev_pk_avg)
            self.test_results.log_dict["FM_Dev_pk_plus[Hz]"].append(fm_dev_pk_plus)
            self.test_results.log_dict["FM_Dev_pk_minus[Hz]"].append(fm_dev_pk_minus)
            # self.test_results.log_dict["TX_Power[dBm]"].append()
            self.test_results.log_dict["Radio_Voltage[V]"].append(voltage)
            self.test_results.log_dict["Radio_Power_Mode"].append(radio_power)
            self.test_results.log_dict["Temperature[C]"].append(temp)
            self.test_results.log_dict["Timestamp"].append(date_time)
            self.test_results.log_dict["Test_Passed"].append(test_passed[idx])
            idx += 1

        self.radio_tx_off()
        if False in test_passed:
            return False
        else:
            return True


    def tx_audio_frequency_response(self, test_config_opt):

        test_id = 'tx_audio_frequency_response'
        self.test_equip.rf_switch.state_tx_rx = 'TX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.radio_power_on()
        self.check_radio_serial_comms()
        self.radio_tx_off()

        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        self.setup_spec_an(config=test_config['spec_an'])

        screenshot = test_config['spec_an']['screenshot']
        looping_arrays = self.get_looping_arrays(test_config=test_config)

        self.test_results.log_dict = {"Frequency[Hz]" : [],
                                      "Mod_Freq[Hz]" : [],
                                      "FM_Dev_nom[Hz]" : [],
                                      "LF_Power[mV]": [],
                                      "FM_Dev_min_permissible[dB]": [],
                                      "FM_Dev_max_permissible[dB]": [],
                                      "FM_Dev_pk_avg[dB]": [],
                                      "FM_Dev_pk_avg[Hz]": [],
                                      "FM_Dev_pk_plus[Hz]": [],
                                      "FM_Dev_pk_minus[Hz]": [],
                                      "Radio_Voltage[V]" : [],
                                      "Radio_Power_Mode": [],
                                      "Temperature[C]": [],
                                      "Timestamp": [],
                                      "Test_Passed": [],
                                      }

        test_result = self.tx_test_executor(looping_arrays=looping_arrays, test_function=self._tx_audio_frequency_response,
                                            screenshot=screenshot, test_config=test_config)
        self.test_results.save_log()

        return test_result


        pass



    def _tx_audio_frequency_response(self, freq, voltage, temp, radio_power, screenshot, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage
        self.test_equip.psu.current_limit = self.radio_param.tx_on_current_max[radio_power]

        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.lf_set_power_mv = test_config['sig_gen_1']['power']['start_mv']
            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)
            self.first_test_loop = False

        else:
            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)

        # Find 1k deviation at nominal frequency
        self.test_equip.signal_gen_1.lfo_frequency = test_config['normal_test_mod']
        self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv
        self.test_equip.signal_gen_1.lfo_output_on = True

        fm_dev_pk_avg = float(self.test_equip.spec_an.meas_analog_demod_fm_dev()[0])
        target_fm_dev = float(test_config['normal_fm_dev'])
        found_target_fm_dev = False
        # lf_power_nominal = None
        fm_dev_nominal = None
        max_permissible_fm_dev = None

        while not found_target_fm_dev:
            print(f'Searching for Target FM Dev. LF_set_mv: {self.lf_set_power_mv}')

            if (fm_dev_pk_avg >= target_fm_dev + float(test_config['tolerance_fm_dev'])) and self.lf_set_power_mv > \
                    test_config['sig_gen_1']['power']['min_mv']:
                self.lf_set_power_mv -= float(test_config['sig_gen_1']['power']['step'])
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv


            elif fm_dev_pk_avg < target_fm_dev and self.lf_set_power_mv < test_config['sig_gen_1']['power'][
                'max_mv']:
                self.lf_set_power_mv += test_config['sig_gen_1']['power']['step']
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv

            fm_dev_pk_avg = self.test_equip.spec_an.meas_analog_demod_fm_dev()[0]

            if target_fm_dev <= fm_dev_pk_avg <= target_fm_dev + float(test_config['tolerance_fm_dev']):
                gui.print_green(f"Found {fm_dev_pk_avg} fm_dev @ {test_config['normal_test_mod']}kHz")
                found_target_fm_dev = True
                if screenshot:
                    date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
                    self.test_equip.spec_an.screenshot(filename='_' + str(freq) + 'Hz_ ' + str(
                        test_config['normal_test_mod']) + '_hz_' + date_time)

                fm_dev_nominal = fm_dev_pk_avg

        mod_frequencies = test_config['lfo_frequency']

        idx = 0

        for mod_freq in mod_frequencies:
            mod_freq = float(mod_freq)
            self.test_equip.signal_gen_1.lfo_frequency = mod_freq
            fm_dev_pk_avg, fm_dev_pk_plus, fm_dev_pk_minus = self.test_equip.spec_an.meas_analog_demod_fm_dev()

            if screenshot:
                date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
                self.test_equip.spec_an.screenshot(filename='_' + str(freq) + 'Hz_ ' + str(mod_freq) + '_hz_' + date_time)

            log_const_freq = 20  # Gain for frequency is 20 * log_10_(f2/f1)
            log_base_freq = 10

            no_octaves = math.log(mod_freq / test_config['normal_test_mod'], 2)
            gain_per_octave = test_config['gain_per_octave_dB'] # # Gain per octave

            fm_dev_pk_avg_db = log_const_freq * math.log(fm_dev_pk_avg/fm_dev_nominal, log_base_freq)
            max_permissible_fm_dev_db = gain_per_octave * no_octaves + test_config['af_response_upper_lim']
            min_permissible_fm_dev_db = gain_per_octave * no_octaves + test_config['af_response_lower_lim']

            if min_permissible_fm_dev_db <= fm_dev_pk_avg_db <= max_permissible_fm_dev_db:
                test_passed.append(True)
            else:
                test_passed.append(False)

            print(
                f'Frequency: {freq / 1e6:.3f} MHz, Mod_Freq {mod_freq:.2f} Hz, '
                f'LF_Power[mV] {self.lf_set_power_mv}, fm_dev_pk_avg {fm_dev_pk_avg:.2f}, '
                f'fm_dev_pk_avg_db {fm_dev_pk_avg_db}, FM_Dev_min_permissible[dB]: {min_permissible_fm_dev_db:.2f}, \n FM_Dev_max_permissible[dB]: {max_permissible_fm_dev_db:.2f} '
                f'Power Mode: {radio_power}, Temp: {temp}, Voltage: {voltage} Test_Passed: {test_passed[idx]}')

            date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.test_results.log_dict["Frequency[Hz]"].append(freq)
            self.test_results.log_dict["Mod_Freq[Hz]"].append(mod_freq)
            self.test_results.log_dict["FM_Dev_nom[Hz]"].append(fm_dev_nominal)
            self.test_results.log_dict["LF_Power[mV]"].append(self.lf_set_power_mv)
            self.test_results.log_dict["FM_Dev_min_permissible[dB]"].append(min_permissible_fm_dev_db)
            self.test_results.log_dict["FM_Dev_max_permissible[dB]"].append(max_permissible_fm_dev_db)
            self.test_results.log_dict["FM_Dev_pk_avg[dB]"].append(fm_dev_pk_avg_db)
            self.test_results.log_dict["FM_Dev_pk_avg[Hz]"].append(fm_dev_pk_avg)
            self.test_results.log_dict["FM_Dev_pk_plus[Hz]"].append(fm_dev_pk_plus)
            self.test_results.log_dict["FM_Dev_pk_minus[Hz]"].append(fm_dev_pk_minus)
            # self.test_results.log_dict["TX_Power[dBm]"].append()
            self.test_results.log_dict["Radio_Voltage[V]"].append(voltage)
            self.test_results.log_dict["Radio_Power_Mode"].append(radio_power)
            self.test_results.log_dict["Temperature[C]"].append(temp)
            self.test_results.log_dict["Timestamp"].append(date_time)
            self.test_results.log_dict["Test_Passed"].append(test_passed[idx])
            idx += 1

        self.radio_tx_off()
        if False in test_passed:
            return False
        else:
            return True

    def tx_audio_frequency_harmonic_distortion_emission(self):
        pass

    def tx_adjacent_channel_power(self, test_config_opt):
        test_id = 'tx_adjacent_channel_power'
        self.test_equip.rf_switch.state_tx_rx = 'TX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.radio_power_on()
        self.check_radio_serial_comms()
        self.radio_tx_off()

        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)

        self.test_results.test_param_log(test_config, test_config_opt)

        self.setup_spec_an(config=test_config['spec_an'])

        screenshot = test_config['spec_an']['screenshot']
        looping_arrays = self.get_looping_arrays(test_config=test_config)

        self.test_results.log_dict = {"Frequency[Hz]" : [],
                                      "Carrier_Power[dBm]" : [],
                                      "ACP-[dBc]":[],
                                      "ACP+[dBc]" : [],
                                      "ACP-[dBm]":[],
                                      "ACP+[dBm]" : [],
                                      #"TX_Power[dBm]" : [],
                                      "Radio_Voltage[V]" : [],
                                      "Radio_Power_Mode": [],
                                      "Temperature[C]": [],
                                      "Timestamp": [],
                                      "Test_Passed": [],
                                      }

        test_result = self.tx_test_executor(looping_arrays=looping_arrays, test_function=self._tx_adjacent_channel_power,
                                            screenshot=screenshot, test_config=test_config)
        self.test_results.save_log()

        return test_result

    def _tx_adjacent_channel_power(self, freq, voltage, temp, radio_power, screenshot, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage
        self.test_equip.psu.current_limit = self.radio_param.tx_on_current_max[radio_power]


        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.lf_set_power_mv = test_config['sig_gen_1']['power']['start_mv']

            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)
            self.first_test_loop = False

        else:
            self.transmit_radio_to_spec_an(freq=freq, power=radio_power, mod_source=0)
        # Find 3k deviation at nominal frequency
        self.test_equip.signal_gen_1.lfo_frequency = test_config['normal_test_mod']


        self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv
        self.test_equip.signal_gen_1.lfo_output_on = True

        fm_dev_pk_avg = float(self.test_equip.spec_an.meas_analog_demod_fm_dev()[0])
        target_fm_dev = float(test_config['normal_fm_dev'])
        found_target_fm_dev = False
        #lf_power_nominal = None
        fm_dev_nominal = None
        max_permissible_fm_dev = None

        while not found_target_fm_dev:
            print(f'Searching for Target FM Dev. LF_set_mv: {self.lf_set_power_mv}')

            if (fm_dev_pk_avg >= target_fm_dev + float(test_config['tolerance_fm_dev'])) and self.lf_set_power_mv > test_config['sig_gen_1']['power']['min_mv']:
                self.lf_set_power_mv -= float(test_config['sig_gen_1']['power']['step'])
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv


            elif fm_dev_pk_avg < target_fm_dev and self.lf_set_power_mv < test_config['sig_gen_1']['power']['max_mv']:
                self.lf_set_power_mv += test_config['sig_gen_1']['power']['step']
                self.test_equip.signal_gen_1.lfo_voltage_mv = self.lf_set_power_mv

            fm_dev_pk_avg = self.test_equip.spec_an.meas_analog_demod_fm_dev()[0]

            if target_fm_dev <=  fm_dev_pk_avg <= target_fm_dev + float(test_config['tolerance_fm_dev']):
                gui.print_green(f"Found {fm_dev_pk_avg} fm_dev @ {test_config['normal_test_mod']}kHz")
                found_target_fm_dev = True
                if screenshot:
                    date_time = datetime.now().strftime("%Y_%m_%d_%H%M_%S")
                    # self.test_equip.spec_an.screenshot(filename=str(test_config['normal_test_mod']) + '_hz_' + date_time)
                    self.test_equip.spec_an.screenshot(filename='_' + str(freq) + 'Hz_ ' + str(test_config['normal_test_mod']) + '_hz_' + date_time)

                fm_dev_nominal = fm_dev_pk_avg
                #self.lf_set_power_mv = self.lf_set_power_mv * 10 # Increase output by 20 dB
                lf_power_set = self.lf_set_power_mv * 10

        self.test_equip.signal_gen_1.lfo_voltage_mv = lf_power_set
                #print('Debug new lf_set_power_mv ', lf_power_set)

        acp_config = test_config['spec_an']['acp']

        acp_list = self.test_equip.spec_an.meas_acp(span=acp_config['span'],\
                                                    rbw=acp_config['rbw'],\
                                                    vbw=acp_config['vbw'],\
                                                    trace_rms=acp_config['trace_rms'],\
                                                    tx_chbw=acp_config['tx_chbw'],\
                                                    aj_chbw=acp_config['aj_chbw'],\
                                                    at_chbw=acp_config['at_chbw'],\
                                                    aj_chnum=acp_config['aj_chnum'],\
                                                    aj_space=acp_config['aj_space'],\
                                                    at_space=acp_config['at_space'],\
                                                    power_mode=acp_config['power_mode'],\
                                                    ave_number=acp_config['ave_number'])
        print(acp_list)



    def tx_conducted_spurious_emissions_conveyed_antenna(self):
        pass

    def tx_cabinet_radiation_conducted_spurious_emissions_other(self):
        pass

    def tx_transient_frequency_behaviour_transmitter(self):
        pass

    def tx_residual_modulation_transmitter(self):
        pass

    def rx_harmonic_distortion_rated_audio_frequency_output_power(self):
        pass

    def rx_audio_frequency_response(self):
        pass


    def get_test_config(self, test_config_opt, test_id):

        if test_config_opt == 'default_config':
            with open('config\\test_settings_config\\ETSI_EN301025_DEFAULT\\' + test_id + '.yaml', "r") as file_descriptor:
                test_config = yaml.load(file_descriptor, Loader=yaml.FullLoader)[test_config_opt]
        else:
            with open('config\\test_settings_config\\ETSI_EN301025_CUSTOM\\' + test_id + '.yaml', "r") as file_descriptor:
                test_config = yaml.load(file_descriptor, Loader=yaml.FullLoader)[test_config_opt]

        return test_config

    def rx_maximum_usable_sensitivity(self, test_config_opt):

        test_id = 'rx_maximum_usable_sensitivity'
        self.test_equip.rf_switch.state_tx_rx = 'RX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)
        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        self.test_equip.soundcard.num_samples = test_config['soundcard']['no_samples']
        self.test_equip.soundcard.psophometric_weighting = test_config['soundcard']['psophometric_weighting']

        self.transmit_sig_gen_to_radio(rf_power_units=test_config['sig_gen_1']['power']['units'],
                                                           lfo_freq=test_config['sig_gen_1']['lfo_frequency'],
                                                           fm_dev=test_config['sig_gen_1']['fm_dev'],
                                                           lfo_on=False, rf_on=False, fm_dev_on=False, sig_gen_no=1)

        self.transmit_sig_gen_to_radio(lfo_on=False, rf_on=False, fm_dev_on=False, sig_gen_no=2)


        self.test_equip.signal_gen_1.fm_dev_on = True


        self.check_radio_serial_comms()
        self.radio_tx_off()

        looping_arrays = self.get_looping_arrays(test_config=test_config)
        self.first_test_loop = True

        self.test_results.log_dict = {"Frequency[Hz]" : [],
                                      "SINAD[dB]" : [],
                                      "Rx Power[dBuv]" : [],
                                      "Voltage[V]" : [],
                                      "Temperature[C]": [],
                                      "Timestamp": [],
                                      "Test_Passed" : [],
                                      }

        test_result = self.rx_test_executor(looping_arrays=looping_arrays,
                                            test_function=self._rx_maximum_usable_sensitivity, test_config=test_config)

        self.test_results.save_log()
        self.test_equip.signal_gen_1.rf_power_on = False

        return test_result


    def _rx_maximum_usable_sensitivity(self, freq, voltage, temp, rx_radio_power, test_config):
        self.test_equip.psu.voltage = voltage

        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.rx_set_power = test_config['sig_gen_1']['power']['start']
            self.transmit_sig_gen_to_radio(rf_freq=freq, rf_power=self.rx_set_power, rf_on=True, fm_dev_on=True, sig_gen_no=1,
                                           audio_vol=int(test_config['radio_volume']), sql_toggle=1)
            self.first_test_loop = False
            print('Sig Gen 1 should now be transmitting...')
            time.sleep(10)

        else:
            self.transmit_sig_gen_to_radio(rf_freq=freq, audio_vol=int(test_config['radio_volume']), sig_gen_no=1, sql_toggle=1)

        sinad, self.rx_set_power = self.find_sinad_power(target_sinad=test_config['sinad_target'], set_power=self.rx_set_power,
                              max_power=test_config['sig_gen_1']['power']['max'], min_power=test_config['sig_gen_1']['power']['min'],
                                                         power_step=test_config['sig_gen_1']['power']['step'], stable_sinad=False)

        if sinad >= test_config['sinad_target'] and self.rx_set_power <= test_config['sig_gen_1']['power']['thresh']:
            test_passed = True
        else:
            test_passed = False

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        print(f'Frequency: {self.test_equip.signal_gen_1.rf_frequency/1e6:.3f} MHz, SINAD: {sinad:.2f} dB, Rx Power: {self.rx_set_power} dBuv ')
        self.test_results.log_dict["Frequency[Hz]"].append(freq)
        self.test_results.log_dict["SINAD[dB]"].append(sinad)
        self.test_results.log_dict["Rx Power[dBuv]"].append(self.rx_set_power)
        self.test_results.log_dict["Voltage[V]"].append(voltage)
        self.test_results.log_dict["Temperature[C]"].append(temp)
        self.test_results.log_dict["Timestamp"].append(date_time)
        self.test_results.log_dict["Test_Passed"].append(test_passed)

        return test_passed

    def rx_co_channel_rejection(self):

        pass


    def rx_adjacent_channel_selectivity(self, test_config_opt):

        test_id = 'rx_adjacent_channel_selectivity'

        self.test_equip.rf_switch.state_tx_rx = 'RX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.check_radio_serial_comms()
        self.radio_tx_off()
        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        looping_arrays = self.get_looping_arrays(test_config=test_config)
        self.first_test_loop = True

        self.test_equip.soundcard.num_samples = test_config['soundcard']['no_samples']
        self.test_equip.soundcard.psophometric_weighting = test_config['soundcard']['psophometric_weighting']

        self.test_equip.signal_gen_1.transmit_from_sig_gen(rf_power_units=test_config['sig_gen_1']['power']['units'],
                                                           lfo_freq=test_config['sig_gen_1']['lfo_frequency'],
                                                           fm_dev=test_config['sig_gen_1']['fm_dev'],
                                                           lfo_on=False, rf_on=False, fm_dev_on=False)

        self.test_equip.signal_gen_2.transmit_from_sig_gen(rf_power_units=test_config['sig_gen_2']['power']['units'],
                                                           lfo_freq=test_config['sig_gen_2']['lfo_frequency'],
                                                           fm_dev=test_config['sig_gen_2']['fm_dev'],
                                                           lfo_on=False, rf_on=False, fm_dev_on=False)

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.test_results.log_dict = {
                                      "RX_Frequency[Hz]": [],
                                      "INTERFERE_Frequency[Hz]": [],
                                      "Channel_Selectivity[dB]": [],
                                      "RX_Power[dBm]": [],
                                      "INTERFERE_Power[dBm]": [],
                                      "SINAD[dB]": [],
                                      "Radio_Voltage[V]": [],
                                      "Temperature[C]": [],
                                      "Timestamp": [],
                                      "Test_Passed": [],
                                      }

        test_result = self.rx_test_executor(looping_arrays=looping_arrays,
                                            test_function=self._rx_adjacent_channel_selectivity, test_config=test_config)

        self.test_results.save_log()
        self.test_equip.signal_gen_1.rf_power_on = False
        self.test_equip.signal_gen_2.rf_power_on = False

        return test_result

    def _rx_adjacent_channel_selectivity(self, freq, voltage, temp, rx_radio_power, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage

        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))


        if self.first_test_loop:
            self.rx_set_power = test_config['sig_gen_1']['power']['start']
            self.interfere_power = test_config['sig_gen_2']['power']['start']
            self.transmit_sig_gen_to_radio(rf_freq=freq, rf_power=self.rx_set_power, rf_on=True, fm_dev_on=True, sql_toggle=1, sig_gen_no=1, audio_vol=1)
            self.first_test_loop = False
        else:
            self.transmit_sig_gen_to_radio(rf_freq=freq, audio_vol=int(test_config['radio_volume']), sig_gen_no=1)

        sinad, self.rx_set_power = self.find_sinad_power(target_sinad=test_config['sinad_target'], set_power=self.rx_set_power,
                              max_power=test_config['sig_gen_1']['power']['max'], min_power=test_config['sig_gen_1']['power']['min'],
                                                         power_step=test_config['sig_gen_1']['power']['step'])

        interference_freq_offsets = test_config['adj_chan_freq']
        interference_power_thresh = self.rx_set_power + test_config['min_adj_chan_selectivity']

        if not sinad >= test_config['sinad_target']:
            gui.print_red('20dB SINAD Not Reached')
            test_passed = False
            return test_passed

        idx = 0
        for freq_offsets in interference_freq_offsets:

            interference_freq = freq + float(freq_offsets)
            self.transmit_sig_gen_to_radio(rf_freq=interference_freq, rf_power=self.interfere_power, rf_on=True, fm_dev_on=True, sig_gen_no=2)

            sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=False,
                                          max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                          num_measurements=test_config['soundcard']['sinad_no_readings'])

            while True:

                if sinad >= test_config['min_sinad'] and self.interfere_power < test_config['sig_gen_2']['power']['max']:
                    self.interfere_power += test_config['sig_gen_2']['power']['step']
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)
                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=True,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                elif sinad < test_config['min_sinad'] and self.interfere_power > test_config['sig_gen_2']['power']['min']:
                    self.interfere_power -= test_config['sig_gen_2']['power']['step']
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)

                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=False,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                if sinad >= test_config['min_sinad'] and sinad < test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']:
                    # print('Target Acheived :)')

                    break

            if self.interfere_power >= interference_power_thresh:
                test_passed.append(True)
            else:
                test_passed.append(False)

            self.transmit_sig_gen_to_radio(rf_on=False, fm_dev_on=False, sig_gen_no=2)
            print(f'RX_Frequency: {freq/1e6:.3f} MHz, Inter Freq: {interference_freq/1e6:.3f}MHz, Channel_Selectivity: '
                  f'{self.interfere_power - self.rx_set_power:.2f} dB, SINAD: {sinad:.2f} dB, RX_Power: {self.rx_set_power} dBm, '
                  f'INTERFERE_Power[dBm]: {self.interfere_power:.2f} Passed: {test_passed[idx]}')

            date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.test_results.log_dict["RX_Frequency[Hz]"].append(freq)
            self.test_results.log_dict["INTERFERE_Frequency[Hz]"].append(interference_freq)
            self.test_results.log_dict["Channel_Selectivity[dB]"].append(self.interfere_power - self.rx_set_power)
            self.test_results.log_dict["RX_Power[dBm]"].append(self.rx_set_power)
            self.test_results.log_dict["INTERFERE_Power[dBm]"].append(self.interfere_power)
            self.test_results.log_dict["SINAD[dB]"].append(sinad)
            self.test_results.log_dict["Radio_Voltage[V]"].append(voltage)
            self.test_results.log_dict["Temperature[C]"].append(temp)
            self.test_results.log_dict["Timestamp"].append(date_time)
            self.test_results.log_dict["Test_Passed"].append(test_passed[idx])

        if False in test_passed:
            return False
        else:
            return True


    def rx_spurious_response_rejection(self, test_config_opt):

        test_id = 'rx_spurious_response_rejection'

        self.test_equip.rf_switch.state_tx_rx = 'RX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.check_radio_serial_comms()
        self.radio_tx_off()
        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        looping_arrays = self.get_looping_arrays(test_config=test_config)
        self.first_test_loop = True

        self.test_equip.soundcard.num_samples = test_config['soundcard']['no_samples']
        self.test_equip.soundcard.psophometric_weighting = test_config['soundcard']['psophometric_weighting']

        self.test_equip.signal_gen_1.transmit_from_sig_gen(
            rf_power_units=test_config['sig_gen_1']['power']['units'],
            lfo_freq=test_config['sig_gen_1']['lfo_frequency'],
            fm_dev=test_config['sig_gen_1']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False)

        self.test_equip.signal_gen_2.transmit_from_sig_gen(
            rf_power_units=test_config['sig_gen_2']['power']['units'],
            lfo_freq=test_config['sig_gen_2']['lfo_frequency'],
            fm_dev=test_config['sig_gen_2']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False)

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.test_results.log_dict = {
            "RX_Frequency[Hz]": [],
            "INTERFERE_Frequency[Hz]": [],
            "Spurious_Resp_Rejection[dB]": [],
            "RX_Power[dBm]": [],
            "INTERFERE_Power[dBuv]": [],
            "SINAD[dB]": [],
            "Radio_Voltage[V]": [],
            "Temperature[C]": [],
            "Timestamp": [],
            "Test_Passed": [],
        }

        test_result = self.rx_test_executor(looping_arrays=looping_arrays,
                                            test_function=self._rx_spurious_response_rejection,
                                            test_config=test_config)

        self.test_results.save_log()
        self.test_equip.signal_gen_1.rf_power_on = False
        self.test_equip.signal_gen_2.rf_power_on = False

        return test_result


    def _rx_spurious_response_rejection(self, freq, voltage, temp, rx_radio_power, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage

        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.rx_set_power = test_config['sig_gen_1']['power']['start']
            self.transmit_sig_gen_to_radio(rf_freq=freq, rf_power=self.rx_set_power, rf_on=True, fm_dev_on=True,
                                           sql_toggle=1, sig_gen_no=1, audio_vol=1)
            self.first_test_loop = False
        else:
            self.transmit_sig_gen_to_radio(rf_freq=freq, audio_vol=int(test_config['radio_volume']), sig_gen_no=1)

        sinad, self.rx_set_power = self.find_sinad_power(target_sinad=test_config['sinad_target'],
                                                         set_power=self.rx_set_power,
                                                         max_power=test_config['sig_gen_1']['power']['max'],
                                                         min_power=test_config['sig_gen_1']['power']['min'],
                                                         power_step=test_config['sig_gen_1']['power']['step'])


        if not sinad >= test_config['sinad_target']:
            gui.print_red('20dB SINAD Not Reached')
            test_passed = False
            return test_passed

        interference_freq_array = self.array_maker(test_config['sig_gen_2']['frequency'])
        #interference_power_thresh = self.rx_set_power + test_config['spurious_resp_rej_ratio']

        idx = 0

        for interference_freq in interference_freq_array:

            if interference_freq == freq:
                #There's no point checking for interference on the same channel...
                continue
            self.interfere_power = test_config['sig_gen_2']['power']['start']
            self.transmit_sig_gen_to_radio(rf_freq=interference_freq, rf_power=self.interfere_power, rf_on=True,
                                           fm_dev_on=True, sig_gen_no=2)

            sinad = self.test_equip.soundcard.calculate_sinad()

            while sinad < test_config['min_sinad']:

                if sinad < test_config['min_sinad'] and self.interfere_power > test_config['sig_gen_2']['power']['min']:
                    self.interfere_power -= test_config['sig_gen_2']['power']['step']
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)

                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=False,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                if sinad >= (test_config['min_sinad'] +  test_config['soundcard']['sinad_proximity']) and self.interfere_power < test_config['sig_gen_2']['power']['max']:
                    self.interfere_power += test_config['sig_gen_2']['power']['step']
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)
                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=True,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                if sinad >= test_config['min_sinad'] and sinad < test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']:

                    break

            if (self.interfere_power - self.rx_set_power) >= self.rx_set_power + test_config['spurious_resp_rej_ratio']:
                test_passed.append(True)
            else:
                test_passed.append(False)

            print(
                f'RX_Frequency: {freq / 1e6:.3f} MHz, Inter Freq: {interference_freq / 1e6:.3f} MHz, Spurious_Resp_Rejection: '
                f'{self.interfere_power - self.rx_set_power:.2f} dB, SINAD: {sinad:.2f} dB, RX_Power: {self.rx_set_power} dBm, '
                f'INTERFERE_Power[dBm]: {self.interfere_power:.2f} Passed: {test_passed[idx]}')

            date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.test_results.log_dict["RX_Frequency[Hz]"].append(freq)
            self.test_results.log_dict["INTERFERE_Frequency[Hz]"].append(interference_freq)
            self.test_results.log_dict["Spurious_Resp_Rejection[dB]"].append(self.interfere_power - self.rx_set_power)
            self.test_results.log_dict["RX_Power[dBm]"].append(self.rx_set_power)
            self.test_results.log_dict["INTERFERE_Power[dBuv]"].append(self.interfere_power)
            self.test_results.log_dict["SINAD[dB]"].append(sinad)
            self.test_results.log_dict["Radio_Voltage[V]"].append(voltage)
            self.test_results.log_dict["Temperature[C]"].append(temp)
            self.test_results.log_dict["Timestamp"].append(date_time)
            self.test_results.log_dict["Test_Passed"].append(test_passed[idx])

        self.transmit_sig_gen_to_radio(rf_on=False, fm_dev_on=False, sig_gen_no=2)
        if False in test_passed:
            return False
        else:
            return True

    def rx_intermodulation_response(self, test_config_opt):

        test_id = 'rx_intermodulation_response'

        self.test_equip.rf_switch.state_tx_rx = 'RX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.check_radio_serial_comms()
        self.radio_tx_off()
        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        looping_arrays = self.get_looping_arrays(test_config=test_config)
        self.first_test_loop = True

        self.test_equip.soundcard.num_samples = test_config['soundcard']['no_samples']
        self.test_equip.soundcard.psophometric_weighting = test_config['soundcard']['psophometric_weighting']

        self.transmit_sig_gen_to_radio(
            rf_power_units=test_config['sig_gen_1']['power']['units'],
            lfo_freq=test_config['sig_gen_1']['lfo_frequency'],
            fm_dev=test_config['sig_gen_1']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False, sig_gen_no=1)

        self.transmit_sig_gen_to_radio(
            rf_power_units=test_config['sig_gen_2']['power']['units'],
            lfo_on=False, rf_on=False, fm_dev_on=False, sig_gen_no=2)


        self.transmit_sig_gen_to_radio(
            rf_power_units=test_config['sig_gen_3']['power']['units'],
            lfo_freq=test_config['sig_gen_3']['lfo_frequency'],
            fm_dev=test_config['sig_gen_3']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False, sig_gen_no=3)

        self.test_equip.signal_gen_1.fm_dev_on = True

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.test_results.log_dict = {
            "RX_Frequency[Hz]": [],
            "Interfere_Frequency_B[Hz]": [],
            "Interfere_Frequency_C[Hz]": [],
            "Interfere_Power_B[dBm]": [],
            "Interfere_Power_C[dBm]": [],
            "Intermod_Resp[dB]": [],
            "RX_Power[dBm]": [],
            "SINAD[dB]": [],
            "Radio_Voltage[V]": [],
            "Temperature[C]": [],
            "Timestamp": [],
            "Test_Passed": [],
        }

        test_result = self.rx_test_executor(looping_arrays=looping_arrays,
                                            test_function=self._rx_intermodulation_response,
                                            test_config=test_config)

        self.test_results.save_log()
        self.test_equip.signal_gen_1.rf_power_on = False
        self.test_equip.signal_gen_2.rf_power_on = False
        self.test_equip.signal_gen_3.rf_power_on = False

        return test_result

    def _rx_intermodulation_response(self, freq, voltage, temp, rx_radio_power, test_config):
        test_passed = []
        self.test_equip.psu.voltage = voltage

        if temp != 'NOT_USED':
            gui.print_yellow('[Notionally] Setting Temp to ' + str(temp))

        if self.first_test_loop:
            self.rx_set_power = test_config['sig_gen_1']['power']['start']
            self.transmit_sig_gen_to_radio(rf_freq=freq, rf_power=self.rx_set_power, rf_on=True, fm_dev_on=True,
                                           sql_toggle=1, audio_vol=1, sig_gen_no=1)


            self.first_test_loop = False
        else:
            self.transmit_sig_gen_to_radio(rf_freq=freq, audio_vol=int(test_config['radio_volume']), sig_gen_no=1)

        sinad, self.rx_set_power = self.find_sinad_power(target_sinad=test_config['sinad_target'],
                                                         set_power=self.rx_set_power,
                                                         max_power=test_config['sig_gen_1']['power']['max'],
                                                         min_power=test_config['sig_gen_1']['power']['min'],
                                                         power_step=test_config['sig_gen_1']['power']['step'])

        if not sinad >= test_config['sinad_target']:
            gui.print_red('20dB SINAD Not Reached')
            test_passed = False
            return test_passed

        #interference_power_thresh = self.rx_set_power + test_config['intermod_resp_ratio']

        for idx in range(len(test_config['sig_gen_2']['interference_offset'])):
            interference_freq_b = freq + float(test_config['sig_gen_2']['interference_offset'][idx])
            interference_freq_c = freq + float(test_config['sig_gen_3']['interference_offset'][idx])

            self.interfere_power = test_config['sig_gen_2']['power']['start']

            self.transmit_sig_gen_to_radio(rf_freq=interference_freq_b, rf_power=self.interfere_power, rf_on=True, sig_gen_no=2)
            self.transmit_sig_gen_to_radio(rf_freq=interference_freq_c, lfo_freq=test_config['sig_gen_3']['lfo_frequency'],
                                           fm_dev=test_config['sig_gen_3']['fm_dev'], rf_power=self.interfere_power, rf_on=True, fm_dev_on=True, sig_gen_no=3)

            while sinad >= test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']:

                sinad = self.test_equip.soundcard.calculate_sinad()
                self.interfere_power += test_config['sig_gen_2']['power']['step']
                self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)
                self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=3)

            sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=False,
                                          max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                          num_measurements=test_config['soundcard']['sinad_no_readings'])

            while (sinad <= test_config['min_sinad']) or (sinad >= test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']):

            #while test_config['min_sinad'] - test_config['soundcard']['sinad_proximity'] >= sinad >= test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']:

                if sinad < test_config['min_sinad'] and self.interfere_power > test_config['sig_gen_2']['power']['min']:
                    self.interfere_power -= test_config['sig_gen_2']['power']['step']

                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=3)

                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=False,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                if sinad >= (test_config['min_sinad'] +  test_config['soundcard']['sinad_proximity']) and self.interfere_power < test_config['sig_gen_2']['power']['max']:
                    self.interfere_power += test_config['sig_gen_2']['power']['step']
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=2)
                    self.transmit_sig_gen_to_radio(rf_power=self.interfere_power, sig_gen_no=3)

                    sinad = self.get_stable_sinad(threshold=test_config['sinad_target'], order_descending=True,
                                                  max_fluctuation=test_config['soundcard']['sinad_max_fluctuation'],
                                                  num_measurements=test_config['soundcard']['sinad_no_readings'])

                if sinad >= test_config['min_sinad'] and sinad < test_config['min_sinad'] + test_config['soundcard']['sinad_proximity']:

                    break

            if (self.interfere_power - self.rx_set_power) >= test_config['intermod_resp_ratio']:
                test_passed.append(True)
            else:
                test_passed.append(False)

            print(
                f'RX_Frequency: {freq / 1e6:.3f} MHz, Inter Freq B: {interference_freq_b / 1e6:.3f} MHz, '
                f'Inter Freq C: {interference_freq_c / 1e6:.3f} MHz, Intermod_Resp_Ratio: '
                f'{self.interfere_power - self.rx_set_power:.2f} dB, SINAD: {sinad:.2f} dB, RX_Power: {self.rx_set_power} dBm, '
                f'INTERFERE_Power[dBm]: {self.interfere_power:.2f} Passed: {test_passed[idx]}')

            date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.test_results.log_dict["RX_Frequency[Hz]"].append(freq)
            self.test_results.log_dict["Interfere_Frequency_B[Hz]"].append(interference_freq_b)
            self.test_results.log_dict["Interfere_Frequency_C[Hz]"].append(interference_freq_c)
            self.test_results.log_dict["Interfere_Power_B[dBm]"].append(self.interfere_power)
            self.test_results.log_dict["Interfere_Power_C[dBm]"].append(self.interfere_power)
            self.test_results.log_dict["Intermod_Resp[dB]"].append(self.interfere_power - self.rx_set_power)
            self.test_results.log_dict["RX_Power[dBm]"].append(self.rx_set_power)
            self.test_results.log_dict["SINAD[dB]"].append(sinad)
            self.test_results.log_dict["Radio_Voltage[V]"].append(voltage)
            self.test_results.log_dict["Temperature[C]"].append(temp)
            self.test_results.log_dict["Timestamp"].append(date_time)
            self.test_results.log_dict["Test_Passed"].append(test_passed[idx])

        # self.transmit_sig_gen_to_radio(rf_on=False, fm_dev_on=False, sig_gen_no=1)
        self.transmit_sig_gen_to_radio(rf_on=False, fm_dev_on=False, sig_gen_no=2)
        self.transmit_sig_gen_to_radio(rf_on=False, fm_dev_on=False, sig_gen_no=3)
        if False in test_passed:
            return False
        else:
            return True

    def rx_blocking_desensitization(self, test_config_opt):
        test_id = 'rx_blocking_desensitization'

        self.test_equip.rf_switch.state_tx_rx = 'RX'

        self.test_results.create_test_results_path(standards_id=self.standard_id, test_id=test_id)

        self.check_radio_serial_comms()
        self.radio_tx_off()
        test_config = self.get_test_config(test_config_opt=test_config_opt, test_id=test_id)
        self.test_results.test_param_log(test_config, test_config_opt)

        looping_arrays = self.get_looping_arrays(test_config=test_config)
        self.first_test_loop = True

        self.test_equip.soundcard.num_samples = test_config['soundcard']['no_samples']
        self.test_equip.soundcard.psophometric_weighting = test_config['soundcard']['psophometric_weighting']

        self.test_equip.signal_gen_1.transmit_from_sig_gen(
            rf_power_units=test_config['sig_gen_1']['power']['units'],
            lfo_freq=test_config['sig_gen_1']['lfo_frequency'],
            fm_dev=test_config['sig_gen_1']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False)

        self.test_equip.signal_gen_2.transmit_from_sig_gen(
            rf_power_units=test_config['sig_gen_2']['power']['units'],
            lfo_on=False, rf_on=False, fm_dev_on=False)

        self.test_equip.signal_gen_3.transmit_from_sig_gen(
            rf_power_units=test_config['sig_gen_3']['power']['units'],
            lfo_freq=test_config['sig_gen_3']['lfo_frequency'],
            fm_dev=test_config['sig_gen_3']['fm_dev'],
            lfo_on=False, rf_on=False, fm_dev_on=False)

        date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.test_results.log_dict = {
            "RX_Frequency[Hz]": [],
            "Interfere_Frequency_B[Hz]": [],
            "Interfere_Frequency_C[Hz]": [],
            "Interfere_Power_B[dBm]": [],
            "Interfere_Power_C[dBm]": [],
            "Intermod_Resp[dB]": [],
            "RX_Power[dBm]": [],
            "SINAD[dB]": [],
            "Radio_Voltage[V]": [],
            "Temperature[C]": [],
            "Timestamp": [],
            "Test_Passed": [],
        }

        test_result = self.rx_test_executor(looping_arrays=looping_arrays,
                                            test_function=self._rx_intermodulation_response,
                                            test_config=test_config)

        self.test_results.save_log()
        self.test_equip.signal_gen_1.rf_power_on = False
        self.test_equip.signal_gen_2.rf_power_on = False
        self.test_equip.signal_gen_3.rf_power_on = False

        return test_result


    def rx_spurious_emissions(self):
        pass

    def rx_receiver_radiated_spurious_emissions(self):
        pass

    def rx_receiver_residual_noise_level(self):
        pass

    def rx_squelch_operation(self):
        pass

    def rx_squelch_hysteresis(self):
        pass

    def rx_multiple_watch_characteristic(self):
        pass

    def rx_receiver_dynamic_range(self):
        pass
