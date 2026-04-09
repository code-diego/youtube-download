from pytube import Playlist
import os

def download_playlist_mp3(url, output_path = None):
    playlist = Playlist(url)
    try :
        test = playlist.title
    except:
        print('Error: Playlist no encontrada')
        return
    for videoyt in playlist.videos:
        try:
            video = videoyt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            videoname = video.title
            print(f'(listo ✓) -> {videoname} ')
        except:
            print(f'✕ error ✕ con {videoname} ')        
            

if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube Playlist to Mp3')
    print('================================================================================================================')
    url = input('\nPlaylist de YouTube: ')
    #output_path = 'music'
    output_path = input('\ncarpeta: ')
    download_playlist_mp3(url, output_path)
