    RPi PWM Outputs:  12, 13, 18, 19
    Ardusimple Pins:  15, 14, 17, 24

- Encontrar proceso automático: `ps -fC python`
- Chequear undervoltage: `dmesg`
- Ver version: `cat /etc/os-release`



# Instalar RPi 

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
    git config --global user.name miguel2


### Ejecución automática:

    sudo crontab -e
    @reboot /usr/bin/python /home/pi/blink.py > /home/pi/blink.log 2>&1 &


### Debian GNU/Linux 12 (bookworm)

Python:

    sudo apt install git python3-pip
    pip3 install --break-system-packages navpy

### Debian GNU/Linux 11 (bullseye)

Python:

    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
    pip install navpy

### RPi3 with only 1.0 Gb RAM

Usar zram
    git clone https://github.com/foundObjects/zram-swap
    sudo ./install.sh

Overclock
    sudo watch "vcgencmd measure_temp && cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    sudo nano /boot/config.txt
        arm_freq=1400
        core_freq=500
        gpu_freq=500
        over_voltage=4
        sdram_freq=500
    sudo stressberry-run -n "My Test" -d 100 -i 30 -c 4 mytest1.dat


Agrandar SWAP (no necesario)
    sudo dphys-swapfile swapoff
    sudo nano /etc/dphys-swapfile
        CONF_SWAPSIZE=1024
    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
    sudo reboot

# Otros 

## Windows (testing)
    
    pip install RPi.GPIO

## Instalar str2str

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

### Para correr Str2str

    cd /home/luis/RTKLIB-rtklib_2.4.3/app/consapp/str2str/gcc/
    str2str -out serial://ttyACM0:115200:8:n:1:off -in ntrip://192.168.1.9:2101/TBO &

## Mapas servicio geografico UY

https://www.gub.uy/infraestructura-datos-espaciales/  
https://visualizador.ide.uy/ideuy/  
Chaja: G13A2, G13A3, G13A5, G13A6  
EPSG 5382

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

## Monitorear el GPS

    sudo systemctl stop gpsd.socket
    sudo systemctl disable gpsd.socket
    sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

    gpsmon
    cgps