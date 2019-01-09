from tkinter import *
import datetime
import obd


connectionStatus = obd.OBDStatus.NOT_CONNECTED
isLogoVisible = True

connection = obd.OBD()

#ports = obd.scan_serial()
#print(ports)

# GUI
#----------------------------------------------------------

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

timeLabel = Label(root, fg='white', bg='black', font=("Aldrich", 16), text="00:00:00")
timeLabel.place(x=380, y=12)

statusLabel = Label(root, fg='white', bg='black', font=("Aldrich", 16), text="NOT_CONNECTED")
statusLabel.place(x=6, y=292)

#----------------------------------------------------------

batteryLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Bordspannung:")
batteryLabel.place(x=6, y=48)
batteryPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
batteryPercentageLabel.place(x=220, y=48)

waterLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Wassertemperatur:")
waterLabel.place(x=6, y=72)
waterPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
waterPercentageLabel.place(x=220, y=72)

airLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Ansaugtemperatur:")
airLabel.place(x=6, y=96)
airPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
airPercentageLabel.place(x=220, y=96)

airflowLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Ansaugmasse:")
airflowLabel.place(x=6, y=120)
airflowPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
airflowPercentageLabel.place(x=220, y=120)

lambdaLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Lambdaspannung:")
lambdaLabel.place(x=6, y=144)
lambdaPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
lambdaPercentageLabel.place(x=220, y=144)

intakepressureLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Ansaugdruck:")
intakepressureLabel.place(x=6, y=168)
intakepressurePercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
intakepressurePercentageLabel.place(x=220, y=168)

fuelpressureLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Benzindruck:")
fuelpressureLabel.place(x=6, y=192)
fuelpressurePercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
fuelpressurePercentageLabel.place(x=220, y=192)

ignitionLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Zündwinkel:")
ignitionLabel.place(x=6, y=216)
ignitionPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
ignitionPercentageLabel.place(x=220, y=216)

loadLabel = Label(root, fg='white', bg='black', font=("Aldrich", 14), text="Motorlast:")
loadLabel.place(x=6, y=240)
loadPercentageLabel = Label(root, fg='cyan', bg='black', font=("Aldrich", 14), text="...")
loadPercentageLabel.place(x=220, y=240)

#----------------------------------------------------------

def uiUpdate():
    global connectionStatus
    global connection
    timeToRunAfter = 200

    time = datetime.datetime.now().strftime("%H:%M:%S")
    timeLabel.config(text=time)

    connectionStatus = connection.status()
    statusLabel.config(text=connectionStatus)

    if connectionStatus is obd.OBDStatus.NOT_CONNECTED:
        connection = obd.OBD()

    if connectionStatus is not obd.OBDStatus.NOT_CONNECTED:
        cmdVoltage = obd.commands.ELM_VOLTAGE
        voltage = connection.query(cmdVoltage)
        batteryLabel.config(text=voltage)
    else:
        timeToRunAfter = 1000

    root.after(timeToRunAfter, uiUpdate)

uiUpdate()

root.mainloop()
