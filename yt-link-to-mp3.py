from pytube import YouTube
import os

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

if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube to Mp3 - Downloader')
    print('================================================================================================================')
    url = input('\nenlace de YouTube: ')
    output_path = 'music'
    audio_file_path = download_youtube_mp3(url, output_path)
    if audio_file_path:
        print('(✓) guardado en: ', audio_file_path)
    else:
        print('✕ Hubo un problema al descargar el audio ✕')
    


# Code original

# print('\nYoutube to Mp3 - Downloader\n')
# URL = input("Ingresar el URL : ")
# yt = YouTube(URL)

# try:
#     print("\nDescargando...")
#     video = yt.streams.filter(only_audio=True).first()
#     out_file = video.download()
#     base, ext = os.path.splitext(out_file)
#     new_file = base + ".mp3"
#     os.rename(out_file, new_file)
#     print("\nDescarga exitosa :D\n")

# except:
#     print("\nOh no, algo paso :x. Intentelo de nuevo!\n")
    

