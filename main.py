# Importing libraries
import tkinter as tk
import numpy as np
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image

# Importing local .py files
from instrument_gauges import *

#Create Classes
class GaugeImage(tk.Frame):
    def __init__(self, container, min_pressure, max_pressure, pressure_value, scale, x_position, y_position):
        super().__init__(container)

        # Variables for the gauge
        self.min_pressure = min_pressure
        self.max_pressure = max_pressure
        self.pressure_value = pressure_value
        self.scale = scale
        self.x_position = x_position
        self.y_position = y_position

        #Variables for displaying
        frame_padding = 2

        img_CLP = rotery_gauge(min_pressure,max_pressure,pressure_value)
        img_width, img_height = img_CLP.size
        img_CLP = img_CLP.resize((img_width // scale, img_height // scale), resample=Image.Resampling.LANCZOS)
        img_CLP = ImageTk.PhotoImage(img_CLP)

        frame_height = (img_width / scale) + frame_padding + 50
        frame_width = (img_width / scale) + frame_padding + 2

        # show the frame on the container
        self.config(background=win_color)
        self.place(x=x_position,y=y_position,height = frame_height,width = frame_width)

        # display gauge               
        self.pressure_gauge = tk.Label(self, image = img_CLP, background=win_color)
        self.pressure_gauge.image = img_CLP # keep a reference!
        self.pressure_gauge.place(x=frame_padding/2,y=frame_padding/2)        
        
        # pressure numbers display
        self.pressure_numbers = tk.Label(self,text= str(pressure_value) + " psi", background=win_color,font=('Helvatical bold',15), justify=tk.RIGHT, bg="White", highlightthickness=2, highlightbackground="Black")
        self.pressure_numbers.place(x=0,y=frame_height-40, height = 30, width=frame_width)

        self.update_gauge_data()

    def update_gauge_data(self):

        refresh_time = 100 #Milliseconds 

        self.pressure_value = int(np.random.rand(1)*5000)

        #Variables for displaying
        frame_padding = 2

        # updating valve image
        img_CLP = rotery_gauge(self.min_pressure,self.max_pressure,self.pressure_value)
        img_width, img_height = img_CLP.size
        img_CLP = img_CLP.resize((img_width // self.scale, img_height // self.scale), resample=Image.Resampling.LANCZOS)
        img_CLP = ImageTk.PhotoImage(img_CLP)

        # updating display gauge               
        self.pressure_gauge.config(image=img_CLP)
        self.pressure_gauge.image = img_CLP
        
        # updating pressure numbers display
        self.pressure_numbers.config(text = str(self.pressure_value) + " psi")

        self.after(refresh_time,self.update_gauge_data)

class ControlValve(tk.Frame):
    def __init__(self, container,valvetype, valvestate, x_position, y_position):
        super().__init__(container)
        # Varibles for creating the valve check button
        self.valvetype = valvetype
        self.valvestate = valvestate
        self.x_position = x_position
        self.y_position = y_position        

        # Load images for the checkbox valves
        if valvetype == "NC":
            valve_image_normal = ImageTk.PhotoImage(self.get_valve_image("images/NCC.png"))            
            valve_image_opposite = ImageTk.PhotoImage(self.get_valve_image("images/NCO.png"))
        elif valvetype == "NO":
            valve_image_normal = ImageTk.PhotoImage(self.get_valve_image("images/NOO.png"))            
            valve_image_opposite = ImageTk.PhotoImage(self.get_valve_image("images/NOC.png"))

        print(x_position)
        print(y_position)
        # Show the frame on the container
        self.config(background=win_color)
        self.place(x=x_position,y=y_position,height = 60,width = 60)
        
        # Create a variable to keep track of state        
        self.button_state = tk.IntVar(self)
        # Show the valve using the conditional to determine the valve initial state

        bt_valve = tk.Checkbutton(self, text = "Valve", command = self.valve_actuation_state, variable = self.button_state, indicatoron = False, image=valve_image_normal, selectimage=valve_image_opposite, relief = tk.FLAT)                
        bt_valve.image = valve_image_normal
        bt_valve.selectimage = valve_image_opposite
        bt_valve.place(x=0,y=0)
        
        # Update valve button state status
        print(valvestate)
        if self.valvestate == 1:
             bt_valve.select()        
        else:
            bt_valve.deselect()


        # Places the initial state of the check button


    def get_valve_image(self, file_loc):
        # Valve images are 100x56
        img = Image.open(file_loc)
        img_width, img_height = img.size
        area = (25, 0, 75, 56)
        img = img.crop(area)
        return img
    
    def valve_actuation_state(self):        
        x = 0
        print(self.button_state.get())
    
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Gas Loader Controls')
        self.geometry('1200x800')
        self.configure(bg=win_color)

#Create Functions

if __name__ == "__main__":
    win_color = 'light gray'

    # Creating the main window
    window = MainWindow()
    
    # Populating the gauges on screen
    bottle_pressure = GaugeImage(window,0,5000,2000, 4, 50, 50)
    cl_chamber_pressure = GaugeImage(window,0,30000,15000, 3, 800, 50)
    lecture_bottle_pressure = GaugeImage(window,0,5000,2000, 4, 800, 500)

    # Populating the checkbuttons to control the flow valves
    Valve1 = ControlValve(window,"NC", 0, 150, 400)
    Valve2 = ControlValve(window,"NC", 0, 650, 400)
    Valve3 = ControlValve(window,"NO", 0, 300, 300)   
    Valve4 = ControlValve(window,"NO", 0, 300, 500)
    Valve5 = ControlValve(window,"NO", 0, 500, 300)
    Valve6 = ControlValve(window,"NO", 0, 500, 500)

    window.mainloop()