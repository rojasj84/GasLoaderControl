# This program requres installation of NIDAQMX library
import nidaqmx

# Read the state of digital port X
def read_di(chan, port):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan("Dev1/port" + str(chan) + "/line" + str(port))
        value = task.read()
        # print(value)
        return value


def read_ai(port):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai" + str(port))
        value = float(task.read())
        # print(value)
        return value

def write_ao(port, volt_val):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("Dev1/ao" + str(port))
        task.write(volt_val)
        # print(value)

def write_diport(chan, port, port_val):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan("Dev1/port" + str(chan) + "/line" + str(port))
        #print(port_val)
        task.write(port_val)
