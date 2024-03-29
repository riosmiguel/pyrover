import os, datetime, sys, threading

def inicializar():
	global file_log
	std_write('\033[2J') # Clear screen
	std_write('\033[1;1H') # Move cursor to home
	std_write('Inicializando','\r\n')
	std_write('\r\n')
	std_write('...','\r\n')
	std_write('\033[4;r') # Freeze 3 top lines
	std_write('\033[4;1H') # Move cursor to log

	folder_name = 'logs'
	file_name = folder_name + '/log.txt'
	if not os.path.exists(folder_name): # crear carpeta logs si no existe
		os.makedirs(folder_name) 
	elif os.path.exists(file_name): # renombrar el archivo viejo si ya existe
		os.rename(file_name, datetime.datetime.now().strftime(file_name+'-%H-%M-%S.txt'))

	file_log = open(file_name, 'w+')

nombres = []
valores = []
linea_cnt = 0
lock = threading.Lock()

def print(nombre:str, valor, decimales:int=None): # imprime msg en la pantalla, guarda msg en el log_file y agrega un tab
	global file_log, nombres, linea_cnt, valores, lock
	with lock:

		if nombre in nombres:
			std_write('\r\n')
			std_write('\0337') # Save cursor position
			std_write('\033[3;1H') # Move cursor to headers position
			
			for n in nombres:
				std_write(format(n), ' ')
			
			std_write('\0338') # Restore cursor position

			if(linea_cnt % 100 == 0):
				for n in nombres:
					file_write(format(n), ',')
				file_write('\r\n')

			for s in valores:
				file_write(s, ',')
			file_write('\r\n')
		
			linea_cnt = linea_cnt + 1
			nombres = []
			valores = []
		
		v = format(valor,decimales)
		nombres.append(nombre)
		valores.append(v)
		std_write(v, ' ')

def print_msg(msg:str):
	global lock 
	time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S ")
	with lock:
		std_write("\r\n")
		std_write(time)
		std_write(msg)
		std_write('\0337') # Save cursor position
		std_write('\033[1;1H') # Move cursor to status position
		std_write(time)
		std_write(msg[:80].replace('\n',' ').replace('\r',''))
		std_write('\0338') # Restore cursor position

def std_write(*args):
	for a in args:
		sys.stdout.write(a)

def file_write(*args):
	for a in args:
		file_log.write(a)

def writeLineEnd():
	sys.stdout.write("\r\n")
	file_log.write("\r\n")
	file_log.flush()

def format(v, decimales=None):
	if isinstance(v, int):
		if(decimales==None): decimales=0
		v=float(v)

	if isinstance(v, float):
		if(decimales==None): decimales=2
		if(v>9999999999):
			s = "{:>10.5g}".format(v)
		else:
			s = '{:>10.{d}f}'.format(v,d=decimales)[:10]
	else:
		s = '{:>10}'.format(v)

	if(len(s)>10):
		s = s[:9]+"…" 

	return s