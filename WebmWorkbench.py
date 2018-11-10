#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=============================================================================#
# A simple ffmpeg GUI for video cutting and exporting to webm                 #
#=============================================================================#

import Tkinter as Tk
import tkFileDialog
import ttk
import os

# Batch export
def batchExport ():
	print "\n==============================================================================="
	# Input file, start time and duration
	command = "ffmpeg -ss " + i_startTime.get() + " -i \"" + i_inputFile.get() + "\" -t " + i_durationTime.get()
	
	if exportToGif.get() :
		print "Gif"
		command = command + " -f gif"
		
		if lowerQuality.get() :
			print "Lower quality"
			command = command + " -vf \"fps=18,scale=-1:320\""
		#else :
			# Palettegen seems to gub right now...
			#command = command + " -filter_complex \"[0:v] scale=-1:480,split [a][b];[a] palettegen [p];[b][p] paletteuse\""
			
		
	else :
		print "WebM"
		# WebM is VP8 / VP9 codec. Here we use variable bitrate in wich each image have a constant "quality" even if one out of some must take more size. (-b:v 1M)
		command = command + " -threads 4 -c:v libvpx -b:v 1M"
		
		if lowerQuality.get():
			print "Lower quality"
			command = command + " -crf 63 -vf \"fps=24,scale=-1:480,format=yuv420p\""
		else :
			command = command + " -crf 4"
		
		if noAudio.get() :
			print "No audio"
			command = command + " -an"
		else :
			command = command + " -c:a libvorbis"
		
	
	command = command + " \"" + i_outputFile.get() + "\""
	
	
	print "Running :"
	print command
	print "-------------------------------------------------------------------------------\n"
	os.system(command)
	print "\n===============================================================================\n"

def inputFileChoose ():
	filename = tkFileDialog.askopenfilename()
	if len(filename) > 0:
		print(filename)
		inputFile.set(filename)


def outputFileChoose ():
	filename = tkFileDialog.askopenfilename()
	if len(filename) > 0:
		print(filename)
		outputFile.set(filename)


# Extract thumbnail
def extractFrame (fname, strTime):
	command = 'ffmpeg -ss ' + strTime + ' -i "'+i_inputFile.get()+'" -vframes 1 -q:v 2 -vf \"scale=120:-1\" ' + fname + '.gif'
	os.system(command)


window = Tk.Tk()
window.title("Webm Workbench")
window.iconbitmap("res\icon.ico")
window.minsize(640, 480)
window.maxsize(640, 480)
print "Main"

p_main = Tk.PanedWindow(window, orient="vertical")
p_main.pack(side="top", expand="yes", fill="both", padx=2, pady=2)

#===============================================================================
# Notebook (tabs) for the appli
notebook = ttk.Notebook(p_main)
nbfrm_Files = ttk.Frame(notebook)
notebook.add(nbfrm_Files, text="Files")

nbfrm_Video = ttk.Frame(notebook)
notebook.add(nbfrm_Video, text="Video")

nbfrm_Audio = ttk.Frame(notebook)
notebook.add(nbfrm_Audio, text="Audio")

nbfrm_Options = ttk.Frame(notebook)
notebook.add(nbfrm_Options, text="Options")
notebook.pack(side="right", expand="yes", fill="both", padx=2, pady=2)

#===============================================================================
# Container for the file
print "File container"
lf_files = Tk.LabelFrame(nbfrm_Files, text="Files", padx=2, pady=2)
lf_files.pack()
#p_main.add(lf_files)

inputFile = Tk.StringVar()
inputFile.set("C:\\")
Tk.Label(lf_files, text="Input file").grid(row=1, column=1)
i_inputFile = Tk.Entry(lf_files, textvariable=inputFile)
i_inputFile.grid(row=1, column=2)
b_inputBrowse = Tk.Button(lf_files, text="...", command=inputFileChoose)
b_inputBrowse.grid(row=1, column=3)


outputFile = Tk.StringVar()
outputFile.set("D:\\tmp\\out.webm")
Tk.Label(lf_files, text="Output file").grid(row=2, column=1)
i_outputFile = Tk.Entry(lf_files, textvariable=outputFile)
i_outputFile.grid(row=2, column=2)
b_outputBrowse = Tk.Button(lf_files, text="...", command=outputFileChoose)
b_outputBrowse.grid(row=2, column=3)


#===============================================================================
# Container for the time
print "Time container"
lf_times = Tk.LabelFrame(nbfrm_Files, text="Time", padx=2, pady=2)
#p_main.add(lf_times)
lf_times.pack()

# Input : start time
startTime = Tk.StringVar()
startTime.set("00:00:00.000")
Tk.Label(lf_times, text="Start time").grid(row=1, column=1)
i_startTime = Tk.Entry(lf_times, textvariable=startTime, width=30)
i_startTime.grid(row=1, column=2)
b_startTimeSnap = Tk.Button(lf_times, text="[o]", command=lambda : extractFrame("snapStart", i_startTime.get()) )
b_startTimeSnap.grid(row=1, column=3)

# Input : duration
durationTime = Tk.StringVar()
durationTime.set("00:01:00.000")
Tk.Label(lf_times, text="Duration").grid(row=2, column=1)
i_durationTime = Tk.Entry(lf_times, textvariable=durationTime, width=30)
i_durationTime.grid(row=2, column=2)
b_durationTimeSnap = Tk.Button(lf_times, text="[o]", command=lambda : extractFrame("snapEnd", i_durationTime.get()) )
b_durationTimeSnap.grid(row=2, column=3)


#===============================================================================
# Container for the options
print "Option container"
lf_options = Tk.LabelFrame(nbfrm_Options, text="Options", padx=2, pady=2)
#p_main.add(lf_options)
lf_options.pack()

# Checkbox : no sound
noAudio = Tk.IntVar()
ck_noAudio = Tk.Checkbutton(lf_options, text="No audio", variable=noAudio)
ck_noAudio.pack()

# Checkbox : Force to standard (low quality, very tiny files)
lowerQuality = Tk.IntVar()
ck_lowerQuality = Tk.Checkbutton(lf_options, text="Standard quality", variable=lowerQuality)
ck_lowerQuality.pack()

# Checkbox : Gif
exportToGif = Tk.IntVar()
ck_exportToGif = Tk.Checkbutton(lf_options, text="Export to gif", variable=exportToGif)
ck_exportToGif.pack()

#===============================================================================
# Buttons
print "Buttons"
Tk.Button(window, text="Quit", command=window.quit).pack(side="right")#.grid(row=1, column=1)
Tk.Button(window, text="Export", command=batchExport).pack(side="left")#.grid(row=1, column=2)

print "mainloop"
window.mainloop()

