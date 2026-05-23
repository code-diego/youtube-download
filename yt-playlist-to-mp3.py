import yt_dlp
import os

def download_playlist_mp3(url, output_path='music'):
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
            info = ydl.extract_info(url, download=False)
            total = len(info['entries'])
            print(f'Playlist: {info["title"]} ({total} videos)\n')
        options['quiet'] = False
        options['progress_hooks'] = [lambda d: print(f'(✓) {d["filename"].split("/")[-1]}') if d['status'] == 'finished' else None]
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    print('================================================================================================================')
    print('\t\t\t\t\tYoutube Playlist to Mp3')
    print('================================================================================================================')
    url = input('\nPlaylist de YouTube: ')
    output_path = input('\ncarpeta: ')
    download_playlist_mp3(url, output_path)
