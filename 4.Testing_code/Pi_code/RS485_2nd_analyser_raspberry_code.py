import minimalmodbus
import time
import struct
import json
import requests
combined_data = 0.0
flow_data = 0.0
cod = 0.0
bod = 0.0
tss = 0.0
ph = 0.0

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument1 = minimalmodbus.Instrument('/dev/ttyUSB0', 2)

def setup_instrument(instrument):
    instrument.serial.baudrate = 9600      
    instrument.serial.bytesize = 8
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 1          
    instrument.mode = minimalmodbus.MODE_RTU  
    instrument.clear_buffers_before_each_transaction = True
    instrument.debug = True

def read_combined_data(instrument):
    try:
        response = instrument.read_registers(0, 10, 3)
        combined_data=(response[3] << 16) | response[2]
        combined_data = combined_data * 0.1
        flow_data= response[1] * 0.01
        return combined_data, flow_data
    except minimalmodbus.NoResponseError:
        print("No response from the instrument. Reytying...")
        return None, None
    
def read_and_process_instrument1_data(instrument1):
    try:
        reg0 = instrument.read_register(0, 0, 3)
        reg1 = instrument.read_register(1, 0, 3)
        regset1 = hex((reg1<<16) | reg0)[2:]
        regset1_str = str(regset1)
        f_cod = struct.unpack('>f', bytes.fromhex(regset1_str))[0]
        cod = round(f_cod, 2)
        ############################################
        reg2 = instrument.read_register(2, 0, 3)
        reg3 = instrument.read_register(3, 0, 3)
        regset2 = hex((reg3<<16) | reg2)[2:]
        regset2_str = str(regset2)
        f_bod = struct.unpack('>f', bytes.fromhex(regset2_str))[0]
        bod = round(f_bod, 2)
        ############################################
        reg4 = instrument.read_register(4, 0, 3)
        reg5 = instrument.read_register(5, 0, 3)
        regset3 = hex((reg5<<16) | reg4)[2:]
        regset3_str = str(regset3)
        f_tss = struct.unpack('>f', bytes.fromhex(regset3_str))[0]
        tss = round(f_tss, 2)
        ############################################
        reg6 = instrument.read_register(6, 0, 3)
        reg7 = instrument.read_register(7, 0, 3)
        regset4 = hex((reg7<<16) | reg6)[2:]
        regset4_str = str(regset4)
        f_ph = struct.unpack('>f', bytes.fromhex(regset4_str))[0]
        ph = round(f_ph, 2)
        print("The COD Value is ", cod)
        print("The BOD Value is ", bod)
        print("The TSS Value is ", tss)
        print("The pH Value is ", ph)
        print("The FM1 TOT Value is ", combined_data)
        print("The FM1 FLOW Value is ", flow_data)
        
    except Exception as e:
        print("an error occurred:", str(e))
while True:
    setup_instrument(instrument)
    setup_instrument(instrument1)
    combined_data, flow_data = read_combined_data(instrument)
    read_and_process_instrument1_data(instrument1)
    
    
    instrument.serial.close()
    instrument1.serial.close()
        
    cod_data = "http://localhost/push/push.php?id=cod&cod={}".format(cod)
    bod_data = "http://localhost/push/push.php?id=bod&bod={}".format(bod)
    tss_data = "http://localhost/push/push.php?id=tss&tss={}".format(tss)
    ph_data = "http://localhost/push/push.php?id=ph&ph={}".format(ph)
    #fm1_data = "http://localhost/push/push.php?id=fm1&fmid1=001&tot1={}&flow1={}".format(tot1,flow1)
    #fm2_data = "http://localhost/push/push.php?id=fm2&fmid2=002&tot2={}&flow2={}".format(tot2,flow2)
    update_cod_api = requests.get(cod_data)
    update_bod_api = requests.get(bod_data)
    update_tss_api = requests.get(tss_data)
    update_ph_api = requests.get(ph_data)
    #update_fm1_api = requests.get(fm1_data)
    #update_fm2_api = requests.get(fm2_data)
    print(cod_data)
    print(update_cod_api.status_code)
    print(bod_data)
    print(update_bod_api.status_code)
    print(tss_data)
    print(update_tss_api.status_code)
    print(ph_data)
    print(update_ph_api.status_code)
    #print(fm1_data)
    #print(update_fm1_api.status_code)
    #print(fm2_data)
    #print(update_fm2_api.status_code)
    time.sleep(5)