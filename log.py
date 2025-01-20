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