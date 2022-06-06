
# USRP setup
usrp_ip = 'addr=10.0.22.190'
usrp_gpsdo_available = False
usrp_use_external_reference = True

# Overall
centre_freq = 400e6
samp_rate = 320e3  # Note, minimum sampling rate on N200 is 200ksps
total_to_measure = 3

# Capture
pass_data_in_file = False #True
capture_threshold = 500  # -18dbm input signal
rx_duration = 0.05

# Data pre-process
cutoff = 4000
decimation_factor = 5

first_filter_iq = False
first_decimate_iq = False
