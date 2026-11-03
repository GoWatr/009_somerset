import minimalmodbus
import time

# Initialize variables
combined_data = 0.0
flow_data = 0.0

# Port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('COM9', 3)


# Set up instrument configurations (baudrate, bytesize, etc.)
def setup_instrument(instrument):
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.clear_buffers_before_each_transaction = True
    instrument.debug = True

# Function to read combined data from instrument
def read_combined_data(instrument):
    try:
        response = instrument.read_registers(0, 8, 3)
        combined_data = (response[3] << 16) | response[2]
        combined_data = combined_data * 0.1
        formatted_decimal = "{:.2f}".format(combined_data)
        flow_data = response[1] * 0.01
        print(combined_data)
        print(flow_data)
        print(formatted_decimal)
        return combined_data, flow_data
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as error:
        print("No response from the instrument. Retrying...")
        return None, None

# Function to read and process data from instrument1
# Main loop
while True:
    setup_instrument(instrument)
    
    combined_data = read_combined_data(instrument)
        
    instrument.serial.close()
    time.sleep(1)
