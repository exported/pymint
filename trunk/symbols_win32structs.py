
from win32structs import *
from ctypes import *

SYMOPT_DEBUG = 0x80000000

SymGetOptions = windll.dbghelp.SymGetOptions
SymGetOptions.argtypes = []
SymGetOptions.restype = c_uint

SymSetOptions = windll.dbghelp.SymSetOptions
SymSetOptions.argtypes = [ c_uint ]
SymSetOptions.restype = c_uint

SymInitialize = windll.dbghelp.SymInitialize
SymInitialize.argtypes = [
		c_uint,		# HANDLE hProcess
		c_char_p,	# PCTSTR UserSearchPath
		c_uint ]	# BOOL fInvadeProcess
SymInitialize.restype = ErrorIfZero

SymLoadModule64 = windll.dbghelp.SymLoadModule64
SymLoadModule64.argtypes = [
		c_uint,		# HANDLE hProcess
		c_uint,		# HANDLE hFile
		c_char_p,	# PCSTR ImageNmae
		c_char_p,	# PCSTR ModuleName
		c_uint64,	# DWORD64 BaseOfDll
		c_uint ]	# SizeOfDll
SymLoadModule64.restype = c_uint64

class SYMBOL_INFO( Structure ):
	_fields_ = [
			('SuzeOfStruct',		c_uint),
			('TypeIndex',			c_uint),
			('reserved1',			c_uint64),
			('reserved2',			c_uint64),
			('Index',				c_uint),
			('Size',				c_uint),
			('ModBase',				c_uint64),
			('Flags',				c_uint),
			('Value',				c_uint64),
			('Address',				c_uint64),
			('Register',			c_uint),
			('Scope',				c_uint),
			('Tag',					c_uint),
			('NameLen',				c_uint),
			('MaxNameLen',			c_uint),
			('Name',				ARRAY(c_char, 0x1000)) ]
				
SYM_ENUMERATESYMBOLS_CALLBACK = WINFUNCTYPE( c_uint, POINTER(SYMBOL_INFO), c_uint, c_void_p )

SymEnumSymbols = windll.dbghelp.SymEnumSymbols
SymEnumSymbols.argtypes = [
		c_uint,		# HANDLE hProcess
		c_uint64,	# ULONG64 BaseOfDll
		c_char_p,	# PCTSTR Mask
		SYM_ENUMERATESYMBOLS_CALLBACK, # PSYM_ENUMERATESYMBOLS_CALLBACK EnumSymbolsCallback
		c_void_p ]	# PVOID UserContext
SymEnumSymbols.restype = ErrorIfZero

SymUnloadModule64 = windll.dbghelp.SymUnloadModule64
SymUnloadModule64.argtypes = [
		c_uint,		# HANDLE hProcess
		c_uint64 ]	# DWORD64 BaseOfDll
SymUnloadModule64.restype = ErrorIfZero

SymCleanup = windll.dbghelp.SymCleanup
SymCleanup.argtypes = [ c_uint ] # HANDLE hProcess
SymCleanup.restype = ErrorIfZero
