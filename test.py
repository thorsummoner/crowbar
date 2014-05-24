#!/c/Python34x32/python.exe

from lib.Extensions import Extensions
from crowbar.crowbar import crowbar

# statusbar = Extensions('StatusBar')

if '__main__' == __name__:
	app = crowbar()
	app.main()


