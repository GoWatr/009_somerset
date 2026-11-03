import minimalmodbus
import time
import struct
#import json
import requests
FM1reg = 0.0
FM1tot = 0.0
FM1flow = 0.0

FM2reg = 0.0
FM2tot = 0.0
FM2flow = 0.0

FM3reg = 0.0
FM3tot = 0.0
FM3flow = 0.0

# port name, slave address (in decimal)
instrument1 = minimalmodbus.Instrument('COM7', 1)

instrument1.serial.baudrate = 9600      
instrument1.serial.bytesize = 8
instrument1.serial.stopbits = 1
instrument1.serial.timeout  = 1          
instrument1.mode = minimalmodbus.MODE_RTU  
instrument1.clear_buffers_before_each_transaction = True
instrument1.debug = True

instrument2 = minimalmodbus.Instrument('COM7', 2)
instrument2.serial.baudrate = 9600      
instrument2.serial.bytesize = 8
instrument2.serial.stopbits = 1
instrument2.serial.timeout  = 1          
instrument2.mode = minimalmodbus.MODE_RTU  
instrument2.clear_buffers_before_each_transaction = True
instrument2.debug = True

instrument3 = minimalmodbus.Instrument('COM7', 3)
instrument3.serial.baudrate = 9600      
instrument3.serial.bytesize = 8
instrument3.serial.stopbits = 1
instrument3.serial.timeout  = 1          
instrument3.mode = minimalmodbus.MODE_RTU  
instrument3.clear_buffers_before_each_transaction = True
instrument3.debug = True

instrument4 = minimalmodbus.Instrument('COM7', 4)
instrument4.serial.baudrate = 9600      
instrument4.serial.bytesize = 8
instrument4.serial.stopbits = 1
instrument4.serial.timeout  = 1          
instrument4.mode = minimalmodbus.MODE_RTU  
instrument4.clear_buffers_before_each_transaction = True
instrument4.debug = True
while True:
    # Register number, number of decimals, function code
    # not sure what to expect on number of register, is it 31004, 31005?
    try:
        FM1reg = instrument2.read_registers(0, 10, 3)
        FM1tot = (FM1reg[3] << 16) | FM1reg[2]
        FM1tot = FM1tot * 0.1
        FM1flow = FM1reg[1] * 0.01
        
        
        #FM2reg = instrument3.read_registers(0, 10, 3)
        #FM2tot = (FM1reg[3] << 16) | FM1reg[2]
        #FM2flow = instrument3.read_registers(1, 10, 3)
        
        #FM3reg = instrument4.read_registers(0, 10, 3)
        #FM3tot = (FM1reg[3] << 16) | FM1reg[2]
        #FM3flow = instrument4.read_registers(1, 10, 3)
        
        reg0 = instrument1.read_register(0, 0, 3)
        reg1 = instrument1.read_register(1, 0, 3)
        regset1 = hex((reg1<<16) | reg0)[2:]
        regset1_str = str(regset1)
        f_cod = struct.unpack('>f', bytes.fromhex(regset1_str))[0]
        cod = round(f_cod, 2)
        ############################################
        reg2 = instrument1.read_register(2, 0, 3)
        reg3 = instrument1.read_register(3, 0, 3)
        regset2 = hex((reg3<<16) | reg2)[2:]
        regset2_str = str(regset2)
        f_bod = struct.unpack('>f', bytes.fromhex(regset2_str))[0]
        bod = round(f_bod, 2)
        ############################################
        reg4 = instrument1.read_register(4, 0, 3)
        reg5 = instrument1.read_register(5, 0, 3)
        regset3 = hex((reg5<<16) | reg4)[2:]
        regset3_str = str(regset3)
        f_tss = struct.unpack('>f', bytes.fromhex(regset3_str))[0]
        tss = round(f_tss, 2)
        ############################################
        reg6 = instrument1.read_register(6, 0, 3)
        reg7 = instrument1.read_register(7, 0, 3)
        regset4 = hex((reg7<<16) | reg6)[2:]
        regset4_str = str(regset4)
        f_ph = struct.unpack('>f', bytes.fromhex(regset4_str))[0]
        ph = round(f_ph, 2)
        
        
        print("The COD Value is ", cod)
        print("The BOD Value is ", bod)
        print("The TSS Value is ", tss)
        print("The pH Value is ", ph)
        print("Flow meter-IN", "tot=", FM1tot, "flow", FM1flow)
        time.sleep(2)
        #instrument.serial.close()
        
        cod_data = "http://localhost/push/push.php?id=cod&cod={}".format(cod)
        bod_data = "http://localhost/push/push.php?id=bod&bod={}".format(bod)
        tss_data = "http://localhost/push/push.php?id=tss&tss={}".format(tss)
        ph_data = "http://localhost/push/push.php?id=ph&ph={}".format(ph)
        fm1_data = "http://localhost/push/push.php?id=fm1&fmid1=001&tot1={}&flow1={}".format(tot1,flow1)
        fm2_data = "http://localhost/push/push.php?id=fm2&fmid2=002&tot2={}&flow2={}".format(tot2,flow2)
        update_cod_api = requests.get(cod_data)
        update_bod_api = requests.get(bod_data)
        update_tss_api = requests.get(tss_data)
        update_ph_api = requests.get(ph_data)
        update_fm1_api = requests.get(fm1_data)
        update_fm2_api = requests.get(fm2_data)
        print(cod_data)
        print(update_cod_api.status_code)
        print(bod_data)
        print(update_bod_api.status_code)
        print(tss_data)
        print(update_tss_api.status_code)
        print(ph_data)
        print(update_ph_api.status_code)
        print(fm1_data)
        print(update_fm1_api.status_code)
        print(fm2_data)
        print(update_fm2_api.status_code)
        time.sleep(10)
        
        
    except minimalmodbus.NoResponseError:
        
        # Close the serial connections for the instruments on error
        instrument1.serial.close()
        instrument2.serial.close()
        instrument3.serial.close()
        instrument4.serial.close()
        #time.sleep(5)
