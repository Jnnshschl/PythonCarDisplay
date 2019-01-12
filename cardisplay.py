from tkinter import *
import datetime
import obd
import subprocess


# Settings
#----------------------------------------------------------

obd.logger.setLevel(obd.logging.DEBUG)
connectionStatus = obd.OBDStatus.NOT_CONNECTED
connection = None

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

# Init stuff
#----------------------------------------------------------

obd.logger.setLevel(obd.logging.ERROR)
connectionStatus = obd.OBDStatus.NOT_CONNECTED
connection = None

# Custom-Parsers
#----------------------------------------------------------

# Custom ELM-Voltage parser & command for my module
def elmVoltageCustom(messages):
	return messages[0].frames[0].raw.lower().split('v')[0].replace('v', '')

voltagecmd = obd.OBDCommand("ELM_VOLTAGECUSTOM", "Voltage custom", b"ATRV", 0, elmVoltageCustom, obd.ECU.UNKNOWN, False)

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

labelsX = 6;
valuesX = 180;

batteryLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Bordspannung:")
batteryLabel.place(x=labelsX, y=48)
batteryPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... V")
batteryPercentageLabel.place(x=valuesX, y=48)

waterLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Wassertemp:")
waterLabel.place(x=labelsX, y=72)
waterPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °C")
waterPercentageLabel.place(x=valuesX, y=72)

airLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugtemp:")
airLabel.place(x=labelsX, y=96)
airPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °C")
airPercentageLabel.place(x=valuesX, y=96)

airflowLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugmasse:")
airflowLabel.place(x=labelsX, y=120)
airflowPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... g/s")
airflowPercentageLabel.place(x=valuesX, y=120)

lambdaLabel1 = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Lambda 1:")
lambdaLabel1.place(x=labelsX, y=144)
lambdaPercentageLabel1 = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... mV")
lambdaPercentageLabel1.place(x=valuesX, y=144)

lambdaLabel2 = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Lambda 2:")
lambdaLabel2.place(x=labelsX, y=168)
lambdaPercentageLabel2 = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... mV")
lambdaPercentageLabel2.place(x=valuesX, y=168)

ignitionLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Zündwinkel:")
ignitionLabel.place(x=labelsX, y=192)
ignitionPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °")
ignitionPercentageLabel.place(x=valuesX, y=192)

loadLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 20), text="Motorlast:")
loadLabel.place(x=labelsX, y=228)
loadPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 20), text="... %")
loadPercentageLabel.place(x=valuesX, y=228)

gasLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 20), text="Gas:")
gasLabel.place(x=labelsX, y=260)
gasPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 20), text="... %")
gasPercentageLabel.place(x=valuesX, y=260)

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
	timeToRunAfter = 500
	
	time = datetime.datetime.now()+datetime.timedelta(hours=1)
	timeLabel.config(text=time.strftime("%H:%M:%S"))

	temp = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	pitempLabel.config(text=round(int(temp)/1000))

	clock = subprocess.run(['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	piclockLabel.config(text=round(int(clock)/1000))

	if connection is not None:
		connectionStatus = connection.status()
		statusLabel.config(text=connectionStatus)

	if connectionStatus is obd.OBDStatus.NOT_CONNECTED or connection is None:
		connection = obd.OBD()
		connection.supported_commands.add(voltagecmd)

	if connectionStatus is not obd.OBDStatus.NOT_CONNECTED:
		voltage = connection.query(voltagecmd, force=True)
		try:
			batteryPercentageLabel.config(text=str(voltage.value).split(" ")[0] + " V")
		except:
			batteryPercentageLabel.config(text="0 V")
			
		water = connection.query(obd.commands.COOLANT_TEMP)
		try:
			waterPercentageLabel.config(text=str(water).split(" ")[0] + " °C")
		except:
			waterPercentageLabel.config(text="0 °C")
		
		intaketemp = connection.query(obd.commands.INTAKE_TEMP)
		try:
			airPercentageLabel.config(text=str(intaketemp).split(" ")[0] + " °C")
		except:
			airPercentageLabel.config(text="0 °C")
			
		maf = connection.query(obd.commands.MAF)
		try:
			airflowPercentageLabel.config(text=str(round(float(maf.split(" ")[0]), 2) + " g/s"))
		except:
			airflowPercentageLabel.config(text=maf)
			
		lambdavolt1 = connection.query(obd.commands.O2_B1S1)
		try:
			lambdaPercentageLabel1.config(text=str(lambdavolt1).split(" ")[0] + " mV")
		except:
			lambdaPercentageLabel1.config(text="0 mV") 
			
		lambdavolt2 = connection.query(obd.commands.O2_B1S2)
		try:	
			lambdaPercentageLabel2.config(text=str(lambdavolt2).split(" ")[0] + " mV")
		except:
			lambdaPercentageLabel2.config(text="0 mV")
			
		timingadvance = connection.query(obd.commands.TIMING_ADVANCE)
		try:
			ignitionPercentageLabel.config(text=str(timingadvance).split(" ")[0] + " °")
		except:
			ignitionPercentageLabel.config(text="0 °") 
		
		engineload = connection.query(obd.commands.ENGINE_LOAD)
		try:
			loadPercentageLabel.config(text=str(round(float(engineload)) + " %"))
		except:
			loadPercentageLabel.config(text=engineload) 
		
		gas = connection.query(obd.commands.THROTTLE_POS)
		try:
			gasPercentageLabel.config(text=str(round(float(gas)) + " %"))
		except:
			gasPercentageLabel.config(text=gas) 
			
		speed = connection.query(obd.commands.SPEED)
		try:
			speedLabel.config(text=str(round(float(speed))))
		except:
			speedLabel.config(text=speed)
			
		rpm = connection.query(obd.commands.RPM)
		try:
			revsLabel.config(text=str(round(float(rpm))))
		except:
			revsLabel.config(text=rpm)
	else:
		timeToRunAfter = 2000

	root.after(timeToRunAfter, uiUpdate)

uiUpdate()

root.mainloop()
