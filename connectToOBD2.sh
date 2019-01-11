#!/bin/bash

# Place this script in a cronjob or similar
# grep 'sh connectToOBD2.sh' /etc/crontab || sudo echo '*/1 *  *  *  * sh connectToOBD2.sh' >> /etc/crontab

if [ ! -f /dev/rfcomm0 ]; then
  # Replace the MAC below
  sudo rfcomm connect hci0 00:1D:A5:68:98:8B 1 &
fi
