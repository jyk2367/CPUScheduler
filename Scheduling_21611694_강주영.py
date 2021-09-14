from tkinter import *
from tkinter.simpledialog import *


Menu = Tk()
Menu.withdraw()
MENU = askinteger("Menu","1.SJF 2.PriorityScheduling 3.Round-Robin 4.Own",minvalue=1,maxvalue=4)
Menu.destroy()

if MENU==1:
    import SJF_21611694_강주영
elif MENU==2:
    import PriorityScheduling_21611694_강주영
elif MENU==3:
    import RoundRobinScheduling_21611694_강주영
elif MENU==4:
    import OwnScheduling_21611694_강주영
else:
    exit()
