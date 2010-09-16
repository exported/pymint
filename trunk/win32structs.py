# ImPoRtS

# Import win32con
class win32con( object ):
	def __init__( self ):
		pass
win32con.NULL = 0
win32con.TOKEN_QUERY					= 8
win32con.TOKEN_ADJUST_PRIVILEGES		= 32
win32con.PROCESS_VM_OPERATION			= 8
win32con.PROCESS_VM_READ				= 16
win32con.PROCESS_VM_WRITE				= 32
win32con.PROCESS_DUP_HANDLE             = 64
win32con.PROCESS_QUERY_INFORMATION		= 1024
win32con.PAGE_EXECUTE_READWRITE         = 0x40
win32con.ObjectBasicInformation         = 0
win32con.ObjectNameInformation          = 1
win32con.ObjectTypeInformation          = 2
win32con.ObjectAllTypesInformation      = 3
win32con.ObjectHandleInformation        = 4
win32con.STATUS_SUCCESS                 = 0x00000000
win32con.STATUS_INFO_LENGTH_MISMATCH    = 0xc0000004
win32con.STATUS_BUFFER_OVERFLOW         = 0x80000005
win32con.SystemHandleInformation        = 16
win32con.STANDARD_RIGHTS_REQUIRED       = 0x000f0000

from ctypes import *

def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

def NtStatusCheck(ntStatus):
    if ntStatus < 0 or ntStatus > 0x80000000:
        raise WinError()
    else:
        return ntStatus

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

class UNICODE_STRING( Structure ):
    _fields_ = [
            ('Length',          c_uint16),
            ('MaximumLength',   c_uint16),
            ('Buffer',          c_wchar_p) ]

class OBJECT_BASIC_INFORMATION( Structure ):
    _fields_ = [
            ('Attributes',          c_uint),
            ('DesiredAccess',       c_uint),
            ('HandleCount',         c_uint),
            ('ReferenceCount',      c_uint),
            ('PagedPoolUsage',      c_uint),
            ('NonPagedPoolUsage',   c_uint),
            ('Reserved',            c_uint * 3),
            ('NameInformationLength',   c_uint),
            ('TypeInformationLength',   c_uint),
            ('SecurityDescriptorLength',    c_uint),
            ('CreationTime',        c_ulonglong) ]

class OBJECT_NAME_INFORMATION( Structure ):
    _fields_ = [
            ('UnicodeStr',      UNICODE_STRING) ]
            

class GENERIC_MAPPING( Structure ):
    _fields_ = [
            ('GenericRead',     c_uint),
            ('GenericWrite',    c_uint),
            ('GenericExecute',  c_uint),
            ('GenericAll',      c_uint)]

class OBJECT_TYPE_INFROMATION( Structure ):
    _fields_ = [
            ('TypeName',                UNICODE_STRING),
            ('TotalNumberOfHandles',    c_uint),
            ('TotalNumberOfObjects',    c_uint),
            ('Unused1',                 c_uint16*8),
            ('HighWaterNumberOfHandles',    c_uint),
            ('HighWaterNumberOfObjects',    c_uint),
            ('Unused2',                 c_uint16*8),
            ('InvalidAttributes',       c_uint),
            ('GenericMapping',          GENERIC_MAPPING),
            ('ValidAttributes',         c_uint),
            ('SecurityRequired',        c_int),
            ('MaintainHandleCount',     c_int),
            ('MaintainTypeList',        c_uint16),
            ('PoolType',                c_uint),
            ('DefaultPagedPoolCharge',  c_uint),
            ('DefaultNonPagedPoolCharge',   c_uint) ]

DuplicateHandle = windll.kernel32.DuplicateHandle
DuplicateHandle.argtypes = [
    c_int,      #  __in   HANDLE hSourceProcessHandle,
    c_int,      #  __in   HANDLE hSourceHandle,
    c_int,      #  __in   HANDLE hTargetProcessHandle,
    c_void_p,   #  __out  LPHANDLE lpTargetHandle,
    c_uint,     #  __in   DWORD dwDesiredAccess,
    c_int,      #  __in   BOOL bInheritHandle,
    c_uint ]    #  __in   DWORD dwOptions
DuplicateHandle.restype = ErrorIfZero


NtQueryObject = windll.ntdll.NtQueryObject
NtQueryObject.argtypes = [
    c_void_p,   #  __in_opt   HANDLE Handle,
    c_uint,     #  __in       OBJECT_INFORMATION_CLASS ObjectInformationClass,
    c_void_p,   #  __out_opt  PVOID ObjectInformation,
    c_uint,     #  __in       ULONG ObjectInformationLength,
    c_void_p ]  #  __out_opt  PULONG ReturnLength
NtQueryObject.restype = c_uint

NtQuerySystemInformation = windll.ntdll.NtQuerySystemInformation
NtQuerySystemInformation.argtypes = [
    c_void_p,   #  __in       SYSTEM_INFORMATION_CLASS SystemInformationClass,
    c_void_p,   #  __inout    PVOID SystemInformation,
    c_uint,     #  __in       ULONG SystemInformationLength,
    c_void_p ]  #  __out_opt  PULONG ReturnLength
NtQuerySystemInformation.restype = c_uint
    

GetModuleFileNameEx = windll.psapi.GetModuleFileNameExA
GetModuleFileNameEx.argtypes = [
        c_int,      #  __in      HANDLE hProcess,
        c_uint,     #  __in_opt  HMODULE hModule,
        c_void_p,   #  __out     LPTSTR lpFilename,
        c_uint ]    #  __in      DWORD nSize
GetModuleFileNameEx.restype = ErrorIfZero

class SYSTEM_HANDLE( Structure ):
    _fields_ = [
            ('uIdProcess',  c_uint),
            ('ObjectType',  c_byte),
            ('Flags',       c_byte),
            ('Handle',      c_uint16),
            ('object',      c_void_p),
            ('GrantedAccess',   c_uint) ]

class SYSTEM_HANDLE_INFORMATION( Structure ):
    _fields_ = [
            ('uCount',      c_uint),
            ('Handle',      SYSTEM_HANDLE) ]

class SYSTEM_HANDLE_INFORMATION( Structure ):
    _fields_ = [
            ('uCount',          c_uint),
            ('SystemHandle',    SYSTEM_HANDLE) ]

