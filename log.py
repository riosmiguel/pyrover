import os, datetime, sys, time

class Transcript(object):
	isLineStart = True
	def write(self, message:str):
		self.terminal.write(message)
		self.terminal.flush()
		
		if(self.isLineStart):
			self.logfile.write(datetime.datetime.now().strftime('[%H:%M:%S] '))
			self.isLineStart = False
		self.logfile.write(message)
		self.logfile.flush()

		if(message.endswith('\n')):
			self.isLineStart = True
		
	def flush(self):
		self.terminal.flush()
		self.logfile.flush()
		pass

def inicializar():
	folder_name = 'logs'
	file_name = folder_name + '/log.txt'
	if not os.path.exists(folder_name): # crear carpeta logs si no existe
		os.makedirs(folder_name) 
	elif os.path.exists(file_name): # renombrar el archivo viejo si ya existe
		os.rename(file_name, datetime.datetime.now().strftime(file_name+'-%H-%M-%S.txt'))
	
	tr = Transcript()
	tr.terminal = sys.stdout
	tr.logfile = open(file_name, "w+")
	sys.stdout = tr

#### Codigo viejo:

# lock = threading.Lock()

# def print(nombre:str, valor, decimales:int=None): # imprime msg en la pantalla, guarda msg en el log_file y agrega un tab
# 	global file_log, nombres, linea_cnt, valores, lock
# 	with lock:

# 		if nombre in nombres:
# 			std_write('\r\n')
# 			file_write('\r\n')
# 			file_log.flush()
# 			nombres = []

# 		nombres.append(nombre)
# 		v = format(valor,decimales)
# 		std_write(v)
# 		#std_write('=', nombre, ' ')
# 		file_write(v)


# def print_msg(msg:str):
# 	global lock 
# 	time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S ")
# 	with lock:
# 		std_write("\r\n")
# 		std_write(time)
# 		std_write(msg)

# def std_write(*args):
# 	for a in args:
# 		sys.stdout.write(a)

# def file_write(*args):
# 	for a in args:
# 		file_log.write(a)

# def format(v, decimales=None):
# 	if isinstance(v, int):
# 		if(decimales==None): decimales=0
# 		v=float(v)

# 	if isinstance(v, float):
# 		if(decimales==None): decimales=2
# 		if(v>9999999999):
# 			s = "{:>10.5g}".format(v)
# 		else:
# 			s = '{:>10.{d}f}'.format(v,d=decimales)[:10]
# 	else:
# 		s = '{:>10}'.format(v)

# 	if(len(s)>10):
# 		s = s[:9]+"…" 

# 	return s