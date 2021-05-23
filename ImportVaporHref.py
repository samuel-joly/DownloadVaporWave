import requests, bs4, json

vaporFiles = 'https://vaporwave.ivan.moe/list/'
res = requests.get(vaporFiles)
res.raise_for_status()

artists = bs4.BeautifulSoup(res.text, features='lxml' )
artists = artists.select('#list tbody tr')
#del artists[0]

totalLen = 11828
count = 0
fullList = []

for artist in artists:
	albumsLink = 'https://files.sq10.net/music/vaporwave/list/' + artist.select('a')[0].get('href')
	albumsRes = requests.get(albumsLink)
	albumsRes.raise_for_status()

	albums = bs4.BeautifulSoup(albumsRes.text, features='lxml')
	albums = albums.select('#list tbody tr')
	del albums[0]

	albumDict = (artist.select('a')[0].getText() , [])


	for album in albums:
		
		if (album.select('a')[0].get('href').endswith('.flac') or 
			album.select('a')[0].get('href').endswith('.jpg') or
			album.select('a')[0].get('href').endswith('.mp3') or
			album.select('a')[0].get('href').endswith('.png')):
		
			albumDict[1].append(albumsLink+album.select('a')[0].get('href'))

		else:
			songsLink = albumsLink + album.select('a')[0].get('href')
			songsRes = requests.get(songsLink)
			songsRes.raise_for_status()

			songs = bs4.BeautifulSoup(songsRes.text, features='lxml')
			songs = songs.select('#list tbody tr')
			del songs[0]

			for song in songs:
				totalLen += 1
				albumDict[1].append(songsLink+song.select('a')[0].get('href'))
	
	fullList.append(albumDict)
	count += 1


json.dump(fullList, open('AllLink.json','w'), indent='\n')
