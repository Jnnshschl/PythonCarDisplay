# Python Car Display

This is a display for my car 🚗 written in python 🐍, it will connect to your OBD2 Adapter via bluetooth.

## How to use it

You need to have *Python3*, *Tkinter* and *bluez* installed
```bash
sudo apt install python3 python3-tk bluez
```

Also you need the pip module *OBD*
```bash
pip3 install obd
```

1. Replace the MAC Address in the file *connectToOBD2.sh*
2. Create a cronjob for this script
```bash
sudo crontab -e
```
3. Add this to the end of the file (every minute it will try to connect to your OBD2 adapter)
```bash
*/1 *  *  *  * sh connectToOBD2.sh
```
4. After you've done that start the *cardisplay.py*
```bash
python3 cardisplay.py
```
5. (Optional) Create an autostart file for it (this is for the XFCE Desktop)
```bash
nano /home/pi/.config/autostart/cardisplay.desktop
```

```bash
[Desktop Entry]
Encoding=UTF-8
Version=0.1
Type=Application
Name=Cardisplay
Comment=Cardisplay
Exec=/usr/bin/python3 /home/pi/cardisplay/cardisplay.py
StartupNotify=false
Terminal=false
Hidden=false
```

![alt text](https://github.com/Jnnshschl//PythonCarDisplay/blob/master/images/image.png?raw=true "Pi with Display")
