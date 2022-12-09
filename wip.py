esptool.py --port /dev/tty.wchusbserial1410 erase_flash

esptool.py --port /dev/tty.wchusbserial1410 --baud 460800 write_flash --flash_size=detect 0 esp8266-20200911-v1.13.bin

screen /dev/tty.wchusbserial1410 115200


