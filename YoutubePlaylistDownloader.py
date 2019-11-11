# Downloads a youtube playlist as mp3/mp4 files

from pytube import *              # For retrieving youtube playlist
import moviepy.editor as mp       # For converting mp4 to mp3
import glob                       # For detecting mp4 extensions
import os              
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# Creates basic window.
window = Tk()
window.title("YoutubePlaylistDownloader")
window.geometry('350x100')

# GUI for entering yt playlist.
lbl = Label(window, text="Youtube Playlist: ", font=("Arial Bold", 10))
lbl.grid(column=1,row=0)
txt = Entry(window,width=20)
txt.grid(column=2, row=0)
txt.focus()

# Buttons for selecting mp3/mp4
v = IntVar()
mp3select = Radiobutton(window, text = "mp3 (audio)", variable=v, value = 1)
mp3select.grid(column=2,row=3)
mp4select = Radiobutton(window, text = "mp4 (video)", variable=v, value = 2)
mp4select.grid(column=2,row=4)
mp4select.deselect()

def download():
    valid = True
    playlist_link = txt.get()
    
    # Checks if link entered is null
    if not playlist_link:
        messagebox.showerror("Error", "No link available!")
        valid = False
       
    playlist = Playlist(playlist_link)

    # Checks if link is invalid or playlist is empty
    try:
        if(len(playlist.video_urls) > 0):
            print('')
    except:
        valid = False
        messagebox.showerror("Error", "Link is invalid or playlist is empty!")

    if(valid):
        directory = filedialog.askdirectory()
        playlist.download_all(directory)

        button_selected = v.get()

        # Since we can't automatically download as an mp3, we must download as an mp4 then covert to mp3 if necessary.
        if(button_selected == 1):
            mp4list = glob.glob(directory + "/*.mp4")
            for mp4 in mp4list:
                clip = mp.VideoFileClip(mp4)
                new_mp4 = mp4[:-4]                          # deletes .mp4 extension in filename.
                clip.audio.write_audiofile(new_mp4 + ".mp3")
                clip.reader.close()                         # prevents error that stops conversions midway through.
                os.remove(mp4)            

            messagebox.showinfo(title = "YoutubePlaylistDownloader", message = "Download Complete!")
            sys.exit()
    

# Button for downloading playlist.
btn = Button(window,text="Download", command=download)
btn.grid(column=2,row=2)

window.mainloop()

