from pytube import YouTube
import os

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
    
if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube to Mp4 - Downloader')
    print('================================================================================================================')
    url = input('\nenlace del video(yt): ')
    output_path = 'videos'
    video_file_path = download_youtube_mp4(url, output_path)
    if video_file_path:
        print('(✓) guardado en: ', video_file_path)
    else:
        print('✕ Hubo un problema al descargar el video ✕')