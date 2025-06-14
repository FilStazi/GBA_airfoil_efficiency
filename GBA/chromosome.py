from pathlib import Path
import numpy as np
from math import pi, sqrt
from shapely.geometry import LineString

try:
    import GBA.gestione_xfoil as gestione_xfoil
    import GBA.spessore_airfoil as spessore_airfoil
    import GBA.bezier_curve as bezier_curve
except:
    import gestione_xfoil
    import spessore_airfoil
    import bezier_curve

class Chromosome:
    def __init__(self, path, nome, Re, AOA, c, th_min, upper_nodes, lower_nodes):
        self.nome = nome
        self.file = Path(path, nome + ".dat")
        self.re, self.aoa, self.c, self.th_min = Re, AOA, c, th_min #/, °, mm, mm
        self.b = 3400 #mm
        self.upper_nodes, self.lower_nodes = upper_nodes, lower_nodes

        self.upper = bezier_curve.BezierCurve(self.upper_nodes[0], self.upper_nodes[1]).get_cardinal_coordinates()
        self.lower = bezier_curve.BezierCurve(self.lower_nodes[0], self.lower_nodes[1]).get_cardinal_coordinates()
        self.x_airfoil = np.append(self.upper[0][::-1], self.lower[0])
        self.y_airfoil = np.append(self.upper[1][::-1], self.lower[1])
        self.combined_coordinates = (self.x_airfoil, self.y_airfoil)
        self.generate_dat_file(self.combined_coordinates)

        self.convergence = True
        self.thickness = spessore_airfoil.SpessoreAirfoil(self.file).get_spessore()
        self.fitness = -1

        if self.thickness * self.c > self.th_min and self.check_airfoil(self.upper, self.lower): 
            self.fitness = self.calculate_fitness()
        if self.fitness < 6:
            self.convergence = False



    def check_intersection(self, x1, y1, x2, y2):
        line1 = LineString(list(zip(x1, y1)))
        line2 = LineString(list(zip(x2, y2)))
        return line1.intersects(line2)

    def check_airfoil(self, upper, lower):
        x_upper, y_upper = upper[0], upper[1]
        x_lower, y_lower = lower[0], lower[1]

        l = len(x_upper)
        flag = True
        camber = [(y_upper[i] + y_lower[i]) / 2 for i in range(l)]

        for i in range(l):
            if camber[i] < 0:
                flag = False
                break
        if self.check_intersection(x_upper[1:-1], y_upper[1:-1], x_lower[1:-1], y_lower[1:-1]):
            flag = False
        return flag

    #GENERATE .dat FILE 
    def generate_dat_file(self, data):
        with open(self.file, "w") as f:
            f.write(self.nome + '\n')
            data = list(zip(*data))
            for i in data:
                f.write(str(i[0]) + ' ' + str(i[1]) + '\n')

    #GETS COEFFICIENT FORM XFOIL
    def get_coefficients(self, re):
        x = gestione_xfoil.Xfoil(self.file)
        cl, cd = x.execute_analysis(re, self.aoa)
        #print(cl,cd)
        return cl, cd

    #AIRFOIL FITNESS
    def calculate_fitness(self):
        cl, cd = gestione_xfoil.Xfoil(self.file).execute_analysis(self.re, self.aoa)
        #print(cl,cd)
        if cl < 0 or cl > 2 or cd < 0.004: return -1 
        #else: return cd*1000
        else: return 1000 * cd / cl
        #else: return 1000000000*abs(cl-1.2)*cd
        
        
if __name__ == '__main__':
    #xn, yn, xs, ys, aoa, corda, spess_min, apertura, v_iniziale
    a = Chromosome("", "naca2414.dat", 300000, 2, 0.2, [0, 0.2, 0.4, 0.8, 1], [0, -0.2, -0.15, -0.05, 0])
    print(a.fitness)