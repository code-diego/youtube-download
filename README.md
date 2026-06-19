# YouTube Downloader

Descarga videos o audio de YouTube usando `yt-dlp`.

## Instalación

```bash
pip install yt-dlp
```

> También necesitas tener `ffmpeg` instalado en tu sistema.

## Uso

```bash
python yt.py
```

Sigue el menú interactivo:
1. Elegí MP3 (solo audio) o MP4 (video)
2. Pegá el enlace de YouTube
3. Si es una playlist, elegí si descargar todo o solo ese video

## Scripts obsoletos

Los scripts originales con `pytube` están en la carpeta [`old/`](old/):
- `old/yt-link-to-mp3.py`
- `old/yt-link-to-mp4.py`
- `old/yt-playlist-to-mp3.py`

Quedan solo como referencia histórica. `yt.py` los reemplaza a todos.
