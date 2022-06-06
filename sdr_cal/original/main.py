import uhd
import numpy as np
import time
import struct
import matplotlib.pyplot as plt
from scipy import signal
import math

from config import *
from cal import *


def print_w_timestamp(s):
    milli_sec = int(round(time.time() * 1000)) % 1000
    print(time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '-' + str(milli_sec) + ': ' + str(s))
    return


class rf_receiver:
    def __init__(self, rx_freq, samp_rate, num_samps):
        for i in range(4):  # try maximum 4 times in case n200 is booting
            try:
                self.usrp = uhd.usrp.MultiUSRP(usrp_ip)
            except:
                raise Exception('Failed to find N200 transceiver')

        self.rx_gain = 30
        self.channel = 0
        self.samp_rate = samp_rate
        self.rx_freq = 400.01e6#rx_freq
        self.rx_bw = 100e3

        self.usrp.set_rx_antenna("TX/RX")
        self.usrp.set_rx_rate(self.samp_rate, self.channel)
        self.usrp.set_rx_gain(self.rx_gain, self.channel)
        self.st_args = uhd.usrp.StreamArgs("sc16", "sc16")
        self.st_args.channels = [self.channel]

        self.usrp.set_rx_freq(uhd.types.TuneRequest(self.rx_freq), self.channel)
        self.rx_streamer = self.usrp.get_rx_stream(self.st_args)
        self.rx_max_samps = self.rx_streamer.get_max_num_samps()
        print("UHD max_num_samps %d" % self.rx_max_samps)

        self.rx_metadata = uhd.types.RXMetadata()
        self.rx_result = np.empty((1, num_samps), dtype=np.int32)

        self.rx_buffer = np.empty((1, self.rx_max_samps * 5), dtype=np.int32)

        if usrp_gpsdo_available:
            gtime = self.usrp.get_mboard_sensor("gps_time")
            print(gtime)
            glocked = self.usrp.get_mboard_sensor("gps_locked")
            print(glocked)

        if usrp_use_external_reference:
            self.usrp.set_clock_source("external")

        print(self.usrp.get_clock_source(0))

    def get_rx_samps(self, num_samps, ret_val='infile'):
        rx_samps = 0

        # discard previous packets if any (flushing)
        samps = 1
        while samps > 0:
            samps = self.rx_streamer.recv(self.rx_buffer, self.rx_metadata)

        # start streaming
        print_w_timestamp("Waiting for signal")
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = True
        stream_cmd.num_samps = self.rx_max_samps * 5
        self.rx_streamer.issue_stream_cmd(stream_cmd)
        # discard the first packet (sdr stabilising)
        self.rx_streamer.recv(self.rx_buffer, self.rx_metadata)

        self.waiting_for_burst = True
        self.start_to_capture = False

        while self.waiting_for_burst:
            samples = self.rx_streamer.recv(self.rx_buffer, self.rx_metadata)
            if self.rx_metadata.error_code != uhd.types.RXMetadataErrorCode.none:
                print('get_rx_samps: ' + self.rx_metadata.strerror())

            if samples > 0:
                for dat in self.rx_buffer[0]:
                    i = np.int16(dat & 0xFFFF)
                    # print(i, end='')
                    if i >= capture_threshold:
                        # print_w_timestamp("Signal detected!")

                        self.start_to_capture = True
                        self.waiting_for_burst = False

                        t = time.localtime()
                        milli_sec = int(round(time.time() * 1000)) % 1000
                        timestamp = time.strftime('%Y%m%d-%H%M%S', t)
                        des_file = 'USRP_' + timestamp + '-' + str(milli_sec) + '.dat'
                        if ret_val == 'infile':
                            fh = open(des_file, "wb")
                        break

        while self.start_to_capture:
            while rx_samps < num_samps:
                samples = self.rx_streamer.recv(self.rx_buffer, self.rx_metadata)
                if self.rx_metadata.error_code != uhd.types.RXMetadataErrorCode.none:
                    print('get_rx_samps: ' + self.rx_metadata.strerror())
                    print(des_file)
                    print("Rx samples: %d" % rx_samps)

                if samples > 0:
                    samps = min(num_samps - rx_samps, samples)

                    if ret_val == 'infile':
                        fh.write(self.rx_buffer[:, 0:samps])
                    else:
                        self.rx_result[:, rx_samps:rx_samps + samps] = self.rx_buffer[:, 0:samps]
                    rx_samps += samps

            # stop streaming
            self.start_to_capture = False
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            self.rx_streamer.issue_stream_cmd(stream_cmd)

        if ret_val == 'infile':
            fh.close()
            retdat = []
        else:
            retdat = self.rx_result

        return des_file, retdat


    def get_rx_power_raw(self, num_samps):
        samples = self.get_rx_samps(num_samps)[0, :]
        if samples is None:
            return np.nan
        return 10 * np.log10(np.sum(samples.real ** 2 + samples.imag ** 2) / len(samples) + 1e-10)

    def get_rx_power_cal(self):
        index = int(self.rx_freq / 1e6) - cal_freq_min_mhz
        return rx_power_cal[index]

    def get_rx_power(self):
        return self.get_rx_power_raw() + self.get_rx_power_cal() + rf_attenuator.attenuation


def calculate_carrier_freq(z, samp_rate):
    #print_w_timestamp("calculate_carrier_freq start")

    chk_thd = True
    blen = len(z)
    z_win = z
    amplitude = np.average(np.absolute(z_win))

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
    return freq_offset, amplitude


def read_iq_from_file(file, highfreq, filter_ena=False, deci_ena=False):
    with open(file, "rb") as fh:
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

    # plt.plot(x1)
    # plt.plot(y1)
    # plt.plot(np.absolute(z))
    # plt.show()
    return z


def read_iq_from_data(iq_captured, highfreq, filter_ena=False, deci_ena=False):
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

    # plt.plot(x1)
    # plt.plot(y1)
    # plt.plot(np.absolute(z))
    # plt.show()
    return z


if __name__ == '__main__':
    '''
    Init
    '''
    total_samples = int(samp_rate * rx_duration)

    '''
    Init USRP receiver
    '''
    rx = rf_receiver(centre_freq, samp_rate, total_samples)
    print_w_timestamp("Starting to capture at %d sampling rate" % samp_rate)

    generate_test_sig()
    for freq_cnt in range(total_to_measure):
        #print("\nBurst counter: %d" % freq_cnt)
        if pass_data_in_file:
            filename, iq_complex = rx.get_rx_samps(total_samples, ret_val='infile')
            #print_w_timestamp(filename)
            if filename is None:
                break

            z = read_iq_from_file(filename, cutoff, filter_ena=first_filter_iq, deci_ena=first_decimate_iq)
        else:
            filename, iq_complex = rx.get_rx_samps(total_samples, ret_val='indata')
            #print_w_timestamp(filename)
            if filename is None:
                break

            z = read_iq_from_data(iq_complex, cutoff, filter_ena=first_filter_iq, deci_ena=first_decimate_iq)

            relative_power = 10 * np.log10(np.sum(z.real ** 2 + z.imag ** 2) / len(z))
            print(relative_power)

        #print_w_timestamp("Read data, Filter is %s, Decimate is %s" % (first_filter_iq, first_decimate_iq))

        if first_decimate_iq:
            rate = samp_rate / decimation_factor
        else:
            rate = samp_rate
        freq_oft, amp = calculate_carrier_freq(z, rate)
        print_w_timestamp("Test %d, Freq offset %.4f, Amplitude %d" % (freq_cnt, freq_oft, amp))


    stop_test_sig()
