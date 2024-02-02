Preparando o ambiente
Esse passo a passo é para o Raspbian Jessie versão 2016-03-18 (download), versões após esta release estão com problemas na interface SPI, e versões do Wheezy não suportam Device Tree, usado no exemplo abaixo. Leia mais sobre Device Tree na documentação do Raspberry. Caso você deseje configurar outra versão do Raspbian siga o tutorial da documentação do SPI.

O Raspbian vem com SPI desabilitado por padrão, para verificar se está ou não habilitado vamos executar o comando a seguir:
& ls /dev/spi*

Se o resultado for o seguinte:
> ls: cannot access /dev/spi*: No such file or directory

Em seguida, no seu editor de texto preferido abra o arquivo /boot/config.txt (como root) e adicione a seguinte linha:
& dtoverlay=spi-bcm2708

Reinicie o Raspbian e verifique novamente, o resultado deverá ser:

/dev/spidev0.0 /dev/spidev0.1

Verifique se o módulo SPI foi carregado corretamente através do comando:

& dmesg | grep spi
O resultado deverá ser algo semelhante ao abaixo, indicando a comunicação RFID com Raspberry Pi:

1
2
[ 6.240564] bcm2708_spi 3f204000.spi: master is unqueued, this is deprecated
[ 6.241262] bcm2708_spi 3f204000.spi: SPI Controller at 0x3f204000 (irq 80)
Para utilizar o módulo RC522 no Python necessitamos instalar alguns componentes antes de começar a programar. Primeiramente iremos instalar o pacote python-dev através do comando:

1
sudo apt-get install python-dev
Após instalado iremos instalar o pacote Python para comunicação SPI, para isto execute os comandos abaixo:

1
2
3
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install