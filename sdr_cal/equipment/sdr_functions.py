import uhd
import yaml
import numpy as np
import time
import struct
# import matplotlib.pyplot as plt
from scipy import signal
import math

# from config import *
# from cal import *

#
# def print_w_timestamp(s):
#     milli_sec = int(round(time.time() * 1000)) % 1000
#     print(time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '-' + str(milli_sec) + ': ' + str(s))
#     return


class RF_ReceiVer():
    def __init__(self, samp_rate, num_samps, usrp_ip):
        for i in range(4):  # try maximum 4 times in case n200 is booting
            try:
                self.usrp = uhd.usrp.MultiUSRP(usrp_ip)
            except:
                raise Exception('Failed to find N200 transceiver')

        with open('config/beacon_sdr_cal/beacon_sdr_cal.yaml', "r") as file_descriptor:
            self.beacon_sdr_cal = yaml.load(file_descriptor, Loader=yaml.FullLoader)

        self.usrp_setup = self.beacon_sdr_cal['usrp_setup']
        self.test_attribute = self.beacon_sdr_cal['test_attribute']


        self.rx_gain = self.usrp_setup['rx_gain']
        self.channel = self.usrp_setup['channel']
        self.samp_rate = samp_rate

        self.rx_bw = float(self.usrp_setup['rx_bw'])
        self.gpsdo_available = self.usrp_setup['gpsdo_available']
        self.use_external_reference = self.usrp_setup['use_external_reference']
        self.capture_threshold = self.test_attribute['capture_threshold']


        self.usrp.set_rx_antenna("TX/RX")
        self.usrp.set_rx_rate(self.samp_rate, self.channel)
        self.usrp.set_rx_gain(self.rx_gain, self.channel)
        self.st_args = uhd.usrp.StreamArgs("sc16", "sc16")
        self.st_args.channels = [self.channel]


        self.rx_streamer = self.usrp.get_rx_stream(self.st_args)
        self.rx_max_samps = self.rx_streamer.get_max_num_samps()
        print("UHD max_num_samps %d" % self.rx_max_samps)

        self.rx_metadata = uhd.types.RXMetadata()
        self.rx_result = np.empty((1, num_samps), dtype=np.int32)
        self.rx_buffer = np.empty((1, self.rx_max_samps * 5), dtype=np.int32)

        if self.gpsdo_available:
            gtime = self.usrp.get_mboard_sensor("gps_time")
            print(gtime)
            glocked = self.usrp.get_mboard_sensor("gps_locked")
            print(glocked)

        if self.use_external_reference:
            self.usrp.set_clock_source("external")

        print(self.usrp.get_clock_source(0))

    def set_rx_freq(self, freq):
        self.usrp.set_rx_freq(uhd.types.TuneRequest(freq), self.channel)


    def get_rx_samps(self, path, num_samps, ret_val='infile'):
        rx_samps = 0

        # discard previous packets if any (flushing)
        samps = 1
        while samps > 0:
            samps = self.rx_streamer.recv(self.rx_buffer, self.rx_metadata)

        # start streaming
        # print_w_timestamp("Waiting for signal")
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
                    #print(i, end='')
                    if i >= self.capture_threshold:
                        #print_w_timestamp("Signal detected!")

                        self.start_to_capture = True
                        self.waiting_for_burst = False

                        t = time.localtime()
                        milli_sec = int(round(time.time() * 1000)) % 1000
                        timestamp = time.strftime('%Y%m%d-%H%M%S', t)
                        des_file = 'USRP_' + timestamp + '-' + str(milli_sec) + '.dat'
                        if ret_val == 'infile':
                            fh = open(path + "/" + des_file, "wb")
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
