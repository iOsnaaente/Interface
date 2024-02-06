### Virtualenv 

Para iniciar o virtual enviroment use `venv\Scripts\activate` no windows ou `source venv\bin\activate` no linux. Se ao ativar o venv no windows, receber a mensagem de erro como:
```
$ venv\Scripts\activate
> .\venv\Scripts\activate
>       + CategoryInfo          : ErrodeSegurança: (:) [], PSSecurityException
>       + FullyQualifiedErrorId : UnauthorizedAccess
> venv\Scripts\activate : O arquivo D:~\venv\Scripts\Activate.ps1 não pode ser carregado porque a execução de scripts   
> foi desabilitada neste sistema. Para obter mais informações, consulte about_Execution_Policies 
```
Pode-se executar o comando `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` para habilitar a execução do ambiente virtual.


# Python_driverTester

Repositório com os scripts gerados em Python e usados para o projeto da Giga de Teste dos drivers de iluminação. 


### Kivy isntallation Raspian 

Para instalar as dependências kivy 

```
# Instalação do python 
$ sudo apt update
$ sudo apt install python3 python3-pip


# Dependencias para o Raspberry Pi 4 
$ apt-get -y install build-essential git make autoconf automake libtool \
      pkg-config cmake ninja-build libasound2-dev libpulse-dev libaudio-dev \
      libjack-dev libsndio-dev libsamplerate0-dev libx11-dev libxext-dev \
      libxrandr-dev libxcursor-dev libxfixes-dev libxi-dev libxss-dev libwayland-dev \
      libxkbcommon-dev libdrm-dev libgbm-dev libgl1-mesa-dev libgles2-mesa-dev \
      libegl1-mesa-dev libdbus-1-dev libibus-1.0-dev libudev-dev fcitx-libs-dev
$ apt-get install xorg wget libxrender-dev lsb-release libraspberrypi-dev raspberrypi-kernel-headers

# Instalações das dependecias do framework Kivy 
python -m pip install kivy kivymd kivy-garden kivymd_extensions.akivymd kivymd_extensions.sweetalert kivygo 
python -m pip install watchdog screeninfo importlib 
python -m pip install pyserial
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



