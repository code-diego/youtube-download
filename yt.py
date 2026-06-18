from pytube import YouTube, Playlist
import os

#---------------------------mp3---------------------------------------------

def download_youtube_mp3(url, output_path = None):
    try:
        yt = YouTube(url)
        print('Descargando...\n')

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        os.rename(out_file, new_file)
        print('Descarga exitosa :D')

        return new_file
    except Exception as e:
        print('Error : ', e)
        return
    
#---------------------------mp4---------------------------------------------
def download_youtube_mp4(url, output_path = None):
    try:
        yt = YouTube(url)
        print('Descargando...\n')

        video = yt.streams.get_highest_resolution()
        out_file = video.download(output_path)

        print('Descarga exitosa :D')
        return out_file
    except Exception as e:
        print('Error : ', e)
        return
    
#---------------------------mp3-playlist------------------------------------

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
            

#=Main===============================================================

if __name__ == '__main__':
    print('============================================================================================')
    print('\t\t\t\t\tDownloader Youtube links:')
    print('============================================================================================')
    print('1. Descargar MP3')
    print('2. Descargar MP4')

    op1 = 0
    while(op1 != 1 and op1 != 2):
        try :
            op1 = int(input('\nIndique una opcion: '))
        except Exception as e:
            print('Error : ' ,e)


    print('============================================================================================')
    print('1. Descargar UN solo video')
    print('2. Descargar PLAYLIST')

    op2 = 0
    while(op2 != 1 and op2 != 2):
        try :
            op2 = int(input('\nIndique una opcion: '))
        except Exception as e:
            print('Error : ' ,e)
    print('============================================================================================')
    url = ''
    if (op1 == 1 and op2 == 1):
        url = input('\nenlace de YouTube: ')
        output_path = 'music'
        audio_file_path = download_youtube_mp3(url, output_path)
        if audio_file_path:
            print('(✓) guardado en: ', audio_file_path)
        else:
            print('✕ Hubo un problema al descargar el audio ✕')

    elif (op1 == 1 and op2 == 2):
        url = input('\nenlace del video(yt): ')
        output_path = 'videos'
        video_file_path = download_youtube_mp4(url, output_path)
        if video_file_path:
            print('(✓) guardado en: ', video_file_path)
        else:
            print('✕ Hubo un problema al descargar el video ✕')

    elif (op1 == 2 and op2 == 1):
        url = input('\nPlaylist de YouTube: ')
        output_path = input('\ncarpeta: ')
        output_path = 'music/' + output_path
        download_playlist_mp3(url, output_path)
    else : #(op1 == 2 and op2 == 2):
        pass