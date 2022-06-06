import yaml
import sys

from test_methods.cal_std import Cal_Std
from ETS_logging.log_generator import Logging
import ETS_logging.text_formatter as gui

header = """
GME SDR Calibration Version 1.0
"""

equipment = """
Check equipment ip address, set ip in yaml files:
./config/run_config.yaml
./config/beacon_sdr_cal/beacon_sdr_cal.yaml
"""

with open('config/run_config.yaml', "r") as file_descriptor:
    run_config = yaml.load(file_descriptor, Loader=yaml.FullLoader)


run_test = run_config['run_test']

test_results = Logging(log_path=run_config['log_path'], run_test=run_test)

test_results.test_setup_log(equip_config=run_config)


def main():
    print("--------------------------------------------")
    print(header)
    print("--------------------------------------------")
    print("--------------------------------------------")
    print(equipment)
    print("--------------------------------------------")
    print("1. Verify Signal Level")
    print("2. Run Cal on Defined Frequency Band ")
    print("3. Run Cal on Beacon Freqencies")
    print("0. Quit")

    while True:
        choice = input("> ")
        if choice == "1":

            while True:
                print("1. Connet Coxial cable (SN:1849) from Siggen to SpecAn")
                print("2. Go back to previous menu")
                choice = input("> ")
                if choice == "1":
                    cal_test.test_executor(verify_level=True)
                elif choice == "2":
                    break
                else:
                    print("Enter integer number 1 or 2 to choose what to do.")
            main()

        elif choice == "2":

            while True:
                print("1. Connet Coxial cable (SN:1849) from Siggen to SDR RF port1")
                print("2. Go back to previous menu")
                choice = input("> ")
                if choice == "1":
                    cal_test.test_executor(verify_level=False)
                elif choice == "2":
                    break
                else:
                    print("Enter integer number 1 or 2 to choose what to do.")

            main()

        elif choice == "3":
            while True:
                print("1. Connet Coxial cable (SN:1849) from Siggen to SDR RF port1")
                print("2. Go back to previous menu")
                choice = input("> ")
                if choice == "1":
                    cal_test.beacon_sdr_test()
                elif choice == "2":
                    break
                else:
                    print("Enter integer number 1 or 2 to choose what to do.")
            main()

        elif choice == "0":
            exit(0)

        else:
            print("Enter integer number 0 to 3 to choose what to do.")


if __name__ == "__main__":
    cal_test = Cal_Std(test_results=test_results)
    main()













#
# radio_test = RunRadioTests(radio_select=radio_select, radio_addr=radio_eeprom, test_equip=test_equip,
#                                         equip_config=equip_config, radio_const=radio_param,
#                                         radio_ctrl=radio_control, test_to_run=test_group, test_results=test_results)
