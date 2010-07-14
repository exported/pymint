
from distutils.core import setup
setup(
	name = 'Mint',
	version = '1.0',
	description = 'Win32 Debugger controled from Python interpreter',
	author = 'Assaf Nativ',
	author_email = 'Nativ.Assaf@gmail.com',
	packages = ['mint'],
	package_dir = {'mint' : ''},
	data_files = [('Lib\\\site-packages', ('mint.pth',))]
	)


