import tkinter, json, webbrowser
from tkinter import font
from urllib.parse import unquote
import os
import urllib.request
import threading
import queue


def displaySavedLinks():
	with open('allLink.json', 'r+') as ofi:
		savedLinks = json.loads(ofi.read())

	for content in savedLinks:
		albumDisplay.insert(tkinter.END, content[0].encode().decode('utf-8')[:-1])

	return savedLinks

def displaySongs(event):
	curAlbum = albumDisplay.get(albumDisplay.curselection())
	count = 0


	for album in albums:
		if album[0].encode().decode('utf-8')[:-1] == curAlbum:
			songDisplay.delete(0, tkinter.END)
			songDisplay.grid(row=0,column=2, rowspan=4)
			scrollSong.grid(row=0,column=3,rowspan=4, sticky='NSW')
			scrollSongX.grid(row=6,column=2,sticky='SEW')
			DLbutton.grid(row=0,column=4,sticky='NWE')
			multipleSelectButton.grid(row=1,column=4,sticky='NWE')
			DLSelectedButton.grid(row=2,column=4,sticky='NWE')
			YtButton.grid(row=3,column=4,sticky='NWE')


			app.rowconfigure(0, weight=0)
			app.rowconfigure(1, weight=0)
			app.rowconfigure(2, weight=0)
			app.rowconfigure(3, weight=1)

			for song in album[1]:
				songName = song.split('/')[-1]
				songDisplay.insert(tkinter.END, unquote(songName))
				count += 1

class downloadThisAlbum(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                curAlbum = albumDisplay.get(albumDisplay.curselection()).encode('utf-8')

                for album in albums:
                        albumName = album[0].encode('utf-8')[:-1]
                        albumFoldName = unquote(album[0])

                        if albumName == curAlbum:
                                for song in album[1]:
                                        songIsHere = False
                                        for folder in os.scandir(os.getcwd()+'//Download'):

                                                if albumFoldName == folder.name+'/':
                                                        songIsHere = True
                                                        break

                                        if not songIsHere:
                                                os.mkdir('Download//'+unquote(album[0]))

                                        songName = song.split('/')[-1]
                                        songLinkLocal = 'Download//'+albumFoldName[:-1]+'//'+unquote(songName)

                                        urllib.request.urlretrieve(song,songLinkLocal)

class downloadSong(threading.Thread):
        def __init__(self,songName, path):
                threading.Thread.__init__(self)
                self.songName = songName
                self.path = path

        def run(self):
                for album in albums:
                        for song in album[1]:
                                curSongName = song.split('/')[-1]
                                
                                if unquote(curSongName) == self.songName:
                                        urllib.request.urlretrieve(song, self.path+'//'+unquote(curSongName))
                                        break

class downloadSelected(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                curItems = songDisplay.curselection()
                downloadIsHere = False
                
                for folder in os.scandir('.'):
                        if folder.name == 'Download':
                                downloadIsHere = True

                if not downloadIsHere:
                        os.mkdir('Download')

                for selection in curItems:
                        selected = songDisplay.get(selection)
                        downloadSong(selected, os.getcwd()+'//Download').start()



app = tkinter.Tk()
app.title('VaporWave Download')


albumDisplayFont = font.Font(size=13, weight='bold', family='Serif')
albumDisplay = tkinter.Listbox(app, height=30, width=44, font=albumDisplayFont)
scrollAlbum = tkinter.Scrollbar(app, orient=tkinter.VERTICAL)
albumDisplay.config(yscrollcommand=scrollAlbum.set)
scrollAlbum.config(command=albumDisplay.yview)
albumDisplay.bind('<<ListboxSelect>>', displaySongs)


songDisplay = tkinter.Listbox(app,  height=30, width=65, font=albumDisplayFont)
scrollSong = tkinter.Scrollbar(app, orient=tkinter.VERTICAL)
scrollSongX = tkinter.Scrollbar(app, orient=tkinter.HORIZONTAL)
songDisplay.config(xscrollcommand=scrollSongX.set)
scrollSongX.config(command=songDisplay.xview)
songDisplay.config(yscrollcommand=scrollSong.set)
scrollSong.config(command=songDisplay.yview)

albumDisplay.grid(row=0,column=1,rowspan=7, sticky='NWS')
scrollAlbum.grid(row=0, column=0, rowspan=7,sticky='WNS')


DLbutton = tkinter.Button(app, text='Download Album', command=lambda:downloadThisAlbum().start())
multipleSelectButton = tkinter.Checkbutton(app, text='Multiple Selection', command=lambda:songDisplay.config(selectmode=tkinter.EXTENDED))
DLSelectedButton = tkinter.Button(app, text='Download Selection', command=lambda:downloadSelected().start())
YtButton = tkinter.Button(app, text='Youtube Search', command = 
			lambda:webbrowser.open_new_tab('https://www.youtube.com/results?search_query='+songDisplay.get(songDisplay.curselection())[:-5]))

albums = displaySavedLinks()






app.mainloop()
