import yt_dlp
import os

def download_youtube_mp4(url, output_path='videos'):
    os.makedirs(output_path, exist_ok=True)
    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        print('Error:', e)
        return None

if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube to Mp4 - Downloader')
    print('================================================================================================================')
    url = input('\nenlace del video(yt): ')
    print('Descargando...\n')
    video_file_path = download_youtube_mp4(url)
    if video_file_path:
        print('(✓) guardado en:', video_file_path)
    else:
        print('✕ Hubo un problema al descargar el video ✕')
