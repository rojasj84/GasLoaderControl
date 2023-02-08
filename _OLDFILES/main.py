# Import libraries from Python
import tkinter as tk
import time
from threading import Thread
from PIL import ImageTk, Image

from instrument_gauges import *
from denkser import *

# This program requres installation of NIDAQMX library
# Import the .py file that accesses the NI-USB-6001
from niusb6001 import *

# Defining functions
def do_nothing():
    x = 0

def get_valve_image(file_loc):
    # Valve images are 100x56
    img = Image.open(file_loc)
    img_width, img_height = img.size
    area = (25, 0, 75, 56)
    img = img.crop(area)
    return img

def scale_images(file_loc,scale):
    img = Image.open(file_loc)
    img_width, img_height = img.size
    img = img.resize((img_width // scale, img_height // scale), resample=Image.Resampling.LANCZOS)
    return img

def update_data():
    window.after(refresh_time, update_data)
    
def update_relay_states(relay,state):
    setbit(COMPORT,relay,state)
    if relay < 6:
        update_valve_image(relay,state)

def update_valve_image(relay,state):
    #Update the status of the valve relays on screen
    if relay < 2:
        # print(relay)
        if state == 1:
            v_color[relay] = "Blue"
        else:
            v_color[relay] = "Red"
    else:
        if state == 1:
            v_color[relay] = "Red"
        else:
            v_color[relay] = "Blue"
    update_plines()

def update_plines():
    # Line that indicates flow status across Valve 1
    V1_line = canvas.create_line(50, c_height/2, c_width/4,c_height/2, width = l_w, fill = v_color[0])
    V1_line_2 = canvas.create_line(50, c_height/2, c_width/4,c_height/2, width = l_w, fill = v_color[0])

    # Line that indicates flow status across Valve 2
    V2_line = canvas.create_line(c_width*3/4, c_height/2, c_width-50,c_height/2, width = l_w, fill = v_color[1])

    # Lines that indicates flow status across Valve 3
    V3_line_1 = canvas.create_line(c_width/4, c_height/2, c_width/4,bt_w, width = l_w, fill = v_color[2])
    V3_line_2 = canvas.create_line(c_width/4-l_w/2,bt_w, c_width/2, bt_w, width = l_w, fill = v_color[2])

    # Lines that indicates flow status across Valve 4
    V4_line_1 = canvas.create_line(c_width/4, c_height/2, c_width/4,c_height-bt_w, width = l_w, fill = v_color[3])
    V4_line_2 = canvas.create_line(c_width/4-l_w/2,c_height-bt_w, c_width/2, c_height-bt_w, width = l_w, fill = v_color[3])

    # Lines that indicates flow status across Valve 5
    V5_line_1 = canvas.create_line(3*c_width/4, c_height/2, 3*c_width/4,bt_w, width = l_w, fill = v_color[4])
    V5_line_2 = canvas.create_line(3*c_width/4+l_w/2,bt_w, c_width/2, bt_w, width = l_w, fill = v_color[4])

    # Lines that indicates flow status across Valve 6
    V6_line_1 = canvas.create_line(3*c_width/4, c_height/2, 3*c_width/4,c_height-bt_w, width = l_w, fill = v_color[5])
    V6_line_2 = canvas.create_line(3*c_width/4+l_w/2,c_height-bt_w, c_width/2, c_height-bt_w, width = l_w, fill = v_color[5])

    # Line that indicates flow line to compressor inlet
    V7_line = canvas.create_line(c_width/4-l_w/2,c_height/2, c_width/3,c_height/2, width = l_w, fill = "blue")

    # Line that indicates flow line to compressor outlet
    V8_line = canvas.create_line(3*c_width/4+l_w/2,c_height/2, 2*c_width/3,c_height/2, width = l_w, fill = "blue")

    # Line that indicates flow to the CL Chamber
    V9_line = canvas.create_line(c_width/2,0, c_width/2,bt_w+l_w/2, width = l_w, fill = "blue")

    # Line that indicates flow to the sample chambers
    V10_line = canvas.create_line(c_width/2,c_height, c_width/2,c_height-(bt_w+l_w/2), width = l_w, fill = "blue")

def update_data_displays():

    Lecture_Bottle_Pressure = 4000
    Bottle_Pressure = 1800
    CloverLeave_Pressure = 15000

    img_CLP = rotery_gauge(0,5000,Bottle_Pressure)
    img_width, img_height = img_CLP.size
    img_CLP = img_CLP.resize((img_width // 5, img_height // 5), resample=Image.Resampling.LANCZOS)
    img_CLP = ImageTk.PhotoImage(img_CLP)
    label = tk.Label(window, image = img_CLP, bg = win_color)
    label.image = img_CLP # keep a reference!
    label.place(x=bt_x-350,y=bt_y-300)

    img_CLP = rotery_gauge(0,30000,CloverLeave_Pressure)
    img_width, img_height = img_CLP.size
    img_CLP = img_CLP.resize((img_width // 3, img_height // 3), resample=Image.Resampling.LANCZOS)
    img_CLP = ImageTk.PhotoImage(img_CLP)
    label = tk.Label(window, image = img_CLP, bg = win_color)
    label.image = img_CLP # keep a reference!
    label.place(x=bt_x+100,y=bt_y-375)

    img_CLP = rotery_gauge(0,5000,Lecture_Bottle_Pressure)
    img_width, img_height = img_CLP.size
    img_CLP = img_CLP.resize((img_width // 4, img_height // 4), resample=Image.Resampling.LANCZOS)
    img_CLP = ImageTk.PhotoImage(img_CLP)
    label = tk.Label(window, image = img_CLP, bg = win_color)
    label.image = img_CLP # keep a reference!
    label.place(x=bt_x-250,y=bt_y+135)

    window.after(refresh_time, update_data_displays)

if __name__ == "__main__":

    # Global variables
    angle = 0
    refresh_time = 100  # time sensors refresh
    ai_pts = [0,0,0,0,0,0]
    win_color = 'light gray'
    COMPORT = "COM10"

    # Valve path colors
    v_color = ["Red","Red","Blue","Blue","Blue","Blue"]


    # Begin code with window code
    window = tk.Tk()
    window.title("Gas Loader Control Screen")
    window.geometry("1000x800")
    window.configure(bg=win_color)

    # Create the check buttons to actuate the valves
    bt_w = 50
    bt_h = 50
    bt_x = 400
    bt_y = 400
    bt_gap = 100

    # Create a canvas to show paths
    c_height = bt_gap*2+2*bt_h
    c_width = bt_gap*6+2*bt_w
    l_w = 8
    canvas=tk.Canvas(window, width=c_width, height=c_height, bg=win_color, bd = 0, relief="flat")
    canvas.config(highlightthickness=0)
    canvas.place(x=bt_x-bt_gap*3-bt_w,y=bt_y-bt_gap-bt_h)

    # Variables for the states of the checkbuttons
    val1_stat = tk.IntVar()
    val2_stat = tk.IntVar()
    val3_stat = tk.IntVar()
    val4_stat = tk.IntVar()
    val5_stat = tk.IntVar()
    val6_stat = tk.IntVar()
    val7_stat = tk.IntVar()
    vacpump_stat = tk.IntVar()
    unstick_stat = tk.IntVar()
    compress_stat = tk.IntVar()
    motor_cw_stat = tk.IntVar()
    motor_ccw_stat = tk.IntVar()

    # Valve images are 100x56
    # img = Image.open("images/NCC.png")
    # img_width, img_height = img.size
    # area = (25, 0, 75, 56)
    # img = img.crop(area)

    img_NCC = ImageTk.PhotoImage(get_valve_image("images/NCC.png"))
    img_NCO = ImageTk.PhotoImage(get_valve_image("images/NCO.png"))
    img_NOO = ImageTk.PhotoImage(get_valve_image("images/NOO.png"))
    img_NOC = ImageTk.PhotoImage(get_valve_image("images/NOC.png"))

    # Adding Images of Cloverleaf, Lecture Bottle and Gas Bottle
    img_lbt = ImageTk.PhotoImage(scale_images("images/lecture-bottle2.png",5))
    lbl_lbt = tk.Label(window, image = img_lbt, bg = win_color, bd = 0)
    lbl_lbt.place(x=bt_x-50,y=bt_y+150)

    img_CL = ImageTk.PhotoImage(scale_images("images/cl-chamber2.png",6))
    lbl_cl = tk.Label(window, image = img_CL, bg = win_color, bd = 0)
    lbl_cl.place(x=bt_x-60,y=bt_y-255)

    img_BT = ImageTk.PhotoImage(scale_images("images/bottle2.png",3))
    lbl_BT = tk.Label(window, image = img_BT, bg = win_color, bd = 0)
    lbl_BT.place(x=bt_x-365,y=bt_y-140)

    # Call for Initial Relay State
    relay_state = readdenk(COMPORT)

    bt_valve1 = tk.Checkbutton(window, text = "Valve 1", variable = val1_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(0,val1_stat.get()), image=img_NCC, selectimage=img_NCO)
    bt_valve1.place(x=bt_x-bt_gap*2.5-bt_w/2,y=bt_y-bt_h/2)

    bt_valve2 = tk.Checkbutton(window, text = "Valve 2", variable = val2_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(1,val2_stat.get()), image=img_NCC, selectimage=img_NCO)
    bt_valve2.place(x=bt_x+bt_gap*2.5-bt_w/2,y=bt_y-bt_h/2)

    bt_valve3 = tk.Checkbutton(window, text = "Valve 3", variable = val3_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(2,val3_stat.get()), image=img_NOO, selectimage=img_NOC)
    bt_valve3.place(x=bt_x-bt_gap-bt_w/2,y=bt_y-bt_gap-bt_h/2)

    bt_valve4 = tk.Checkbutton(window, text = "Valve 4", variable = val4_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(3,val4_stat.get()), image=img_NOO, selectimage=img_NOC)
    bt_valve4.place(x=bt_x-bt_gap-bt_w/2,y=bt_y+bt_gap-bt_h/2)

    bt_valve5 = tk.Checkbutton(window, text = "Valve 5", variable = val5_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(4,val5_stat.get()), image=img_NOO, selectimage=img_NOC)
    bt_valve5.place(x=bt_x+bt_gap-bt_w/2,y=bt_y-bt_gap-bt_h/2)

    bt_valve6 = tk.Checkbutton(window, text = "Valve 6", variable = val6_stat, onvalue = 1, offvalue = 0, height=bt_h, width = bt_w, indicatoron = False, command=lambda: update_relay_states(5,val6_stat.get()), image=img_NOO, selectimage=img_NOC)
    bt_valve6.place(x=bt_x+bt_gap-bt_w/2,y=bt_y+bt_gap-bt_h/2)

    lbl_cin = tk.Label(window, text = "LP", font=("Helvetica", 20, "bold"), bg = win_color)
    lbl_cin.place(x=bt_x-150,y=bt_y-1.5*l_w)

    lbl_cout = tk.Label(window, text = "HP", font=("Helvetica", 20, "bold"), bg = win_color)
    lbl_cout.place(x=bt_x+110,y=bt_y-1.5*l_w)

    # Vacuum Pump, Compressor and Unsticker Actuation
    sl_x = 800
    sl_y = 100
    sl_y_gap = 35

    # Slider image
    on_image = tk.PhotoImage(width=48, height=25)
    off_image = tk.PhotoImage(width=48, height=25)
    on_image.put(("red",), to=(0, 0, 23,23))
    off_image.put(("blue",), to=(24, 0, 47, 23))

    lbl_vacpump = tk.Label(window, text = "Vacuum Pump", font=("Helvetica", 12, "bold"), bg = win_color, anchor="e", width = 15)
    lbl_vacpump.place(x=sl_x-35,y=sl_y+sl_y_gap*0)
    bt_vacpump = tk.Checkbutton(window, text = "Vacuum Pump", variable = vacpump_stat, onvalue = 1, offvalue = 0, height=24, width = 48, indicatoron = False, command=lambda: update_relay_states(10,vacpump_stat.get()), image=on_image, selectimage=off_image)
    bt_vacpump.place(x=sl_x+125,y=sl_y+sl_y_gap*0-5)

    lbl_valveunstick = tk.Label(window, text = "Unstick Valves", font=("Helvetica", 12, "bold"), bg = win_color, anchor="e", width = 15)
    lbl_valveunstick.place(x=sl_x-35,y=sl_y+sl_y_gap*1)
    bt_valveunstick = tk.Checkbutton(window, text = "Unstick Valves", variable = unstick_stat, onvalue = 1, offvalue = 0, height=24, width = 48, indicatoron = False, command=lambda: update_relay_states(6,unstick_stat.get()), image=on_image, selectimage=off_image)
    bt_valveunstick.place(x=sl_x+125,y=sl_y+sl_y_gap*1-5)

    lbl_booster = tk.Label(window, text = "Compressor", font=("Helvetica", 12, "bold"), bg = win_color, anchor="e", width = 15)
    lbl_booster.place(x=sl_x-35,y=sl_y+sl_y_gap*2)
    bt_booster = tk.Checkbutton(window, text = "Compressor", variable = compress_stat, onvalue = 1, offvalue = 0, height=24, width = 48, indicatoron = False, command=lambda: update_relay_states(7,compress_stat.get()), image=on_image, selectimage=off_image)
    bt_booster.place(x=sl_x+125,y=sl_y+sl_y_gap*2-5)

    lbl_motor_cw = tk.Label(window, text = "Motor CW", font=("Helvetica", 12, "bold"), bg = win_color, anchor="e", width = 15)
    lbl_motor_cw.place(x=sl_x-35,y=sl_y+sl_y_gap*4)
    bt_motor_cw = tk.Checkbutton(window, text = "Motor CW", variable = motor_cw_stat, onvalue = 1, offvalue = 0, height=24, width = 48, indicatoron = False, command=lambda: update_relay_states(8,motor_cw_stat.get()), image=on_image, selectimage=off_image)
    bt_motor_cw.place(x=sl_x+125,y=sl_y+sl_y_gap*4-5)

    lbl_motor_ccw = tk.Label(window, text = "Motor CCW", font=("Helvetica", 12, "bold"), bg = win_color, anchor="e", width = 15)
    lbl_motor_ccw.place(x=sl_x-35,y=sl_y+sl_y_gap*5)
    bt_motor_ccw = tk.Checkbutton(window, text = "Motor CCW", variable = motor_ccw_stat, onvalue = 1, offvalue = 0, height=24, width = 48, indicatoron = False, command=lambda: update_relay_states(9,motor_ccw_stat.get()), image=on_image, selectimage=off_image)
    bt_motor_ccw.place(x=sl_x+125,y=sl_y+sl_y_gap*5-5)

    # Set image for valve state
    val1_stat.set(relay_state[0])
    val2_stat.set(relay_state[1])
    val3_stat.set(relay_state[2])
    val4_stat.set(relay_state[3])
    val5_stat.set(relay_state[4])
    val6_stat.set(relay_state[5])

    unstick_stat.set(relay_state[6])
    compress_stat.set(relay_state[7])
    vacpump_stat.set(relay_state[10])

    # Call function to add pressure lines
    for i in range (0,6):        
        update_valve_image(i,relay_state[i])


    # Start thread to update data
    new_thread2 = Thread(target=update_data_displays())
    new_thread2.start()

    window.mainloop()
