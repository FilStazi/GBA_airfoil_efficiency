import math, time
import numpy as np
import os
from pathlib import Path
from random import uniform, random, randint
from statistics import variance

import matplotlib
import matplotlib.pyplot as plt

try:
	import GBA.chromosome as chromosome
except:
	import chromosome

class GeneticBasedAlgorithm:

	def __init__(self, dim_pop, num_gen):
		self.dim_pop, self.num_gen = int(dim_pop), int(num_gen)

		self.re = 300000

		#Decide how much of the previous population goes to the nex by elitism
		self.elitism_rate = 0.25
		self.elites = int(self.dim_pop * self.elitism_rate)

		self.aoa_min, self.aoa_max = 0, 5
		self.c = 250 
		self.th_min = 20 #mm

		self.count = 0 #serve per il file "fit.txt"

		self.scia = []

	def generatete_random_airfoil(self):#ESTRADOSSO
		x_upper = sorted([0, 0, uniform(0,1), uniform(0,1), 1])
		y_upper = [0, uniform(0,0.2), uniform(0,0.2), uniform(0,0.2), 0]
		x_lower = sorted([0, 0, uniform(0,1), uniform(0,1), 1])
		y_lower = [0, uniform(-0.2,0), uniform(-0.2,0.1), uniform(-0.2,0.1), 0]

		return (x_upper, y_upper), (x_lower, y_lower)

	def generate_file_name(self, p, g): #formattazione name file
		if p <= 9: name_file = "airfoil_" + str(g) + "_000" + str(p) #name file dat
		elif p <= 99: name_file = "airfoil_" + str(g) + "_00" + str(p) #name file dat
		elif p <= 999: name_file = "airfoil_" + str(g) + "_0" + str(p) #name file dat
		else: name_file = "airfoil_" + str(g) + "_" + str(p) #name file dat
		return name_file

	def rotate_point(self, x_l, y_l, angle):
		x_new, y_new = [], []
		"""Rotate a point by a given angle (in radians) around the origin."""
		for i in range(len(x_l)):
			x, y = x_l[i], y_l[i]
			x_new.append(x * np.cos(angle) - y * np.sin(angle))
			y_new.append(x * np.sin(angle) + y * np.cos(angle))

		return x_new, y_new

	#CREAZIONE PLOT PER VIDEO FINALE
	def create_plot(self, p, g, individual):
		name_file = self.generate_file_name(p,g)
		fig, ax = plt.subplots()
		ax.set_xlim(0, 1)
		ax.set_ylim(-0.3, 0.3)
		ax.autoscale(False)
		aoa = np.radians(-1 * individual.aoa)
		l=30 if len(self.scia) > 30 else len(self.scia)
		for i, ind in enumerate(self.scia[-l:]):
			#print(ind.fitness)
			ax.plot(ind.x_airfoil, ind.y_airfoil, color=(0, 0, 0, (i+1)/l), label='profile', linewidth=0.5)
			#ax.scatter(ind.upper_nodes[0], ind.upper_nodes[1], color=(0, 0, 1, (i+1)/l), label='upper nodes', marker = 'x')
			#ax.scatter(ind.lower_nodes[0], ind.lower_nodes[1], color=(1, 0, 0, (i+1)/l), label='lower nodes', marker = 'x')
		ax.plot(individual.x_airfoil, individual.y_airfoil, color=(1, 0, 0, 1), label='profile', linewidth=1)
		#ax.scatter(individual.upper_nodes[0], individual.upper_nodes[1], color=(0, 0, 1, 1), label='upper nodes', marker = 'x')
		#ax.scatter(individual.lower_nodes[0], individual.lower_nodes[1], color=(1, 0, 0, 1), label='lower nodes', marker = 'x')
		with open(individual.file, 'r') as file:
		    next(file)  # Skip the first line
		    x, y = zip(*(map(float, line.split()[:2]) for line in file))
		folder_img = Path("Images", "generation_" + str(g))

		if g < 10: folder_img = Path("Images", "generation_00" + str(g))
		elif g < 100: folder_img = Path("Images", "generation_0" + str(g))
		else: folder_img = Path("Images", "generation_" + str(g))

		if not os.path.exists(folder_img): os.makedirs(folder_img)
		#plt.suptitle("Generation: " + str(g) + "   Number: " + str(p) + "   Fit: " + str(round(individual.fitness, 3)) + "\nAoa: " + str(round(individual.aoa,2)) + "   Chord: " + str(round(individual.c,3)) + "   Th (mm): " + str(round(individual.thickness*individual.c,3)))
		plt.suptitle("Generation: " + str(g) + "   Fit: " + str(round(individual.fitness, 3)) + "\nAoa: " + str(round(individual.aoa,2)) + "   Chord: " + str(round(individual.c,3)) + "   Th (mm): " + str(round(individual.thickness*individual.c,3)))
		#plt.legend()
		plt.savefig(Path(folder_img, name_file))
		matplotlib.pyplot.close()
		with open("fit.txt", "a") as f:
			f.write(str(self.count) + ' ' + str(round(individual.fitness, 3)) + ' ' + str(int(individual.aoa)) +  ' ' + str(round(individual.c, 3)) +'\n')
			self.count += 1

	def generation_0(self):
		print("Generation 0:")
		self.folder_dat = Path("Airfoil", "generation_" + str(0))
		if not os.path.exists(self.folder_dat): os.makedirs(self.folder_dat)
		
		population = []
		for p in range(self.dim_pop):
			print(p, end='\r')

			name_file = self.generate_file_name(p, 0)
			conv = False

			while not conv:
				upper_nodes, lower_nodes = self.generatete_random_airfoil()
				aoa = randint(self.aoa_min, self.aoa_max)

				individuals = chromosome.Chromosome(self.folder_dat, name_file, self.re, aoa, self.c, self.th_min, upper_nodes, lower_nodes) #generateting the chromosome
				conv = individuals.convergence

			population.append(individuals)
		
		self.last_time = time.time()

		population.sort(key=lambda x: x.fitness) #Ordino in base al fitness

		#for p, individual in enumerate(population):
		#	print("                   ", end = '\r')
		#	print(f"Image: {p}", end = '\r')
		self.create_plot(0, 0, population[0])
		self.scia.append(population[0])
		return population

	def elitism(self, population, g):
		population = population[:self.elites] #La peggiore metà la elimino
		for p, individual in enumerate(population):
			individual.file = Path(self.folder_dat, self.generate_file_name(p, g) + '.dat')
			individual.generate_dat_file(individual.combined_coordinates)
		return population #restituisco la list con dentro i cromosomi 

	def offspring(self, population, g):
		p = self.elites	
		# Calculate the sum of all numbers to use as a normalization factor
		total_fitness = sum(individual.fitness for individual in population[:p])
		# Calculate probabilities based on the relative size of each number
		probabilities = [individual.fitness / total_fitness for individual in population[:p]]

		#per tutti i posti disponibili nella generation successiva accoppio due elite random finchè il figlio non converge
		while p < int(self.dim_pop):
			print("Reproduction:", p, end = '\r')
			conv = False
			name_file = self.generate_file_name(p, g)
			while not conv:

				# Generate a random number between 0 and 1
				parent1_prob = random()
				parent2_prob = random()

				# Initialize the cumulative probability
				cumulative_prob = 0

				# Iterate through the numbers and select one based on the random number and its probability
				for i, prob in enumerate(probabilities):
				    cumulative_prob += prob
				    if parent1_prob < cumulative_prob:
				        parent1 = population[i]
				        break

				cumulative_prob = 0

				# Iterate through the numbers and select one based on the random number and its probability
				for i, prob in enumerate(probabilities):
				    cumulative_prob += prob
				    if parent2_prob < cumulative_prob:
				        parent2 = population[i]
				        break

				power1 = parent1.fitness / (parent1.fitness + parent2.fitness)
				power2 = parent2.fitness / (parent1.fitness + parent2.fitness)

				#il figlio viene generateto con punti generatetrici che sono media pesata tra l'i-esimo punto del primo parent e l'i-esimo punto del secondo
				upper_nodes = [(parent1.upper_nodes[0][i] * power1 + parent2.upper_nodes[0][i] * power2) for i in range(len(parent1.upper_nodes[0]))], [(parent1.upper_nodes[1][i] * power1 + parent2.upper_nodes[1][i] * power2) for i in range(len(parent1.upper_nodes[1]))]
				lower_nodes = [(parent1.lower_nodes[0][i] * power1 + parent2.lower_nodes[0][i] * power2) for i in range(len(parent1.lower_nodes[0]))], [(parent1.lower_nodes[1][i] * power1 + parent2.lower_nodes[1][i] * power2) for i in range(len(parent1.lower_nodes[1]))]
			
				aoa = int(parent1.aoa * power1 + parent2.aoa * power2)
				
				individual = chromosome.Chromosome(self.folder_dat, name_file, self.re, aoa, self.c, self.th_min, upper_nodes, lower_nodes) #generateting the chromosome
				conv = individual.convergence
	            
			p += 1
			population.append(individual)
		return population

	def mutation(self, population, g):
		mutated = []
		for p, individual in enumerate(population):
			print("                   ", end = '\r')
			print(f"Mutation: {p}", end = '\r')
			old = individual
			new = self.mutate(individual, p, g)
			if new.convergence and new.fitness < old.fitness:
				mutated.append(new)
			else:
				old.file = Path(self.folder_dat, self.generate_file_name(p, g) + ".dat")
				old.generate_dat_file(individual.combined_coordinates)
				mutated.append(old)
		return mutated

	def mutate(self, individual, p, g):
		upper_nodes, lower_nodes, aoa, c = individual.upper_nodes, individual.lower_nodes, individual.aoa, individual.c
		name_file = self.generate_file_name(p, g)
		flag = False
		for idx, i in enumerate(upper_nodes[0]):
			if idx != 0 and idx != 1 and idx != 4:
				upper_nodes[0][idx] += uniform(-0.01, 0.01)
			if idx != 0 and idx != 4:
				upper_nodes[1][idx] += uniform(-0.005, 0.005)
			if upper_nodes[0][idx] < 0: upper_nodes[0][idx] = 0
			if upper_nodes[0][idx] > 1: upper_nodes[0][idx] = 1

		for idx, i in enumerate(lower_nodes[0]):
			if idx != 0 and idx != 1 and idx != 4:
				lower_nodes[0][idx] += uniform(-0.01, 0.01)
			if idx != 0 and idx != 4:
				lower_nodes[1][idx] += uniform(-0.005, 0.005)
			if lower_nodes[0][idx] < 0: lower_nodes[0][idx] = 0
			if lower_nodes[0][idx] > 1: lower_nodes[0][idx] = 1
		if lower_nodes[1][1] > 0: lower_nodes[1][1] = 0

		def sort_both(x, y):
		    pairs = sorted(zip(x, y), key=lambda pair: pair[0])
		    return [list(coord) for coord in zip(*pairs)]

		upper_nodes_sorted = sort_both(*upper_nodes)
		lower_nodes_sorted = sort_both(*lower_nodes)

		r = uniform(0,1)
		if r < 0.5:
			aoa +=1
		elif 0.33 < r < 0.66:
			aoa -=1
		if aoa < self.aoa_min: aoa = self.aoa_min
		if aoa > self.aoa_max: aoa = self.aoa_max
		individual = chromosome.Chromosome(self.folder_dat, name_file, self.re, aoa, self.c, self.th_min, upper_nodes_sorted, lower_nodes_sorted) #generateting the chromosome
		return individual


	def generation_g(self, population, g):
		print("                   ", end = '\r')
		print(f"Generation {g}:")
		self.folder_dat = Path("Airfoil", "generation_" + str(g))
		if not os.path.exists(self.folder_dat): os.makedirs(self.folder_dat)
		population = self.elitism(population, g)
		population = self.offspring(population, g)
		if g < 0.95 * self.num_gen: population = self.mutation(population, g)
		population.sort(key=lambda x: x.fitness) #Ordino in base al fitness
		#for p, individual in enumerate(population):
		#	print("                   ", end = '\r')
		#	print(f"Image: {p}", end = '\r')
		self.create_plot(0, g, population[0])
		self.scia.append(population[0])
		return population

	def final_generation(self, population,g):
		print("Final generation:")
		self.folder_dat = Path("Airfoil", "generation_final")
		if not os.path.exists(self.folder_dat): os.makedirs(self.folder_dat)
		with open("ottimizzazzione.txt", "a") as f:
			f.write(str(g+1) + '\t' + str(round(population[0].fitness,3)) + '\t')
		for p, individual in enumerate(population):
			if p == 0:
				with open("time.txt", "w") as f:
					f.write(str(individual.fitness) + '\n')
			print(f"Image: {p}", end = '\r')
			individual.file = Path(self.folder_dat, self.generate_file_name(p, "final") + ".dat")
			individual.generate_dat_file(individual.combined_coordinates)
			#self.create_plot(p, "final", individual)
		return population

	def start(self):
		population = self.generation_0()
		best_fitness = float('inf')
		stall_count = 0

		for generation in range(1, self.num_gen):
		    population = self.generation_g(population, generation)
		    current_best_fitness = population[0].fitness

		    if current_best_fitness < best_fitness:
		        best_fitness = current_best_fitness
		        stall_count = 0
		    else:
		        stall_count += 1

		    print("                   ", end = '\r')
		    print(f"{round(current_best_fitness, 3)} - {stall_count}")

		    if stall_count > 30:
		        print("Reached stalled iteration limit")
		        break

		final_generation_index = generation
		population = self.final_generation(population, final_generation_index)
		return True


if __name__ == '__main__':
	a = GeneticBasedAlgorithm(100, 10)
	a.start()