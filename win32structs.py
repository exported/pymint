# ImPoRtS

# Import win32con
class win32con( object ):
	def __init__( self ):
		pass
win32con.NULL = 0
win32con.TOKEN_QUERY					= 8
win32con.TOKEN_ADJUST_PRIVILEGES		= 32
win32con.PROCESS_QUERY_INFORMATION		= 1024
win32con.PROCESS_VM_READ				= 16
win32con.PROCESS_VM_WRITE				= 32
win32con.PROCESS_VM_OPERATION			= 8
win32con.PAGE_EXECUTE_READWRITE = 0x40

from ctypes import *

def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

TRUE = c_char( 	chr( int( True  ) ) )
FALSE = c_char( chr( int( False ) ) )
void_NULL = c_void_p( win32con.NULL )
pchar_NULL = c_char_p( win32con.NULL )

from win64structs import *

OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [
	c_uint,		# DWORD dwDesiredAccess
	c_int,		# BOOL bInheritHandle
	c_uint ]	# DWORD dwProcessId
OpenProcess.restype = ErrorIfZero

GetCurrentProcess = windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = ErrorIfZero

OpenProcessToken = windll.advapi32.OpenProcessToken
OpenProcessToken.argtypes = [
	c_void_p,	# HANDLE ProcessHandle
	c_uint,		# DWORD DesiredAccess
	c_void_p ]	# PHANDLE TokenHandle
OpenProcessToken.restype = ErrorIfZero

AdjustTokenPrivileges = windll.advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.argtypes = [
	c_void_p,	# HANDLE TokenHandle
	c_int,		# BOOL DisableAllPrivileges
	c_void_p,	# PTOKEN_PRIVILEGES NewState
	c_uint,		# DWORD BufferLength
	c_void_p,	# PTOKEN_PRIVILEGES PreviousState
	c_void_p ]	# PDWORD ReturnLength
AdjustTokenPrivileges.restype = ErrorIfZero

EnumProcessModules = windll.psapi.EnumProcessModules
EnumProcessModules.argtypes = [
	c_void_p,	# HANDLE hProcess
	c_void_p,	# HMODULE* lphModule
	c_uint,		# DWORD cb
	c_void_p ]	# LPDWORD lpcbNeeded
EnumProcessModules.restype = ErrorIfZero

EnumProcesses = windll.psapi.EnumProcesses
EnumProcesses.argtypes = [
    c_void_p,
    c_uint,
    c_void_p]
EnumProcesses.restype = ErrorIfZero

GetModuleBaseName = windll.psapi.GetModuleBaseNameA
GetModuleBaseName.argtypes = [
	c_void_p,	# HANDLE hProcess
	c_void_p,	# HMODULE hModule
	c_void_p,	# LPTSTR lpBaseName
	c_uint ]	# DWORD nSize
GetModuleBaseName.restype = ErrorIfZero

GetModuleInformation = windll.psapi.GetModuleInformation
GetModuleInformation.argtypes = [
	c_void_p,	# HANDLE hProcess
	c_void_p,	# HMODULE hModule
	c_void_p,	# LPMODULEINFO lpmodinfo
	c_uint ]	# DWORD cb
GetModuleInformation.restype = ErrorIfZero

GetProcessHeaps = windll.kernel32.GetProcessHeaps
GetProcessHeaps.argtypes = [
	c_uint,		# DWORD NumberOfHeaps
	c_void_p ]	# PHANDLE ProcessHeaps
GetProcessHeaps.restype = c_uint

HeapQueryInformation = windll.kernel32.HeapQueryInformation
HeapQueryInformation.argtypes = [
	c_void_p,	# HANDLE HeapHandle
	c_int,		# HEAP_INFORMATION_CLASS HeapInformationClass
	c_void_p,	# PVOID HeapInformation
	c_longlong,	# SIZE_T HeapInformationLength
	c_void_p ]	# PSIZE_T ReturnLength
HeapQueryInformation.restype = ErrorIfZero

HeapWalk = windll.kernel32.HeapWalk
HeapWalk.argtypes = [
	c_void_p,	# HANDLE hHeap
	c_void_p ]	# LPPROCESS_HEAP_ENTRY lpEntry
HeapWalk.restype = c_uint

LookupPrivilegeValue = windll.advapi32.LookupPrivilegeValueA
LookupPrivilegeValue.argtypes = [
	c_char_p,	# LPCTSTR lpSystemName
	c_char_p,	# LPCTSTR lpName
	c_void_p ]	# PLUID lpLuid
LookupPrivilegeValue.restype = ErrorIfZero

ReadProcessMemory = windll.kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [
	c_int,		# hProcess // handle to the process
	c_uint,		# lpBaseAddress // base of memory area
	c_void_p,	# lpBuffer // data buffer
	c_uint,		# nSize // number of bytes to read
	c_void_p]	# lpNumberOfBytesWritten // number of bytes write
ReadProcessMemory.restype = c_uint

WriteProcessMemory = windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [
	c_int,		# hProcess // handle to the process
	c_uint,		# lpBaseAddress // base of memory area
	c_void_p,	# lpBuffer // data buffer
	c_uint,		# nSize // number of bytes to read
	c_void_p]	# lpNumberOfBytesRead // number of bytes read
WriteProcessMemory.restype = ErrorIfZero

QueryWorkingSet = windll.psapi.QueryWorkingSet
QueryWorkingSet.argtypes = [
	c_void_p,	# HANDLE hProcess
	c_void_p,	# PVOID pv
	c_uint]		# DWORD cb
QueryWorkingSet.restype = ErrorIfZero

VirtualProtectEx = windll.kernel32.VirtualProtectEx
VirtualProtectEx.argtypes = [
	c_void_p,	# HANDLE
	c_void_p,	# Address
	c_uint,		# SIZE
	c_uint,		# Protection
	c_void_p ]	# Old protection
VirtualProtectEx.restype = ErrorIfZero

VirtualQueryEx = windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [
    c_int,      # HANDLE hProces
    c_void_p,   # LPCVOID lpAddress
    c_void_p,   # PMEMORY_BASIC_INFORMATION lpBuffer
    c_longlong ] # SIZE_T dwLength
VirtualQueryEx.restype = ErrorIfZero
	
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [ c_int ]
CloseHandle.restype = ErrorIfZero

class MODULEINFO( Structure ):
	_fields_ = [
			('lpBaseOfDll',		c_void_p),
			('SizeOfImage',		c_uint),
			('EntryPoint',		c_void_p) ]

class LUID( Structure ):
	_fields_ = [
			('LowPart',			c_uint),
			('HighPart',		c_uint)]

class TOKEN_PRIVILEGES( Structure ):
	_fields_ = [
			('PrivilegeCount',	c_uint),
			('Luid',			LUID),
			('Attributes',		c_uint) ]
	
class PROCESS_HEAP_ENTRY( Structure ):
	_fields_ = [
			('lpData',			c_void_p),
			('cbData',			c_uint),
			('cbOverhead',		c_byte),
			('iRegionIndex',	c_byte),
			('wFalgs',			c_uint16),
			('more_info1',		c_uint),
			('more_info2',		c_uint),
			('more_info3',		c_uint),
			('more_info4',		c_uint) ]

def DATA( data, base = 0 ):
	result = ''
	for i in xrange(0, len(data), 0x10):
		line = '%08X  ' % (i + base)
		line_data = data[i:][:0x10]
		for t in xrange(len(line_data)):
			if( 8 == t ):
				line += '- %02X' % ord(line_data[t])
			elif( 0 == (t & 1) ):
				line += '%02X' % ord(line_data[t])
			elif( 1 == (t & 1) ):
				line += '%02X ' % ord(line_data[t])
			
		line += ' ' * (55 - len(line))
		for t in line_data:
			if( t == `t`[1] ):
				line += t
			else:
				line += '.'
		line += '\n'
		result += line
	return( result )


