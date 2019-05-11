from winrecon.cf.sid import SID

class FileInfo:
	def __init__(self):
		self.fid = None
		self.permissions = None
		self.num_locks = None
		self.pathname = None
		self.username = None
		
	@staticmethod
	def from_struct(si, level):
		sess = FileInfo()
		sess.fid = si.fid
		if level == 2:
			return sess
		sess.permissions = si.permissions
		sess.num_locks = si.num_locks
		sess.pathname = si.pathname
		sess.username = si.username
		
		return sess
		
	def __str__(self):
		t = '==ShareInfo==\r\n'
		t+= 'netname : %s\r\n' % self.netname
		if self.path:
			t+= 'path : %s\r\n' % self.path
		if self.remark:
			t+= 'remark : %s\r\n' % self.remark
		return t
		
class ShareInfo:
	def __init__(self):
		self.flags = None
		self.netname = None
		self.type = None
		self.remark = None
		self.permissions = None
		self.max_uses = None
		self.current_uses = None
		self.path = None
		self.passwd = None
		self.servername = None
		
	@staticmethod
	def from_struct(si, level):
		sess = ShareInfo()
		sess.netname = si.netname
		if level == 0:
			return sess
		sess.type = si.type
		sess.remark = si.remark
		if level == 1:
			return sess
		
		if level == 501:
			sess.flags = si.flags
			return sess
		
		
		sess.permissions = si.permissions
		sess.max_uses = si.max_uses
		sess.current_uses = si.current_uses
		sess.path = si.path
		sess.passwd = si.passwd
		
		if level != 503:
			return sess
			
		sess.servername = si.servername
		return sess
		
	def __str__(self):
		t = '==ShareInfo==\r\n'
		t+= 'netname : %s\r\n' % self.netname
		if self.path:
			t+= 'path : %s\r\n' % self.path
		if self.remark:
			t+= 'remark : %s\r\n' % self.remark
		return t

class UserSessionInfo:
	def __init__(self):
		self.computername = None
		self.username = None
		self.time = None
		self.idle_time = None
		
	@staticmethod
	def from_session_info(si, level):
		sess = UserSessionInfo()
		sess.computername = si.cname.replace('\\\\','')
		if level == 0:
			return sess
		
		sess.computername = si.cname
		sess.username = si.username
		sess.time = si.time
		sess.idle_time = si.idle_time
		return sess
		
	def __str__(self):
		t = '==Session==\r\n'
		t+= 'computername : %s\r\n' % self.computername
		t+= 'username : %s\r\n' % self.username
		t+= 'time : %s\r\n' % self.time
		t+= 'idle_time : %s\r\n' % self.idle_time
		return t
		
class LocalGroupInfo:
	def __init__(self):
		self.sid = None
		self.sidusage = None
		self.domain = None
		self.username = None

	def from_struct(lg, level):
		lgi = LocalGroupInfo()
		if level == 0:
			lgi.sid = SID.from_address(lg.sid)
			return lgi
		
		elif level == 1:
			lgi.sid = SID.from_address(lg.sid)
			lgi.sidusage = lg.sidusage
			lgi.username = lg.name
			return lgi
			
		elif level == 2:
			lgi.sid = SID.from_address(lg.sid)
			lgi.sidusage = lg.sidusage
			lgi.domain, lgi.username = lg.domainandname.split('\\')
			return lgi
		
		elif level == 3:
			lgi.sid = SID.from_address(lg.sid)
			lgi.sidusage = lg.sidusage
			lgi.domain, lgi.username = lg.domainandname.split('\\')
			return lgi
		else:
			raise Exception('Unknown struct of type %s passed to LocalGroupInfo' % (type(lg)))
			
	def __str__(self):
		t = '==LocalGroupInfo==\r\n'
		t+= 'sid : %s\r\n' % self.sid
		t+= 'sidusage : %s\r\n' % self.sidusage
		t+= 'domain : %s\r\n' % self.domain
		t+= 'username : %s\r\n' % self.username
		return t