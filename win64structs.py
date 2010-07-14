# Imports  
from ctypes import *

def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

TRUE = c_char( 	chr( int( True  ) ) )
FALSE = c_char( chr( int( False ) ) )
void_NULL = c_void_p( 0 )
pchar_NULL = c_char_p( 0 )

IsWow64Process = windll.kernel32.IsWow64Process
IsWow64Process.argtypes = [
		c_int,
		c_void_p ]
IsWow64Process.restype = ErrorIfZero

GetCurrentProcess = windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = c_int



