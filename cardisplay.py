from tkinter import *

root = Tk()

root.title("Car Display")
root.geometry("480x320")
root.attributes('-fullscreen', True)
root.configure(background='black')

#----------------------------------------------------------

logoImage = PhotoImage(file="opel.png")
logoLabel = Label(image=logoImage)
logoLabel.place(x=6, y=2, height=36, width=36)

titleLabel1 = Label(root, fg='red', bg='black', font=("Aldrich", 20), text="OPEL")
titleLabel1.place(x=42, y=8)
titleLabel2 = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="Corsa C 1.2L Twinport")
titleLabel2.place(x=120, y=14)

#----------------------------------------------------------

batteryLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Battery:")
batteryLabel.place(x=6, y=48)

batteryPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="12 V")
batteryPercentageLabel.place(x=220, y=48)

#----------------------------------------------------------

waterLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Water Temperature:")
waterLabel.place(x=6, y=72)

waterPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="90 °C")
waterPercentageLabel.place(x=220, y=72)

#----------------------------------------------------------

root.mainloop()
