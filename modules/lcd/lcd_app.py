import modules.lcd.I2C_LCD_driver as LCD
from time import *

def tulis_lcd(mylcd, tulisan, posisi):
	mylcd.lcd_display_string(tulisan, posisi)

def hapus_lcd(mylcd):
	mylcd.lcd_clear()

def get_lcd():
	return LCD.lcd()

if __name__ == '__main__':
	try:

		mylcd = LCD.lcd()

		while True:
			tulis_lcd(mylcd, "Hallo", 1)
			tulis_lcd(mylcd, "Testing", 2)
			sleep(1.0)
			hapus_lcd(mylcd)
			sleep(1.0)
			tulis_lcd(mylcd, "LCD", 1)
			tulis_lcd(mylcd, "Testing", 2)
			sleep(1.0)
			hapus_lcd(mylcd)
			sleep(1.0)
			tulis_lcd(mylcd, "Font", 1)
			tulis_lcd(mylcd, "Testing", 2)
			sleep(1.0)


	except KeyboardInterrupt:

		print("[INFO] WIPE PIN...")