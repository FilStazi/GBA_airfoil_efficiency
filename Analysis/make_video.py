import matplotlib
import matplotlib.pyplot as plt

#GENERAZIONE VIDEO
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *

def make_plot(name_file):
	name_file = name_file
	x,y = [],[]
	with open(name_file, "r") as f:
		f.readline()
		data = f.readlines()
		for i in data:
			x.append(data[0])
			y.append(data[1])
	fig, ax = plt.subplots()
	ax.set_xlim(0, 1)
	ax.set_ylim(-0.3, 0.3)
	ax.autoscale(False)
	ax.plot(x, y, color='black', label='profile')
	ax.scatter(individual.upper_nodes[0], individual.upper_nodes[1], color='blue', label='upper nodes', marker = 'x')
	ax.scatter(individual.lower_nodes[0], individual.lower_nodes[1], color='red', label='lower nodes', marker = 'x')
	with open(individual.file, 'r') as file:
	    next(file)  # Skip the first line
	    x, y = zip(*(map(float, line.split()[:2]) for line in file))
	folder_img = Path("Images", "generation_" + str(g))
	if not os.path.exists(folder_img): os.makedirs(folder_img)
	plt.suptitle("Generation: " + str(g) + "   Number: " + str(p) + "   Fit: " + str(round(individual.fitness, 3)) + "\nAoa: " + str(round(individual.aoa,2)) + "   Chord: " + str(round(individual.c,3)) + "   Th (mm): " + str(round(individual.thickness*individual.c,3)))
	plt.legend()
	plt.savefig(Path(folder_img, name_file))
	matplotlib.pyplot.close()
    #grafici finali
	with open("fit.txt", "a") as f:
		f.write(str(self.count) + ' ' + str(round(individual.fitness, 3)) + ' ' + str(int(individual.aoa)) +  ' ' + str(round(individual.c, 3)) +'\n')
		self.count += 1


sys.stdout = StringIO()
    print("Creating video:")

    directory_input = Path("", "clip")
    if not os.path.exists(directory_input):
        os.makedirs(directory_input)

    for i in range(num_gen):
        frames_folder = Path("Images", "generation_" + str(i) + "/")
        if i < 10:
            output_video = "generation_00"+ str(i) + ".mp4"
        elif i < 100:
            output_video = "generation_0"+ str(i) + ".mp4"
        else:
            output_video = "generation_"+ str(i) + ".mp4"

        clip = ImageSequenceClip(frames_folder, fps=FPS)
        path_output = directory_input
        clip.write_videofile(Path(path_output, output_video).as_posix(), fps=FPS)
        clip.close()

    all_files = os.listdir(directory_input)
    mp4_files = sorted([file for file in all_files if file.endswith(".mp4")])
    clips = [VideoFileClip(Path(directory_input, video).as_posix()) for video in mp4_files]
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("video_summary.mp4")
    final_video.close()
    shutil.move("video_summary.mp4", Path(analysis_folder, "video_summary.mp4"))

shutil.move(Path("", "Images", "generation_final"), analysis_folder)
shutil.rmtree("Images")