# Import libraries from Python
import tkinter as tk
import math
import cv2
import time
from threading import Thread

# This program requres installation of NIDAQMX library

# Import the .py file that accesses the NI-USB-6001
from niusb6001 import *

# Defining global Variables
refresh_time = 100  # time sensors refresh
ai_pts = [0,0,0,0,0,0]

# Begin code with window code
window = tk.Tk()
window.title("Excimer Laser Control Screen")
window.geometry("600x600")
win_color = 'light gray'
window.configure(bg=win_color)

# *******************Defining functions*******************

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)


# Function for sending button states to NI USB 6001 Digital Ports
# Arguments, Digital Channel (INT), Digital Port (INT), Port Status (BOOL)
def cBt_clk(chan, port, bt_state):
    # print(bt_state)
    write_diport(chan, port, bt_state)

def set_LazHV():
    # print(bt_state)
    volt_val = float(txt_HV_val.get("1.0", "end-1c"))
    if volt_val > 20:
        volt_val = 20
    elif volt_val < 0:
        volt_val = 0

    volt_val = volt_val / 4
    write_ao(0, volt_val)

def update_data():
    #read the analog ports and store values
    ai_pts[0] = round(float(read_ai('0'))*10/5,3)
    ai_pts[1] = round(float(read_ai('4'))*6500/5)
    ai_pts[2] = read_ai('1')
    ai_pts[3] = round(float(read_ai('5'))*20/5,1)
    ai_pts[4] = read_ai('2')
    ai_pts[5] = round(float(read_ai('6'))*50/5)


    lbl_filmon_val.config(text = ai_pts[0])
    lbl_gasP_val.config(text = ai_pts[1])
    lbl_enS_val.config(text = ai_pts[2])
    lbl_hvP_val.config(text = ai_pts[3])
    lbl_enEXT_val.config(text = ai_pts[4])
    lbl_lazTMP_val.config(text = ai_pts[5])
    lbl_IntSTAT_val.config(text=str(read_di(1,3)))
    lbl_SumSTAT_val.config(text=str(read_di(2,0)))

    window.after(refresh_time, update_data)

def donothing():
   x = 0

def begin_pulses():
    # Enable pulsing
    write_ao(1, 5)
    time.sleep(0.002)
    write_ao(1, 0)
    # print("True")
    
# *******************Populate window with items to display information*******************

# Declaring the variables for the digital logic connections
Pin1_Pulses = tk.BooleanVar()
Pin2_Com = tk.BooleanVar()
Pin3_Sol1 = tk.BooleanVar()
Pin16_Sol2 = tk.BooleanVar()
Pin4_Sol3 = tk.BooleanVar()
Pin5_EnRes = tk.BooleanVar()
Pin6_Mot1 = tk.BooleanVar()
Pin12_FloInj = tk.BooleanVar()
Pin17_Fans = tk.BooleanVar()
Pin15_Mot2 = tk.BooleanVar()
Pin21_VacP = tk.BooleanVar()

# label = tk.Label(window)
# label.place(x=600,y=50)
# cap = cv2.VideoCapture(0)

# Declaring some consntants
btn_w = 22
btn_h = 2

# Location of logic output buttons
out_btx = 400
out_bty = 50
out_bt_gap = 42

in_lbx = 0
in_lby = 50
in_lb_gap = 25
in_lb_gapx = 270

# Top menu bar customization
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=donothing)
# filemenu.add_command(label="Save", command=donothing)
# filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)

# Placing the checkbuttons for logic outputs that talks to the laser
classBt1  = tk.Checkbutton(window, text = "Command Charge", variable = Pin2_Com, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 0, Pin2_Com.get()))
classBt1.place(x=out_btx,y=out_bty+out_bt_gap*0)

classBt2  = tk.Checkbutton(window, text = "Solenoid #1 Pump Out", variable = Pin3_Sol1, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 1, Pin3_Sol1.get()))
classBt2.place(x=out_btx,y=out_bty+out_bt_gap*1)

classBt3  = tk.Checkbutton(window, text = "Solenoid #2 Fill Valve", variable = Pin16_Sol2, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 6, Pin16_Sol2.get()))
classBt3.place(x=out_btx,y=out_bty+out_bt_gap*2)

classBt4  = tk.Checkbutton(window, text = "Solenoid #3 Main Valve", variable = Pin4_Sol3, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 2, Pin4_Sol3.get()))
classBt4.place(x=out_btx,y=out_bty+out_bt_gap*3)

classBt5  = tk.Checkbutton(window, text = "Enable/Reset", variable = Pin5_EnRes, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 3, Pin5_EnRes.get()))
classBt5.place(x=out_btx,y=out_bty+out_bt_gap*4)

classBt6  = tk.Checkbutton(window, text = "Motor 1", variable = Pin6_Mot1, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 4, Pin6_Mot1.get()))
classBt6.place(x=out_btx,y=out_bty+out_bt_gap*5)

classBt6  = tk.Checkbutton(window, text = "Motor 2", variable = Pin15_Mot2, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(1, 0, Pin15_Mot2.get()))
classBt6.place(x=out_btx,y=out_bty+out_bt_gap*6)

classBt7  = tk.Checkbutton(window, text = "Cooling Fan ON/OFF", variable = Pin17_Fans, onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 7, Pin17_Fans.get()))
classBt7.place(x=out_btx,y=out_bty+out_bt_gap*7)

classBt8  = tk.Checkbutton(window, text = "Vacuum Pump ON/OFF", variable = Pin21_VacP,  onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(1, 1, Pin21_VacP.get()))
classBt8.place(x=out_btx,y=out_bty+out_bt_gap*8)

classBt9  = tk.Checkbutton(window, text = "Flourine Injector", variable = Pin12_FloInj,  onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False, command = lambda: cBt_clk(0, 5, Pin12_FloInj.get()))
classBt9.place(x=out_btx,y=out_bty+out_bt_gap*9)

classBt10  = tk.Checkbutton(window, text = "Begin Pulses", variable = Pin1_Pulses,  onvalue = True, offvalue = False, height=btn_h, width = btn_w, bd=2, indicatoron=False)#, command = lambda: begin_pulses(Pin1_Pulses.get()))
classBt10.place(x=out_btx,y=out_bty+out_bt_gap*10)

# Placing labels to display analog inputs from laser
lbl_filmon = tk.Label(window, text='Filament Monitor (V): ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_filmon.place(x=in_lbx,y=in_lby+in_lb_gap*0)
lbl_filmon_val = tk.Label(window, text= ai_pts[0], bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_filmon_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*0)

lbl_gasP = tk.Label(window, text='Gas Pressure (Torr): ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_gasP.place(x=in_lbx,y=in_lby+in_lb_gap*1)
lbl_gasP_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_gasP_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*1)

lbl_enS = tk.Label(window, text='Energy Sensor: ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_enS.place(x=in_lbx,y=in_lby+in_lb_gap*2)
lbl_enS_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_enS_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*2)

lbl_hvP = tk.Label(window, text='HV Peak (kV): ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_hvP.place(x=in_lbx,y=in_lby+in_lb_gap*3)
lbl_hvP_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_hvP_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*3)

lbl_enEXT = tk.Label(window, text='External Energy Monitor: ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_enEXT.place(x=in_lbx,y=in_lby+in_lb_gap*4)
lbl_enEXT_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_enEXT_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*4)

lbl_lazTMP = tk.Label(window, text='Laser Temperature (°C): ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_lazTMP.place(x=in_lbx,y=in_lby+in_lb_gap*5)
lbl_lazTMP_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_lazTMP_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*5)

lbl_IntSTAT= tk.Label(window, text='Interlock Open: ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_IntSTAT.place(x=in_lbx,y=in_lby+in_lb_gap*6)
lbl_IntSTAT_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_IntSTAT_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*6)

lbl_SumSTAT= tk.Label(window, text='Fault Status: ', bg = win_color, font = ('Helvetica', 12), borderwidth=0, relief="solid", height=1, width = 30, anchor = "e")
lbl_SumSTAT.place(x=in_lbx,y=in_lby+in_lb_gap*7)
lbl_SumSTAT_val = tk.Label(window, text='test', bg = win_color, font = ('Helvetica', 12), borderwidth=1, relief="solid", height=1, width = 10, anchor = "w")
lbl_SumSTAT_val.place(x=(in_lbx+in_lb_gapx),y=in_lby+in_lb_gap*7)

# Change the HV Value of the Laser
lbl_HV_val = tk.Label(window, height = 1, width = 30, text = "Set Laser HV 0-20kV ",bg = win_color, font = ('Helvetica', 10), borderwidth=0, relief="solid", anchor = "w")
lbl_HV_val.place(x=100,y=330)

txt_HV_val = tk.Text(window, height = 1, width = 15)
txt_HV_val.place(x=100,y=350)

btn_HV_val = tk.Button(window, text ="SET LASER HV", command = set_LazHV)
btn_HV_val.place(x=100,y=375)

# Updating values from the digital and analog inputs
new_thread2 = Thread(target=update_data())
new_thread2.start()

new_thread3 = Thread(target=begin_pulses())
new_thread3.start()

# Function to call camera
#show_frames()
window.mainloop()
