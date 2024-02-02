# Python_driverTester

Repositório com os scripts gerados em Python e usados para o projeto da Giga de Teste dos drivers de iluminação. 


### Kivy isntallation Raspian 

Para instalar as dependências kivy 

```
$ sudo apt update
$ sudo apt install python3 python3-pip
$ apt-get -y install build-essential git make autoconf automake libtool \
      pkg-config cmake ninja-build libasound2-dev libpulse-dev libaudio-dev \
      libjack-dev libsndio-dev libsamplerate0-dev libx11-dev libxext-dev \
      libxrandr-dev libxcursor-dev libxfixes-dev libxi-dev libxss-dev libwayland-dev \
      libxkbcommon-dev libdrm-dev libgbm-dev libgl1-mesa-dev libgles2-mesa-dev \
      libegl1-mesa-dev libdbus-1-dev libibus-1.0-dev libudev-dev fcitx-libs-dev
$ apt-get install xorg wget libxrender-dev lsb-release libraspberrypi-dev raspberrypi-kernel-headers
$ python -m pip isntall kivy kivymd kivy-garden kivymd_extensions.akivymd kivymd_extensions.sweetalert
$ python -m pip install watchdog screeninfo 
$ python -m pip install pyserial
```

### Using Official RPi touch display

If you will use the official Raspberry Pi touch display, you need to configure Kivy to use it as an input source. To do this, edit the file ~/.kivy/config.ini and go to the [input] section. Add this:

```
$ mouse = mouse
$ mtdev_%(name)s = probesysfs,provider=mtdev
$ hid_%(name)s = probesysfs,provider=hidinput
```

### to build .exe with buildozer 
under construction 



