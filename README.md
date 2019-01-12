# Python Car Display

This is a display for my car written in python, it will connect to your OBD2 Adapter via bluetooth.

🐍 + 🚗 = ❤️

## How to use it

You need to have *Python3*, *Tkinter* and *bluez* installed
```shell
sudo apt install python3 python3-tk bluez
```

Also you need the pip module *OBD*
```shell
pip3 install obd
```

*Optional*: Install the aldrich font https://fonts.google.com/specimen/Aldrich

1. Replace the MAC Address (00:1D:A5:68:98:8B) in the file *connectToOBD2.sh* with your OBD2 Adapter MAC. To get the MAC address use *bluetoothctl*, type *"scan on"* and it will get listed if your Pi is able to reach it.
```shell
pi@CorsaC:~/cardisplay $ sudo bluetoothctl
[NEW] Controller 00:1A:7D:DA:71:13 CorsaC [default]
[bluetooth]# scan on
[NEW] Device 00:1D:A5:68:98:8B OBDII
[NEW] Device 08:AE:D6:67:79:DC Galaxy S9+
```
```shell
if [ ! -f /dev/rfcomm0 ]; then
  # Replace the MAC below
  sudo rfcomm connect hci0 00:1D:A5:68:98:8B 1 &
fi
```
2. Create a cronjob for this script
```shell
sudo crontab -e
```
3. Add this to the end of the file (every minute it will try to connect to your OBD2 adapter)
```shell
*/1 *  *  *  * sh connectToOBD2.sh
```
4. After you've done that start the *cardisplay.py*
```shell
python3 cardisplay.py
```
5. (Optional) Create an autostart file for it (this is for the XFCE Desktop)
```shell
nano /home/pi/.config/autostart/cardisplay.desktop
```

```shell
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

## Images

![alt text](https://github.com/Jnnshschl//PythonCarDisplay/blob/master/images/image.png?raw=true "Pi with Display")

## Credits

❤️ PyOBD - https://python-obd.readthedocs.io/en/latest/

❤️ Tkinter - https://wiki.python.org/moin/TkInter