import numpy as np
from math import sqrt
import time


class SpessoreAirfoil:
    def __init__(self, file):
        # Read the file
        with open(file, 'r') as f:
            lines = f.readlines()

        # Parse the data and remove the first row
        data = [line.strip().split() for line in lines[1:]]

        # Convert strings to floats
        data = [(float(row[0]), float(row[1])) for row in data]

        # Calculate the midpoint index
        self.l = len(data) // 2

        # Split the data into two lists
        self.sopra = list(reversed(data[:self.l]))
        self.sotto = list(data[self.l:])
        self.linea_media = [((self.sopra[i][0] + self.sotto[i][0]) / 2, (self.sopra[i][1] + self.sotto[i][1]) / 2) for i in range(self.l)]

    def get_spessore(self):
        dist = []
        d1,d2 = -1,-1     

        m_sopra = [self.m(self.sopra[i], self.sopra[i+1]) for i in range(self.l-1)]
        m_sotto = [self.m(self.sotto[i], self.sotto[i+1]) for i in range(self.l-1)]

        for i in range(self.l - 1):
        	xP, yP = (self.linea_media[i][0] + self.linea_media[i+1][0])/2, (self.linea_media[i][1] + self.linea_media[i+1][1])/2
        	mP = -1/self.m(self.linea_media[i], self.linea_media[i+1])

        	for j in range(self.l-1):
        		xA, yA = self.sopra[j][0], self.sopra[j][1]
        		xB, yB = self.sopra[j+1][0], self.sopra[j+1][1]
        		mA = self.m([xA,yA], [xB,yB])
        		xI = (yA - yP + xP * mP - xA * mA) / (mP - mA) 
        		yI = mA*(xI-xA)+yA
        		if (xA < xI < xB and yA < yI < yB or yB < yI < yA) or (xB < xI < xA and yA < yI < yB or yB < yI < yA):
        			d1 = self.dist([xP,yP], [xI, yI])

        	for j in range(self.l-1):
        		xA, yA = self.sotto[j][0], self.sotto[j][1]
        		xB, yB = self.sotto[j+1][0], self.sotto[j+1][1]
        		mA = self.m([xA,yA], [xB,yB])
        		xI = (yA - yP + xP * mP - xA * mA) / (mP - mA) 
        		yI = mA*(xI-xA)+yA
        		if (xA < xI < xB and yA < yI < yB or yB < yI < yA) or (xB < xI < xA and yA < yI < yB or yB < yI < yA):
        			d2 = self.dist([xP,yP], [xI, yI])

        	dist.append(d1+d2)
        return max(dist)

    def m(self, A, B):
        try:
            return (A[1] - B[1]) / (A[0] - B[0])
        except ZeroDivisionError:
            return 0#(A[1] - B[1]) / (A[0] - B[0] + 0.0001)

    def dist(self, A, B):
        return sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

if __name__ == '__main__':

    st = time.time()
    a = SpessoreAirfoil("airfoil.dat")
    print(a.get_spessore(), time.time()-st)

    st = time.time()
    a = SpessoreAirfoil("airfoil2.dat")
    print(a.get_spessore(), time.time()-st)

    st = time.time()
    a = SpessoreAirfoil("ag19.dat")
    print(a.get_spessore(), time.time()-st)
