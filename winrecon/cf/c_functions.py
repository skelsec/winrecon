from defines import *
import enum
import datetime
import ctypes

LMSTR = LPSTR
MAX_PREFERRED_LENGTH = 2048

class SESSION_INFO_10(Structure): 
	_fields_ = [
		('cname',LMSTR),
		('username',LMSTR),
		('time',DWORD),
		('idle_time',DWORD)
	]
PSESSION_INFO_10 = POINTER(SESSION_INFO_10)
	
class NetSessionEnumRes(enum.Enum):
	ERROR_ACCESS_DENIED = 5
	ERROR_INVALID_LEVEL = 124
	ERROR_INVALID_PARAMETER = 87
	ERROR_NOT_ENOUGH_MEMORY = 8
	NERR_ClientNameNotFound = 2312
	NERR_InvalidComputer = (2100 + 251)
	ERROR_FILE_NOT_FOUND = 2
	NERR_FileIdNotFound = 2314
	NERR_SUCCESS= 0
	ERROR_MORE_DATA = 234

# https://docs.microsoft.com/en-us/windows/desktop/api/lmshare/nf-lmshare-netsessionenum
def NetSessionEnum(servername = None, clientname = None, username = None, level = 10):
	def errc(result, func, arguments):
		r = NetSessionEnumRes(result)
		if r == NetSessionEnumRes.NERR_SUCCESS or r == NetSessionEnumRes.ERROR_MORE_DATA:
			return r
		raise Exception('NetSessionEnum exception! %s' % r)
		
	_NetSessionEnum = windll.Netapi32.NetSessionEnum
	_NetSessionEnum.argtypes = [LMSTR, LMSTR, LMSTR, DWORD, PVOID, DWORD, LPDWORD ,LPDWORD , LPDWORD ]
	_NetSessionEnum.restype  = DWORD
	_NetSessionEnum.errcheck  = errc
	
	if level == 10:
		buf = (SESSION_INFO_10*100)()
	else:
		buf = ctypes.create_string_buffer(MAX_PREFERRED_LENGTH)
		buf = ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte))
	entriesread = DWORD()
	totalentries = DWORD()
	resume_handle = DWORD()
	
	
	if servername:
		servername = LPSTR(servername.encode('utf-16-le')+b'\x00')
	if clientname:
		clientname = LPSTR(clientname.encode('utf-16-le')+b'\x00')
	if username:
		username = LPSTR(username.encode('utf-16-le')+b'\x00')
	
	
	res = _NetSessionEnum(servername, clientname, username, level, byref(buf), sizeof(buf), byref(entriesread), byref(totalentries), byref(resume_handle))
	
	if level == 10:
		SESSION_INFO_10
	print(entriesread.value)
	print(totalentries.value)
	print(resume_handle.value)
	print(buf[0].cname)
	print(res)
	
	return data
	
if __name__ == '__main__':
	creds = None
	#target = 'krbtgt@TEST'
	#target = 'srv_http@TEST.corp'
	target = 'WIN2019AD'
	
	#NetSessionEnum()
	NetSessionEnum(target)
	