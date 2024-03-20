## PyRover

    python main.py

**RPi PWM Outputs:** 12, 13, 18, 19  
**Ardusimple Pins:** 15, 14, 17, 24

## Para correr Str2str
    cd /home/luis/RTKLIB-rtklib_2.4.3/app/consapp/str2str/gcc/
    str2str -out serial://ttyACM0:115200:8:n:1:off -in ntrip://192.168.1.9:2101/TBO &

## Instalar RPi GNU/Linux 12 (bookworm)
Para chequear version: cat /etc/os-release

Python:

    sudo apt install git python3-pip
    pip3 install --break-system-packages keyboard 
    pip3 install --break-system-packages navpy

Habilitar puerto serial:

    sudo nano /etc/udev/rules.d/99-serial.rules
        KERNEL=="ttyUSB[0-9]*",MODE="0666"
        KERNEL=="ttyACM[0-9]*",MODE="0666"
        KERNEL=="ttyS[0-9]*",MODE="0666"


Instalar XRDP

    sudo apt install xrdp
    sudo adduser luis
    sudo adduser luis sudo
    echo 'luis ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/010_luis-nopasswd
    sudo usermod -aG gpio luis

Git  

    git clone https://github.com/riosmiguel/pyrover.git
    git config --global user.email jumiguelrios@gmail.com
    git config --global user.name miguel

# No necesario

Instalar str2str

    https://discourse.agopengps.com/t/rtk-base-with-a-raspberry-pi4-and-simplertk2b/1849/2
    https://github.com/tomojitakasu/RTKLIB/tree/rtklib_2.4.3
    download zip
    extract to ~/RTKLIB-rtklib_2.4.3
    cd ~/RTKLIB-rtklib_2.4.3/app/consapp/str2str/gcc
    make
    sudo make install
    close and open terminal

    Find out which COM port is the GPS in the USB:

    dmesg | grep tty
    [  232.604357] cdc_acm 1-1.2:1.0: ttyACM0: USB ACM device


## Mapas servicio geografico chaja

G13A2
G13A3
G13A5
G13A6

EPSG 5382

## Mover archivos



## Pantalla adafruit

    git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git

    sudo apt install python3.11-venv
    python -m venv env --system-site-packages
    source env/bin/activate
    pip3 install --upgrade adafruit-python-shell click

    source env/bin/activate
    cd Raspberry-Pi-Installer-Scripts
    sudo -E env PATH=$PATH python3 adafruit-pitft.py --display=35r --rotation=270 --install-type=console

    sudo dpkg-reconfigure console-setup
    sudo raspi-config

## gpsd 


    sudo apt install gpsd gpsd-clients python-gps -->> E: Package 'python-gps' has no installation candidate

Monitorear el GPS

    sudo systemctl stop gpsd.socket
    sudo systemctl disable gpsd.socket
    sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

    gpsmon
    cgps

