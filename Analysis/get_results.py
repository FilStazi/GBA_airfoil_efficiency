from PIL import Image
from pathlib import Path
import os

directory_path = r"C:\Users\filip\OneDrive\Desktop\tesi\__algoritmo\Analysis"

folder_names = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

for folder in folder_names:
	with open(Path(folder, "time.txt"), "r") as f:
		print(''.join(filter(lambda x: x.isdigit() or x == '.', f.readline().strip()))[:-1])

for folder in folder_names:
	print(folder)
	image_path = Path(folder, "generation_final", "airfoil_final_0000.png")
	image = Image.open(image_path)
	image.show()
	a = input()