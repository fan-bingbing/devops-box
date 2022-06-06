from contextlib import contextmanager
import time
import pyvisa


@contextmanager # so in open_resource object it has __enter__() magic function now
def open_siggen_resource(address):
    rm = pyvisa.ResourceManager('@py')
    try:
        inst = rm.open_resource(address)
        yield inst
    finally:
        inst.close()


def generate_test_sig():
    with open_siggen_resource('TCPIP0::10.0.22.83::inst0::INSTR') as r:
        print(r.query("*IDN?"))
        r.write(f"*RST") # write all paramaters to SigGen
        r.write("SYST:DISP:UPD ON")
        r.write(f"FREQ 400MHz")
        r.write(f":UNIT:POW dBm")
        r.write(f":POW -53dBm")
        r.write(":OUTP1 ON")
        #time.sleep(int(dur))
        #r.write(":OUTP1 OFF")
        return r


def stop_test_sig():
    with open_siggen_resource('TCPIP0::10.0.22.83::inst0::INSTR') as r:
        r.write(":OUTP1 OFF")
