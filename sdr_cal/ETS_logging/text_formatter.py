'''
Not really GUI, just text based UI.

Documentation: http://wiki.gme.net.au/display/PDLC/CX50+Manufacturing+Software

Copyright (C) 2018 Standard Communications Pty Ltd (GME). All rights reserved.
'''

import time
import os

import time, sys
# import msvcrt

# from termios import tcflush, TCIFLUSH (termios is a Linux package)

# text colours

text_red = '\033[91m'
text_green = '\033[92m'
text_yellow = '\033[93m'
text_reset = '\033[0m'


def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())


def print_red(msg):
    print(text_red + msg + text_reset)


def print_green(msg):
    print(text_green + msg + text_reset)


def print_yellow(msg):
    print(text_yellow + msg + text_reset)


def my_input(msg):
    # while msvcrt.kbhit():
    #     msvcrt.getch()
    # tcflush(sys.stdin, TCIFLUSH)
    print(text_yellow + msg + text_reset, end=' ')
    return input()


def message(msg):
    my_input(msg)


def question(msg):
    while msvcrt.kbhit():
        msvcrt.getch()
    ans = my_input(msg + ' [y/n]').lower()
    while True:
        if ans in ('y', ""):
            return True
        elif ans == 'n':
            return False
        else:
            ans = my_input("Please respond with 'y' or 'n':").lower()


# A trivial container for test results
class TestResults:
    def __init__(self, log_path):
        self.passed = True
        self.passed_before = False
        self.unique_id = 'unknown_id'
        self.failure_report_message = None
        self.log_path = log_path
        self.log_list = []
        self.new_sn_allocated = False
        self.radio_model = None
        self._serial_no = ''
        self.serial_no_wk_old = ''
        self._test_id = None
        self._fail_id = None
        self._test_status = None
        self._test_info = []

    @property
    def serial_no(self):
        return self._serial_no

    # @serial_no.setter
    # def serial_no(self, serial_no):
    #     self._serial_no = serial_no
    #
    def add_serial_no(self, serial_no, is_newly_allocated=False):
        if is_newly_allocated:
            self.new_sn_allocated = True
        self._serial_no = serial_no

    @property
    def test_id(self):
        return self._test_id

    @test_id.setter
    def test_id(self, test_id):
        self._test_id = test_id

    @property
    def fail_id(self):
        return self._fail_id

    @fail_id.setter
    def fail_id(self, fail_id):
        self._fail_id = fail_id

    @property
    def test_status(self):
        return self._test_status

    @test_status.setter
    def test_status(self, test_status):
        self._test_status = test_status
        self.add_line()

    @property
    def test_info(self):
        return self._test_info

    @test_info.setter
    def test_info(self, test_info):
        self._test_info = test_info

    def fail_line(self, line, to_print=True):
        if to_print:
            fail_reason = line
            print_red(fail_reason)
        self.log_list.append(line)

    def add_line(self, line, to_print=True, colour='w'):
        if to_print:
            if colour == 'w':
                print(line)
            elif colour == 'r':
                print_red(line)
            elif colour == 'g':
                print_green(line)
            elif colour == 'y':
                print_yellow(line)
        self.log_list.append(line)

    def save_log(self):

        print_green('saving log')

        # Need to figure out how we'll store all the files etc...
        filename = '%s/%s_%s.log' % (self.log_path, self.serial_no, self.unique_id)
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create the directories if required
        with open(filename, 'a+') as f:
            for item in self.log_list:
                f.write(item + '\n')
            f.write('\n')  # add a blank line at the end

        if self.serial_no is not '':
            with open(self.log_path + '/last_sn_tested.log', 'a+') as h:
                h.write(self.radio_model + ',' + self.serial_no + '\n')

            if self.new_sn_allocated:
                with open(self.log_path + '/sn_allocation_log.log', 'a+') as h:
                    h.write(self.radio_model + ',' + self.serial_no + '\n')
            else:
                print('Note: No New Serial Number Allocated')

            if self.serial_no_wk_old is not '':
                # print('Saving Old/New WK SN Log...')
                with open(self.log_path + '/new_gme_sn_replace_wk.log', 'a+') as h:
                    h.write(self.radio_model + ',' + self.serial_no_wk_old + ',' + self.serial_no + '\n')
            # else:
            #     print('Not Saving Old/New WK SN Log...')


        elif self.serial_no is '':
            with open(self.log_path + '/last_sn_tested.log', 'a+') as h:
                h.write(self.radio_model + ',' + '[NO_SERIAL_NUMBER]' + '\n')


if __name__ == '__main__':
    # unit test
    print_red('Red')
    print_green('Green')
    print_yellow('Yellow')
    # if question('Question?'):
    #     print_green('Yes')
    # else:
    #     print_red('No')
