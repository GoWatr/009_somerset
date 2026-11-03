#updated on 28.09.2023
import minimalmodbus
import serial
import time
import struct
import json
import requests
from serial.tools import list_ports

cod = 0.0
bod = 0.0
tss = 0.0
ph = 0.0
tot1 = 0.0
flow1 = 0.0
tot2 = 0.0
flow2 = 0.0

flow11 = 0
tot11 = 0


# Function to automatically find the Arduino port on both Windows and Linux
def find_arduino_port():
    arduino_ports = [p.device for p in list_ports.comports() if 'Arduino' in p.description]
    if not arduino_ports:
        arduino_ports = [p.device for p in list_ports.comports() if 'ttyACM' in p.device]
        if not arduino_ports:
            raise IOError("No Arduino found. Check if it's connected.")
    return arduino_ports[0]
try:
# Automatically find the Arduino port
    arduino_port = find_arduino_port()

# port name, slave address (in decimal)
    ser = serial.Serial(arduino_port, 9600, timeout=1)
except IOError as e:
    print(e)
    ser = None
    
    
an_instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
fm1_instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 2)
fm2_instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 3)
an_instrument.serial.baudrate = fm1_instrument.serial.baudrate = fm2_instrument.serial.baudrate = 9600      
an_instrument.serial.bytesize = fm1_instrument.serial.bytesize = fm2_instrument.serial.bytesize = 8
an_instrument.serial.stopbits = fm1_instrument.serial.stopbits = fm2_instrument.serial.stopbits = 1
an_instrument.serial.timeout = fm1_instrument.serial.timeout  = fm2_instrument.serial.timeout  = 1          
an_instrument.mode = fm1_instrument.mode = fm2_instrument.mode = minimalmodbus.MODE_RTU  
an_instrument.clear_buffers_before_each_transaction = fm1_instrument.clear_buffers_before_each_transaction = fm2_instrument.clear_buffers_before_each_transaction = True
an_instrument.debug = fm1_instrument.debug = fm2_instrument.debug = True


def analyzer_cod():
    try:
        reg0 = an_instrument.read_register(0, 0, 3)
        reg1 = an_instrument.read_register(1, 0, 3)
        regset1 = hex((reg1<<16) | reg0)[2:]
        regset1_str = str(regset1)
        f_cod = struct.unpack('>f', bytes.fromhex(regset1_str))[0]
        cod = round(f_cod, 2)
        print("The COD HEX is : ", regset1_str)
        print("The COD Value is : ", cod)
        cod_data = "http://localhost/push/push.php?id=cod&cod={}".format(cod)
        update_cod_api = requests.get(cod_data)
        print(cod_data)
        print(update_cod_api.status_code)
        an_instrument.serial.close()
     
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError, ValueError, UnboundLocalError) as error:
        print("Error in response of cod")
        ############################################
def analyzer_bod():
    try:
        reg2 = an_instrument.read_register(2, 0, 3)
        reg3 = an_instrument.read_register(3, 0, 3)
        regset2 = hex((reg3<<16) | reg2)[2:]
        regset2_str = str(regset2)
        f_bod = struct.unpack('>f', bytes.fromhex(regset2_str))[0]
        bod = round(f_bod, 2)
        print("The BOD HEX is : ", regset2_str)
        print("The BOD Value is : ", bod)
        bod_data = "http://localhost/push/push.php?id=bod&bod={}".format(bod)
        update_bod_api = requests.get(bod_data)
        print(bod_data)
        print(update_bod_api.status_code)
        an_instrument.serial.close()
     
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError, ValueError) as error:
        print("Error in response of bod")
        ############################################
def analyzer_tss():
    global tss  # Use global variable
    try:
        reg4 = an_instrument.read_register(4, 0, 3)
        reg5 = an_instrument.read_register(5, 0, 3)
        regset3 = hex((reg5<<16) | reg4)[2:]
        regset3_str = str(regset3)
        try:
            f_tss = struct.unpack('>f', bytes.fromhex(regset3_str))[0]
        except (struct.error, ValueError):
            f_tss = 0.0

        tss = round(f_tss, 2)
        print("The TSS HEX is : ", regset3_str)
        print("The TSS Value is : ", tss)
        tss_data = "http://localhost/push/push.php?id=tss&tss={}".format(tss)
        update_tss_api = requests.get(tss_data)
        print(tss_data)
        print(update_tss_api.status_code)
        an_instrument.serial.close()
     
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as error:
        print("Error in response of tss")
        ############################################
def analyzer_ph():
    try:
        reg6 = an_instrument.read_register(6, 0, 3)
        reg7 = an_instrument.read_register(7, 0, 3)
        regset4 = hex((reg7<<16) | reg6)[2:]
        regset4_str = str(regset4)
        f_ph = struct.unpack('>f', bytes.fromhex(regset4_str))[0]
        ph = round(f_ph, 2)
        print("The PH HEX is : ", regset4_str)
        print("The PH Value is : ", ph)
        ph_data = "http://localhost/push/push.php?id=ph&ph={}".format(ph)
        update_ph_api = requests.get(ph_data)
        print(ph_data)
        print(update_ph_api.status_code)
        
        an_instrument.serial.close()
     
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError, ValueError) as error:
        print("Error in response of ph")

def flowmeter1():
    try:
        response = fm1_instrument.read_registers(0, 10, 3)
        tot1 = ((response[3] << 16) | response[2])
        #tot1 = tot1
        #tot1 = "{:.1f}".format(tot1)
        flow1 = response[1]
        flow11 = flow1
        tot11 = tot1
        print("The inlet fm totalizer is : ", tot1, "LPH")
        print("The inlet fm flowrate is : ", flow1, "LPH")
    
        fm1_data = "http://localhost/push/push.php?id=fm1&fmid1=001&tot1={}&flow1={}".format(tot1,flow1)
        update_fm1_api = requests.get(fm1_data)
        print(fm1_data)
        print(update_fm1_api.status_code)
        #time.sleep(2)
        sensor_name = "Flow"
        sensor_value = flow1
        send_sensor_data(sensor_name , sensor_value)
        #time.sleep(2)
        sensor_name = "Tot"
        sensor_value = tot1
        send_sensor_data(sensor_name , sensor_value)
        #time.sleep(2)
        fm1_instrument.serial.close()
             
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as error:
        print("Error in response of FM1")
        
def flowmeter2():
    try:
        response2 = fm2_instrument.read_registers(0, 8, 3)
        tot2 = ((response2[3] << 16) | response2[2])
        #tot2 = tot2
        #tot2 = "{:.1f}".format(tot2)
        flow2 = response2[1] 
        print("The outlet fm totalizer is : ", tot2, "LPH")
        print("The outlet fm flowrate is : ", flow2, "LPH")
    
        fm2_data = "http://localhost/push/push.php?id=fm2&fmid2=002&tot2={}&flow2={}".format(tot2,flow2)
        update_fm2_api = requests.get(fm2_data)
        print(fm2_data)
        print(update_fm2_api.status_code)
        #time.sleep(2)
        sensor_name = "Flow2"
        sensor_value = flow2
        send_sensor_data(sensor_name , sensor_value)
        #time.sleep(2)
        sensor_name = "Tot2"
        sensor_value = tot2
        send_sensor_data(sensor_name , sensor_value)
        #time.sleep(2)
        fm2_instrument.serial.close()
        
        
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as error:
        print("Error in response of FM2")

def send_sensor_data(sensor_name, sensor_value):
    data = f"{sensor_name}:{sensor_value}\n"
    ser.write(data.encode())  

while True:
    analyzer_cod()
    analyzer_bod()
    analyzer_tss()
    analyzer_ph()
    time.sleep(5)
    flowmeter1()
    time.sleep(5)
    flowmeter2()
    
    #send_sensor_data(sensor_name, sensor_value)

    time.sleep(1)
    time.sleep(20)
        






