from tkinter import *
import datetime
import obd
import subprocess

# Settings
bluetoothMac = "00:1D:A5:68:98:8B"
uiRefreshInterval = 200
logoPng = "/home/pi/cardisplay/opel.png"

colorBackground = "black"

colorTitle1 = "red"
colorTitle2 = "orange"
colorTime = "white"

colorPi = "white"
colorTemp = "orange"
colorC = "white"
colorClock = "orange"
colorMHz = "white"

colorStatus= "white"
colorLabels = "white"
colorValues = "orange"

colorSpeed = "orange"
colorRevs = "orange"

colorKmh = "white"
colorUmin = "white"
# Settings end

connectionStatus = obd.OBDStatus.NOT_CONNECTED
connection = obd.OBD()

# GUI
#----------------------------------------------------------

root = Tk()

root.title("Car Display")
root.geometry("480x320")
root.attributes('-fullscreen', True)
root.configure(background=colorBackground)

# Titel bar
#----------------------------------------------------------

logoImage = PhotoImage(file=logoPng)
logoLabel = Label(image=logoImage)
logoLabel.place(x=6, y=2, height=36, width=36)

titleLabel1 = Label(root, fg=colorTitle1, bg=colorBackground, font=("Aldrich", 20), text="OPEL")
titleLabel1.place(x=42, y=8)

titleLabel2 = Label(root, fg=colorTitle2, bg=colorBackground, font=("Aldrich", 14), text="Corsa C 1.2L Twinport")
titleLabel2.place(x=120, y=14)

timeLabel = Label(root, fg=colorTime, bg=colorBackground, font=("Aldrich", 16), text="00:00:00")
timeLabel.place(x=380, y=12)

statusLabel = Label(root, fg=colorStatus, bg=colorBackground, font=("Aldrich", 16), text="NOT_CONNECTED")
statusLabel.place(x=6, y=300)

# Pi Labels
#----------------------------------------------------------

piLabel = Label(root, fg=colorPi, bg=colorBackground, font=("Aldrich", 16), text="Pi:")
piLabel.place(x=220, y=300)

pitempLabel = Label(root, fg=colorTemp, bg=colorBackground, font=("Aldrich", 16), text="50")
pitempLabel.place(x=280, y=300)
pitempxLabel = Label(root, fg=colorC, bg=colorBackground, font=("Aldrich", 16), text="°C")
pitempxLabel.place(x=310, y=300)

piclockLabel = Label(root, fg=colorClock, bg=colorBackground, font=("Aldrich", 16), text="1000")
piclockLabel.place(x=350, y=300)
piclockxLabel = Label(root, fg=colorMHz, bg=colorBackground, font=("Aldrich", 16), text="MHz")
piclockxLabel.place(x=420, y=300)

# Left Labels
#----------------------------------------------------------

batteryLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Bordspannung:")
batteryLabel.place(x=6, y=48)
batteryPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... V")
batteryPercentageLabel.place(x=220, y=48)

waterLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Wassertemperatur:")
waterLabel.place(x=6, y=72)
waterPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °C")
waterPercentageLabel.place(x=220, y=72)

airLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugtemperatur:")
airLabel.place(x=6, y=96)
airPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °C")
airPercentageLabel.place(x=220, y=96)

airflowLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugmasse:")
airflowLabel.place(x=6, y=120)
airflowPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... g/s")
airflowPercentageLabel.place(x=220, y=120)

lambdaLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Lambdaspannung:")
lambdaLabel.place(x=6, y=144)
lambdaPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... mV")
lambdaPercentageLabel.place(x=220, y=144)

intakepressureLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugdruck:")
intakepressureLabel.place(x=6, y=168)
intakepressurePercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... kPa")
intakepressurePercentageLabel.place(x=220, y=168)

fuelpressureLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Benzindruck:")
fuelpressureLabel.place(x=6, y=192)
fuelpressurePercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... kPa")
fuelpressurePercentageLabel.place(x=220, y=192)

ignitionLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Zündwinkel:")
ignitionLabel.place(x=6, y=216)
ignitionPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °")
ignitionPercentageLabel.place(x=220, y=216)

loadLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Motorlast:")
loadLabel.place(x=6, y=240)
loadPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... %")
loadPercentageLabel.place(x=220, y=240)

gasLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Gas:")
gasLabel.place(x=6, y=264)
gasPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... %")
gasPercentageLabel.place(x=220, y=264)

# Left Labels
#----------------------------------------------------------

speedLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 32), text="0")
speedLabel.place(x=280, y=48)
kmhLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 32), text="km/h")
kmhLabel.place(x=370, y=48)

revsLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 20), text="0")
revsLabel.place(x=280, y=96)
uminLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 20), text="U/min")
uminLabel.place(x=370, y=96)

#----------------------------------------------------------

def uiUpdate():
	global connectionStatus
	global connection
	timeToRunAfter = uiRefreshInterval
	
	time = datetime.datetime.now().strftime("%H:%M:%S")
	timeLabel.config(text=time)

	temp = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	pitempLabel.config(text=round(int(temp)/1000))

	clock = subprocess.run(['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	piclockLabel.config(text=round(int(clock)/1000))

	connectionStatus = connection.status()
	statusLabel.config(text=connectionStatus)

	if connectionStatus is obd.OBDStatus.NOT_CONNECTED:
		connection = obd.OBD()

	if connectionStatus is not obd.OBDStatus.NOT_CONNECTED:
		
		try:
			voltage = connection.query(obd.commands.ELM_VOLTAGE)
			batteryPercentageLabel.config(text=str(voltage).split("")[0] + " V")
		except:
			batteryPercentageLabel.config(text="0 V")
			
		try:	
			water = connection.query(obd.commands.COOLANT_TEMP)
			waterPercentageLabel.config(text=str(water).split("")[0] + " °C")
		except:
			waterPercentageLabel.config(text="0 °C")
			
		try:	
			intaketemp = connection.query(obd.commands.INTAKE_TEMP)
			airPercentageLabel.config(text=str(intaketemp).split("")[0] + " °C")
		except:
			airPercentageLabel.config(text="0 °C")
			
		try:	
			maf = connection.query(obd.commands.MAF)
			airflowPercentageLabel.config(text=round(int(str(maf).split("")[0]), 2) + " g/s")
		except:
			airflowPercentageLabel.config(text="0 g/s")
			
		try:	
			lambdavolt = connection.query(obd.commands.O2_S1_WR_VOLTAGE)
			lambdaPercentageLabel.config(text=str(lambdavolt).split("")[0] + " mV")
		except:
			lambdaPercentageLabel.config(text="0 mVl") 
			
		try:	
			intakepressure = connection.query(obd.commands.INTAKE_PRESSURE)
			intakepressurePercentageLabel.config(text=str(intakepressure).split("")[0] + " kPa")		
		except:
			intakepressurePercentageLabel.config(text="0 kPa") 
			
		try:   
			fuelpressure = connection.query(obd.commands.FUEL_PRESSURE)
			fuelpressurePercentageLabel.config(text=str(fuelpressure).split("")[0] + " kPa")
		except:
			fuelpressurePercentageLabel.config(text="0 kPa") 
			
		try:	
			timingadvance = connection.query(obd.commands.TIMING_ADVANCE)
			ignitionPercentageLabel.config(text=str(timingadvance).split("")[0] + " °")
		except:
			ignitionPercentageLabel.config(text="0 °") 
		 
		try:	
			engineload = connection.query(obd.commands.ENGINE_LOAD)
			loadPercentageLabel.config(text=round(int(str(engineload).split("")[0])) + " %")
		except:
			loadPercentageLabel.config(text="0 %") 
			
		try:	
			gas = connection.query(obd.commands.THROTTLE_POS)
			gasPercentageLabel.config(text=round(int(str(gas).split("")[0])) + " %")
		except:
			gasPercentageLabel.config(text="0 %") 
			
		try:	
			speed = connection.query(obd.commands.SPEED)
			speedLabel.config(text=round(int(speed.split("")[0]))) 
		except:
			speedLabel.config(text="0")
			
		try:	
			rpm = connection.query(obd.commands.RPM)
			revsLabel.config(text=round(int(rpm.split("")[0])))
		except:
			revsLabel.config(text="0")
	else:
		timeToRunAfter = 2000

	root.after(timeToRunAfter, uiUpdate)

uiUpdate()

root.mainloop()
