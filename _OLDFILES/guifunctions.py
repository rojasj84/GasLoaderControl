# Defining functions
def Bt1_clk():
    if Pin2_Com.get() == 0:
        state_val = False
    else:
        state_val = True
    write_diport(0, state_val)
