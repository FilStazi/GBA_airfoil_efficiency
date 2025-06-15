"""
    GENETIC BASED ALGORITHM for UAV airfoil generation.
    GBA for UAV Airfoil Generation is a Python-based tool developed
    as part of my undergraduate thesis. It automates the generation
    of airfoil shapes optimized to minimize a user-defined fitness
    function. The tool leverages a simple single-objective genetic
    algorithm and integrates with XFOIL for aerodynamic analysis,
    enabling efficient performance evaluation of evolved airfoils
    for UAV applications.
    Filippo Stazi, Università degli studi di Udine,
    July 2024

"""

print("Including external modules")
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import numpy as np
import random
import math
import time
import os
import sys


#MODULO ALGORITMO GENETICO
from GBA import genetic_based_algorithm

#GENERAZIONE VIDEO
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import *

#REDIRECT OUTPUT
from io import StringIO


import shutil #PER CANCELLARE CARTELLE


def clean_environment():
    #PULISCE DALLE ANALISI PASSATE
    print("Environment Setup:")
    if os.path.exists("Airfoil"): shutil.rmtree("Airfoil")
    os.makedirs("Airfoil")
    if os.path.exists("Images"): shutil.rmtree("Images")
    os.makedirs("Images")
    if os.path.exists("Clip"): shutil.rmtree("Clip")

    with open("fit.txt", "w") as f: pass #cancella file per grafico finale o lo crea se non c'era

if __name__ == '__main__':

    with open("input.txt", "r") as f:
        for _ in range(5): # skip first 5 lines
            f.readline()
        dim_pop = int(f.readline())
        num_gen = int(f.readline())
        mod = f.readline()
        make_video = f.readline().strip() == "True"
        make_plots = f.readline().strip() == "True"

    #dim_pop, num_gen = 100, 15
    if dim_pop % 2 != 0: dim_pop += 1
    FPS = 30
    
    clean_environment()

    os.system("cls")
    print(dim_pop, num_gen, mod)
    print("Genetic algorithm for wing airfoil generation.")
    #mod = input("Insert analysis name -> ")

    #GENERO NOME ANALISI E CREO CARTELLA FINALE
    analysis_folder = Path("Analysis", str(dim_pop) + "_" + str(num_gen) + "_" +  mod)
    if os.path.exists(analysis_folder):
        ans = input("The analysis has already been executed, do it again losing the first one (Y/N) ->")
        if ans == "Y":
            shutil.rmtree(analysis_folder)
            os.makedirs(analysis_folder)
        else:
            exit()
    else: os.makedirs(analysis_folder)

    matplotlib.use("Agg") #FA IN MODO CHE I PLOT VENGANO SALVATI E NON MOSTRATI

    #ANALISI
    start_time = time.time()
    execute = genetic_based_algorithm.GeneticBasedAlgorithm(dim_pop,num_gen).start()

    end_time = time.time() - start_time
    with open("ottimizzazzione.txt", "a") as f:
        f.write(str(round(end_time,2)) + '\n')

    #os.system("cls")

    #STAMPO IL TEMPO DI ANALISI
    print("Execution time:", str(round(end_time,2)))
    with open(Path("GBA","time.txt"), "a") as f:
        f.write(str(round(end_time,2)) + " seconds.")

    shutil.move(Path("GBA","time.txt"), analysis_folder)


    #CREAZIONE VIDEO
    if make_video:
        sys.stdout = StringIO()
        print("Creating video:")

        clip_dir = "Images"
        image_paths = []
        for folder in os.listdir(clip_dir):
            folder_path = os.path.join(clip_dir, folder)
            if os.path.isdir(folder_path):
                # Find the image in the subdirectory (assuming there's only one image per folder)
                for file in os.listdir(folder_path):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(folder_path, file)
                        image_paths.append(image_path)
                        break  # Assuming only one image per folder

        # Create a video clip from the images
        clip = ImageSequenceClip(image_paths, fps=4)  # 1 frame per second

        # Write the video file
        output_path = 'video_algoritmo.mp4'
        clip.write_videofile(output_path, codec='libx264', fps=5)
        clip.close()

    #shutil.move(Path("", "Images", "generation_final"), analysis_folder)
    #shutil.rmtree("Images")

    #CREAZIONE GRAFICI POST-ANALISI
    make_plots = True
    if make_plots:
        print("Data elaboration:")
        #CREA LE LISTE PER I PLOT
        with open("fit.txt") as f:
            lines = f.readlines()
        order_number,fit,aoa,chord = [],[],[],[]
        for line in lines:
            values = line.split()
            order_number.append(float(values[0]))
            fit.append(float(values[1]))
            aoa.append(float(values[2]))
            chord.append(float(values[3]))

        #CREA PLOT AOA
        fig, ax = plt.subplots()
        plt.scatter(order_number, aoa, color='red', s=2)
        plt.xlabel("Order number")
        plt.ylabel("Angle of attack (°)")
        plt.suptitle("Angle of attack")
        plt.savefig(Path(analysis_folder, "aoa"))
        matplotlib.pyplot.close()

        #CREA PLOT chord
        fig, ax = plt.subplots()
        plt.scatter(order_number, chord, color='blue', s=2)
        plt.xlabel("Order number")
        plt.ylabel("Chord (mm)")
        plt.suptitle("chord")
        plt.savefig(Path(analysis_folder, "chord"))
        matplotlib.pyplot.close()

        #CREA PLOT FITNESS
        fig, ax = plt.subplots()
        plt.plot(order_number, fit, color='green')
        plt.xlabel('Order Number')
        plt.ylabel('Fitness')
        plt.suptitle('Fitness vs Order Number')
        plt.savefig(Path(analysis_folder, "fitness"))
        matplotlib.pyplot.close()

        shutil.move(Path("", "fit.txt"), Path("", analysis_folder))
        
    #SPOSTO GLI AIRFOIL NELLA CARTELLA FINALE
    shutil.move(Path("", "Airfoil"), Path("", analysis_folder))
    
    sys.stdout = sys.__stdout__