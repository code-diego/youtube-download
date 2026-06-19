import yt_dlp
import os

def download_youtube_mp3(url, output_path='music'):
    os.makedirs(output_path, exist_ok=True)
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            return filename
    except Exception as e:
        print('Error:', e)
        return None

if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube to Mp3 - Downloader')
    print('================================================================================================================')
    url = input('\nenlace de YouTube: ')
    print('Descargando...\n')
    audio_file_path = download_youtube_mp3(url)
    if audio_file_path:
        print('(✓) guardado en:', audio_file_path)
    else:
        print('✕ Hubo un problema al descargar el audio ✕')
