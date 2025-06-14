import os, sys
import subprocess
import numpy as np
from pathlib import Path
import re	

import threading
import time

class Xfoil:
	def __init__(self, file):
		self.file = file
		self.n_iter = 100
		self.ok = 0

	def my_thread(self):
		time.sleep(0.5)
		if self.ok == 0:
			try: os.system("taskkill /f /im xfoil.exe > NUL")
			except: pass

	#---ESECUZIONE ANALISI XFOIL, 1 AOA
	def execute_analysis(self, Re, alpha_aoa):

	    input_file = open("input_file.in", 'w')
	    input_file.write("PLOP\n")
	    input_file.write("G\n\n")
	    input_file.write("LOAD " + str(self.file) + "\n")
	    input_file.write("PPAR\n")
	    input_file.write("N\n")
	    input_file.write("100\n\n\n")
	    input_file.write("PANE\n")
	    input_file.write("OPER\n")
	    input_file.write("Visc {0}\n".format(Re))
	    input_file.write("PACC\n")
	    input_file.write("polar_file.txt\n\n")
	    input_file.write("ITER 100\n")
	    input_file.write("alfa {0}\n".format(alpha_aoa)) # occhio agli alfa negativi
	    input_file.write("\n\n")
	    input_file.write("quit\n")
	    input_file.close()		    

	    self.ok = 0

	    # Start the thread
	    t = threading.Thread(target=self.my_thread)
	    t.start()

	    subprocess.call("xfoil.exe < input_file.in > NUL", shell=True)
	    self.ok = 1

	    return self.get_polars()


	#---LA FUNZIONE RESTITUISCE I COEFFICIENTI DI LIFT E DI ATTRITO GENERATI CON XFOIL
	def get_polars(self):

		#---LETTURA FILE GENERATO
		try:
			with open(Path("","polar_file.txt"), "r") as f:
				for i in range(12): # salto le prime 12
					d = f.readline()
				polar_data = f.readline()
		except:
			return -1, -1
		# extract float numbers using regular expression
		numbers = re.findall(r"[-+]?\d*\.\d+|\d+", polar_data)
		# convert the resulting list of strings to a list of floats
		numbers = [float(x) for x in numbers]
		#---IN CASO DI NON CONVERGENZA LA FUNZIONE TORNA -1 -1
		cl, cd = -1, -1
		#---CONTROLLO CONVERGENZA
		if len(numbers) == 7:
			cl = numbers[1]
			cd = numbers[2]
			
		#---PULIZIA FILE
		#os.remove(self.file)
		os.remove("input_file.in")
		os.remove("polar_file.txt")
		return cl, cd

if __name__ == '__main__':
	x = Xfoil("naca2414.dat")
	print(x.execute_analysis(300000, 2))