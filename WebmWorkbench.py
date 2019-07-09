#! C:\Python\Python37\python.exe
#! coding: utf-8
#! python3
# Guillaume Viravau 2018-2019
#=============================================================================#
# A simple ffmpeg GUI for video cutting and exporting to webm                 #
#                                                                             #
#=============================================================================#

# Python 2
#import os
#import Tkinter as Tk
#import tkFileDialog as Tk.filedialog
#import ttk as Tk.ttk

# Python 3
import os
import tkinter as Tk
import tkinter.filedialog
import tkinter.ttk


# Batch export
def batchExport() :
	print( "\n===============================================================================" )
	# Input file, start time and duration
	command = "ffmpeg -ss " + i_startTime.get() + " -i \"" + i_inputFile.get() + "\""
	
	if( exportToGif.get() ) :
		print( "Gif" )
		command = command + " -t " + i_durationTime.get() + " -f gif"
		
		if( lowerQuality.get() ) :
			print( "Lower quality" )
			command = command + " -vf \"fps=18,scale=-1:320\""
		#else :
			# Palettegen seems to gub right now...
			#command = command + " -filter_complex \"[0:v] scale=-1:480,split [a][b];[a] palettegen [p];[b][p] paletteuse\""
			
		
	else :
		print( "WebM" )
		# Manage audio stream
		if( audioMode.get() == 0 ) :
			print( "To vorbis" )
			command = command + " -c:a libvorbis"
		elif( audioMode.get() == 1 ) :
			print( "No audio" )
			command = command + " -an"
		else :
			print( "From audio" )
			command = command + " -i \"" + i_audioFile.get() + "\"" " -c:a libvorbis  -shortest"
		
		command = command + " -t " + i_durationTime.get()
		# WebM is VP8 / VP9 codec. Here we use variable bitrate in wich each image have a constant "quality" even if one out of some must take more size. (-b:v 1M)
		command = command + " -threads 4 -c:v libvpx -b:v 1M"
		
		if( lowerQuality.get() ) :
			print( "Lower quality" )
			command = command + " -crf 63 -vf \"fps=24,scale=-1:480,format=yuv420p\""
		else :
			command = command + " -crf 4"
		
		
	
	command = command + " \"" + i_outputFile.get() + "\""
	
	#textCommand.insert(command)
	print( "Running :" )
	print( command )
	print( "-------------------------------------------------------------------------------\n" )
	os.system(command)
	print( "\n===============================================================================\n" )


def FileChoose( TkStringVar ) :
	filename = Tk.filedialog.askopenfilename()
	if( len(filename) > 0 ):
		print( filename )
		TkStringVar.set(filename)


# Extract thumbnail
def extractFrame( fname, strTime ) :
	command = 'ffmpeg -ss ' + strTime + ' -i "'+i_inputFile.get()+'" -vframes 1 -q:v 2 -vf \"scale=120:-1\" ' + fname + '.gif'
	os.system( command )


window = Tk.Tk()
window.title( "Webm Workbench" )
window.iconbitmap( "res\icon.ico" )
window.minsize( 480, 360 )
window.maxsize( 640, 480 )
print( "Main" )

#===============================================================================
# Notebook (tabs) for the appli
notebook = Tk.ttk.Notebook( window )
nbfrm_Files = Tk.ttk.Frame( notebook )
notebook.add( nbfrm_Files, text="Files" )

nbfrm_Video = Tk.ttk.Frame( notebook )
notebook.add( nbfrm_Video, text="Video" )

nbfrm_Audio = Tk.ttk.Frame( notebook )
notebook.add( nbfrm_Audio, text="Audio" )

nbfrm_Options = Tk.ttk.Frame( notebook )
notebook.add( nbfrm_Options, text="Options" )
notebook.grid( row=1, column=1, columnspan=2, sticky="we" )
#pack( expand="yes", fill="both", padx=2, pady=2 )

textCommand = Tk.Text( window, width=40, height=4 )
textCommand.grid( row=2, column=1, columnspan=2, sticky="wens", padx=2, pady=2 )
#pack( expand="yes", fill="both", padx=2, pady=2 )

print( "Buttons" )
buttonExport = Tk.Button( window, text="Execute", command=batchExport )
buttonExport.grid( row=3, column=2, sticky="we" )

#window.grid_rowconfigure( 1,weight=1 )
window.grid_rowconfigure( 2,weight=1 )
#window.grid_rowconfigure( 3,weight=1 )
window.grid_columnconfigure( 1,weight=1 )
window.grid_columnconfigure( 2,weight=1 )

#===============================================================================
# Container for the file
print( "File container" )
lf_files = Tk.LabelFrame( nbfrm_Files, text="Files", padx=2, pady=2 )
lf_files.pack()
#p_main.add( lf_files )

inputFile = Tk.StringVar()
inputFile.set( "C:\\" )
Tk.Label( lf_files, text="Input file" ).grid( row=1, column=1 )
i_inputFile = Tk.Entry( lf_files, textvariable=inputFile )
i_inputFile.grid( row=1, column=2 )
b_inputBrowse = Tk.Button( lf_files, text="...", command=lambda : FileChoose( inputFile ) )
b_inputBrowse.grid( row=1, column=3 )


outputFile = Tk.StringVar()
outputFile.set( "D:\\tmp\\out.webm" )
Tk.Label( lf_files, text="Output file" ).grid( row=2, column=1 )
i_outputFile = Tk.Entry( lf_files, textvariable=outputFile )
i_outputFile.grid( row=2, column=2 )
b_outputBrowse = Tk.Button( lf_files, text="...", command=lambda : FileChoose( outputFile ) )
b_outputBrowse.grid( row=2, column=3 )


#===============================================================================
# Container for the time
print( "Time container" )
lf_times = Tk.LabelFrame( nbfrm_Files, text="Time", padx=2, pady=2 )
#p_main.add(lf_times)
lf_times.pack()

# Input : start time
startTime = Tk.StringVar()
startTime.set( "00:00:00.000" )
Tk.Label( lf_times, text="Start time" ).grid( row=1, column=1 )
i_startTime = Tk.Entry( lf_times, textvariable=startTime, width=30 )
i_startTime.grid( row=1, column=2 )
b_startTimeSnap = Tk.Button( lf_times, text="[o]", command=lambda : extractFrame("snapStart", i_startTime.get()) )
b_startTimeSnap.grid( row=1, column=3 )

# Input : duration
durationTime = Tk.StringVar()
durationTime.set( "00:01:00.000" )
Tk.Label( lf_times, text="Duration" ).grid( row=2, column=1 )
i_durationTime = Tk.Entry( lf_times, textvariable=durationTime, width=30 )
i_durationTime.grid( row=2, column=2 )
b_durationTimeSnap = Tk.Button( lf_times, text="[o]", command=lambda : extractFrame("snapEnd", i_durationTime.get()) )
b_durationTimeSnap.grid( row=2, column=3 )

#===============================================================================
# Container for the Audio
print( "Audio container" )
lf_audio = Tk.LabelFrame( nbfrm_Audio, text="Audio", padx=2, pady=2 )
lf_audio.pack()

# Radobutton : Audio mode
audioMode = Tk.IntVar()
rb_audioMode_copy = Tk.Radiobutton( lf_audio, text="Convert to Vorbis", variable=audioMode, value=0 )
rb_audioMode_copy.grid( row=1, column=1, sticky='w' )

# Checkbox : no sound
rb_audioMode_mute = Tk.Radiobutton( lf_audio, text="No audio", variable=audioMode, value=1 )
rb_audioMode_mute.grid( row=2, column=1, sticky='w')

# Input file : change audio
rb_audioMode_file = Tk.Radiobutton( lf_audio, text="Audio audio", variable=audioMode, value=2 )
rb_audioMode_file.grid( row=3, column=1, sticky='w')
audioFile = Tk.StringVar()
audioFile.set( "D:\\tmp\\audio.mp3" )
i_audioFile = Tk.Entry( lf_audio, textvariable=audioFile )
i_audioFile.grid( row=3, column=2 )
b_audioBrowse = Tk.Button( lf_audio, text="...", command=lambda : FileChoose( audioFile ) )
b_audioBrowse.grid( row=3, column=3 )

#===============================================================================
# Container for the options
print( "Option container" )
lf_options = Tk.LabelFrame( nbfrm_Options, text="Options", padx=2, pady=2 )
#p_main.add(lf_options)
lf_options.pack()

# Checkbox : Force to standard (low quality, very tiny files)
lowerQuality = Tk.IntVar()
ck_lowerQuality = Tk.Checkbutton( lf_options, text="Standard quality", variable=lowerQuality )
ck_lowerQuality.pack()

# Checkbox : Gif
exportToGif = Tk.IntVar()
ck_exportToGif = Tk.Checkbutton( lf_options, text="Export to gif", variable=exportToGif )
ck_exportToGif.pack()
#===============================================================================

print( "mainloop" )
window.mainloop()

