#!/usr/bin/env python3

from tkinter import Label, PhotoImage, Tk, Canvas, ttk
import subprocess
import datetime
import time
import json
import obd
import os


# Settings
#----------------------------------------------------------
labelsX = 6
valuesX = 170

connectionStatus = obd.OBDStatus.NOT_CONNECTED
connection = None

logValuesToFile = True
logFileName = "/home/pi/obd2_values.txt"

logoPng = "/home/pi/cardisplay/opel.png"
textTile1 = "OPEL"
textTile2 = "Corsa C 1.2L Twinport"

colorBackground = "black"

colorTitle1 = "firebrick1"
colorTitle2 = "firebrick2"
colorTime = "white"

colorLoadBar = "firebrick1"
colorGasBar = "firebrick1"

colorPi = "white"
colorTemp = "tomato"
colorC = "white"
colorClock = "tomato"
colorMHz = "white"

colorStatus= "darkorange"
colorLabels = "white"
colorValues = "orange"

colorSpeed = "darkorange"
colorRevs = "darkorange"

colorKmh = "white"
colorUmin = "white"

pointerWidth = 6 / 2 # will be 6 pixels

colorLambdaHeader = "white"
colorLambdaFooter = "white"

colorLambda1Bad = "firebrick1"
colorLambda1Okay = "gold"
colorLambda1Good = "chartreuse2"

colorLambda2Bad = "firebrick1"
colorLambda2Okay = "gold"
colorLambda2Good = "chartreuse2"

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

titleLabel1 = Label(root, fg=colorTitle1, bg=colorBackground, font=("Aldrich", 20), text=textTile1)
titleLabel1.place(x=42, y=8)

titleLabel2 = Label(root, fg=colorTitle2, bg=colorBackground, font=("Aldrich", 14), text=textTile2)
titleLabel2.place(x=120, y=14)

timeLabel = Label(root, fg=colorTime, bg=colorBackground, font=("Aldrich", 16), text="00:00:00")
timeLabel.place(x=376, y=12)

statusLabel = Label(root, fg=colorStatus, bg=colorBackground, font=("Aldrich", 16), text="NOT_CONNECTED")
statusLabel.place(x=6, y=300)

# Pi Labels
#----------------------------------------------------------

piLabel = Label(root, fg=colorPi, bg=colorBackground, font=("Aldrich", 16), text="Pi:")
piLabel.place(x=220, y=300)

pitempLabel = Label(root, fg=colorTemp, bg=colorBackground, font=("Aldrich", 16), text="0")
pitempLabel.place(x=280, y=300)
pitempxLabel = Label(root, fg=colorC, bg=colorBackground, font=("Aldrich", 16), text="°C")
pitempxLabel.place(x=310, y=300)

piclockLabel = Label(root, fg=colorClock, bg=colorBackground, font=("Aldrich", 16), text="0")
piclockLabel.place(x=350, y=300)
piclockxLabel = Label(root, fg=colorMHz, bg=colorBackground, font=("Aldrich", 16), text="MHz")
piclockxLabel.place(x=420, y=300)

# Left Labels
#----------------------------------------------------------

batteryLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Bordspannung:")
batteryLabel.place(x=labelsX, y=48)
batteryPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... V")
batteryPercentageLabel.place(x=valuesX, y=48)

waterLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Kühlmittel:")
waterLabel.place(x=labelsX, y=72)
waterPercentageLabel = Label(root, fg=colorValues, bg=colorBackground, font=("Aldrich", 14), text="... °C")
waterPercentageLabel.place(x=valuesX, y=72)

airLabel = Label(root, fg=colorLabels, bg=colorBackground, font=("Aldrich", 14), text="Ansaugluft:")
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

speedLabel = Label(root, fg=colorSpeed, bg=colorBackground, font=("Aldrich", 32), text="0")
speedLabel.place(x=280, y=48)
kmhLabel = Label(root, fg=colorKmh, bg=colorBackground, font=("Aldrich", 32), text="km/h")
kmhLabel.place(x=370, y=48)

revsLabel = Label(root, fg=colorRevs, bg=colorBackground, font=("Aldrich", 20), text="0")
revsLabel.place(x=280, y=96)
uminLabel = Label(root, fg=colorUmin, bg=colorBackground, font=("Aldrich", 20), text="U/min")
uminLabel.place(x=370, y=96)

# Gauges
#----------------------------------------------------------

#speedGauge = Canvas(root, bg=colorBackground, width=180, height=200)
#speedGauge.place(x=280, y=140)
#speedGauge.create_arc(10, 10, 170, 190, style="arc", width=20, start=-10, extent=170, outline=speedGaugeColorNormal, tags=('arc2'))
#speedGauge.create_arc(10, 10, 170, 190, style="arc", width=20, start=160, extent=20, outline=speedGaugeColorHigh, tags=('arc1'))

#polyPoints = [(100, 40), (110, 100), (100, 110), (90, 100)]
#polyNeedle = speedGauge.create_polygon(polyPoints, fill='white')

# Bars
#----------------------------------------------------------


lambdaBarsLabel = Label(root, fg=colorLambdaHeader, bg=colorBackground, font=("Aldrich", 12), text="Luft/Benzingemisch:")
lambdaBarsLabel.place(x=280, y=130)
lambdaBarsLabel2 = Label(root, fg=colorLambdaFooter, bg=colorBackground, font=("Aldrich", 12), text="Mager                  Fett")
lambdaBarsLabel2.place(x=280, y=196)

lambda1BarCanvas = Canvas(root, bg=colorBackground, width=180, height=12, borderwidth=0, highlightthickness=0)
lambda1BarCanvas.create_rectangle(0, 2, 40, 10, fill=colorLambda1Bad)
lambda1BarCanvas.create_rectangle(30, 2, 70, 10, fill=colorLambda1Okay)
lambda1BarCanvas.create_rectangle(70, 2, 110, 10, fill=colorLambda1Good)
lambda1BarCanvas.create_rectangle(110, 2, 150, 10, fill=colorLambda1Okay)
lambda1BarCanvas.create_rectangle(150, 2, 180, 10, fill=colorLambda1Bad)
lambda1Pointer = lambda1BarCanvas.create_rectangle(88, 0, 92, 11, fill='white')
lambda1BarCanvas.place(x=280, y=154 + 1)

lambda2BarCanvas = Canvas(root, bg=colorBackground, width=180, height=12, borderwidth=0, highlightthickness=0)
lambda2BarCanvas.create_rectangle(0, 2, 40, 10, fill=colorLambda2Bad)
lambda2BarCanvas.create_rectangle(30, 2, 70, 10, fill=colorLambda2Okay)
lambda2BarCanvas.create_rectangle(70, 2, 110, 10, fill=colorLambda2Good)
lambda2BarCanvas.create_rectangle(110, 2, 150, 10, fill=colorLambda2Okay)
lambda2BarCanvas.create_rectangle(150, 2, 180, 10, fill=colorLambda2Bad)
lambda2Pointer = lambda2BarCanvas.create_rectangle(88, 0, 92, 11, fill='white')
lambda2BarCanvas.place(x=280, y=178 + 1)

gasLoadTheme = ttk.Style()
gasLoadTheme.theme_use('clam')
gasLoadTheme.configure("loadBarTheme.Horizontal.TProgressbar", background=colorLoadBar, troughcolor=colorBackground, bordercolor="gray30")

loadBar = ttk.Progressbar(root, style="loadBarTheme.Horizontal.TProgressbar", orient="horizontal", length=180, mode="determinate", maximum=100)
loadBar.place(x=280, y=228)

gasBarTheme = ttk.Style()
gasBarTheme.theme_use('clam')
gasBarTheme.configure("gasBarTheme.Horizontal.TProgressbar", background=colorGasBar, troughcolor=colorBackground, bordercolor="gray30")

gasBar = ttk.Progressbar(root, style="gasBarTheme.Horizontal.TProgressbar", orient="horizontal", length=180, mode="determinate", maximum=100)
gasBar.place(x=280, y=260)

#----------------------------------------------------------

class CarData:
	def __init__(self, connectionStatus, batteryVoltage, coolantTemperature, intakeTemperature, intakeAirflow, lambdaVoltage1, lambdaVoltage2, timingAdvance, engineLoad, throttle, speed, rpm):
		self.timestamp = int(round(time.time() * 1000))
		self.connectionStatus = connectionStatus
		self.batteryVoltage = batteryVoltage
		self.coolantTemperature = coolantTemperature
		self.intakeTemperature = intakeTemperature
		self.intakeAirflow = intakeAirflow
		self.lambdaVoltage1 = lambdaVoltage1
		self.lambdaVoltage2 = lambdaVoltage2
		self.timingAdvance = timingAdvance
		self.engineLoad = engineLoad
		self.throttle = throttle
		self.speed = speed
		self.rpm = rpm

#----------------------------------------------------------

def QueryAndParseResultSpace(connection, cmd, roundDecimals):
	try:
		result = 0
		rawResult = connection.query(cmd)

		if rawResult != None and str(rawResult) != "None" and str(rawResult.value) != "atr":
			try:
				splittedStuff = str(rawResult.value)
				result = round(float(splittedStuff), roundDecimals)
		
				if roundDecimals is 0:
					result = int(result)
			except Exception as ex:
				print("Error: " + str(ex)) 
				result = -1
		else:
			print("[" + str(cmd) + "] No value received...")
			result = 0
		
	except Exception as excep:
		print("Error: " + str(excep))
		result = -1
	return result


def CalculateLambdaPointerPosition(currentLambda, maxX, maxY):
	finalPos = int(maxX / 2) - pointerWidth, 0, int(maxX / 2) + pointerWidth, 12

	try:
		lambdaPercent = float(currentLambda) / 1.0
		finalPos = (maxX * lambdaPercent) - pointerWidth, 0, (maxX * lambdaPercent) + pointerWidth, 12
	except:
		pass

	return finalPos


def uiUpdate():
	global connectionStatus
	global connection

	#print("Updating UI...")

	time = datetime.datetime.now() + datetime.timedelta(hours=1)
	timeLabel.config(text=time.strftime("%H:%M:%S"))

	temp = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	pitempLabel.config(text=round(int(temp)/1000))

	clock = subprocess.run(['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	piclockLabel.config(text=round(int(clock)/1000))

	if connection is not None:
		connectionStatus = connection.status()
		statusLabel.config(text=connectionStatus)

	# if we aren't connected, try to connect and add our custom voltage cmd
	if connectionStatus is obd.OBDStatus.NOT_CONNECTED or connection is None:
		connection = obd.OBD()
		connection.supported_commands.add(voltagecmd)
	
	if connectionStatus is obd.OBDStatus.CAR_CONNECTED:
		currentCarData = CarData(
			connectionStatus,
			QueryAndParseResultSpace(connection, voltagecmd, 2),
			QueryAndParseResultSpace(connection, obd.commands.COOLANT_TEMP, 0),
			QueryAndParseResultSpace(connection, obd.commands.INTAKE_TEMP, 0),
			QueryAndParseResultSpace(connection, obd.commands.MAF, 0),
			QueryAndParseResultSpace(connection, obd.commands.O2_B1S1, 2),
			QueryAndParseResultSpace(connection, obd.commands.O2_B1S2, 2),
			QueryAndParseResultSpace(connection, obd.commands.TIMING_ADVANCE, 2),
			QueryAndParseResultSpace(connection, obd.commands.ENGINE_LOAD, 0),
			QueryAndParseResultSpace(connection, obd.commands.THROTTLE_POS, 0),
			QueryAndParseResultSpace(connection, obd.commands.SPEED, 0),
			QueryAndParseResultSpace(connection, obd.commands.RPM, 0)
		)
	else:
		if connectionStatus is obd.OBDStatus.OBD_CONNECTED:
			currentCarData = CarData(connectionStatus, QueryAndParseResultSpace(connection, voltagecmd, 2), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
		else:
			currentCarData = CarData(connectionStatus, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

	batteryPercentageLabel.config(text=str(currentCarData.batteryVoltage) + " V")
	waterPercentageLabel.config(text=str(currentCarData.coolantTemperature) + " °C")
	airPercentageLabel.config(text=str(currentCarData.intakeTemperature) + " °C")
	airflowPercentageLabel.config(text=str(currentCarData.intakeAirflow) + " g/s")
	lambdaPercentageLabel1.config(text=str(currentCarData.lambdaVoltage1) + " mV")
	lambdaPercentageLabel2.config(text=str(currentCarData.lambdaVoltage2) + " mV")
	ignitionPercentageLabel.config(text=str(currentCarData.timingAdvance) + " °")
	loadPercentageLabel.config(text=str(currentCarData.engineLoad) + " %")
	gasPercentageLabel.config(text=str(currentCarData.throttle) + " %")
	speedLabel.config(text=str(currentCarData.speed))
	revsLabel.config(text=str(currentCarData.rpm))

	loadBar["value"] = currentCarData.engineLoad
	gasBar["value"] = currentCarData.throttle

	lambdaPointer1Pos = CalculateLambdaPointerPosition(currentCarData.lambdaVoltage1, 180, 12)
	lambdaPointer2Pos = CalculateLambdaPointerPosition(currentCarData.lambdaVoltage2, 180, 12)

	lambda1BarCanvas.coords(lambda1Pointer, lambdaPointer1Pos[0], lambdaPointer1Pos[1], lambdaPointer1Pos[2], lambdaPointer1Pos[3],)
	lambda2BarCanvas.coords(lambda2Pointer, lambdaPointer2Pos[0], lambdaPointer2Pos[1], lambdaPointer2Pos[2], lambdaPointer2Pos[3],)

	# log data
	if logValuesToFile:
		with open(logFileName, "a") as logfile:
			logfile.write(json.dumps(currentCarData.__dict__) + "\n")

	root.after(250, uiUpdate)

def main():
	# prevent screensaver on XFCE
	os.system("xset s off")
	os.system("xset dpms 0 0 0")
	os.system("xset -dpms s off")

	# hide the cursor
	os.system("unclutter &")

	uiUpdate()
	root.mainloop()


if __name__ == '__main__':
	main()
