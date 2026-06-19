import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import yt_dlp


# ---------------------------------------------------------------------------
# Configuracion de la descarga
# ---------------------------------------------------------------------------

@dataclass
class DownloadConfig:
    url: str
    output_dir: Path
    is_audio: bool
    is_playlist: bool


# ---------------------------------------------------------------------------
# Deteccion de playlist
# ---------------------------------------------------------------------------

def inspect_url(url: str) -> dict:
    """Consulta yt-dlp SIN descargar nada, solo para ver de que tipo es el link."""
    opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "noplaylist": False,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def has_specific_video(url: str) -> bool:
    """True si la URL apunta a un video puntual en lugar de solo una playlist."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "v" in query:
        return True
    path = parsed.path.strip("/")
    hostname = parsed.hostname or ""
    # youtu.be/VIDEO_ID?list=...
    if "youtu.be" in hostname and path and "/" not in path:
        return True
    # youtube.com/shorts/VIDEO_ID
    if "shorts" in path.split("/"):
        return True
    return False


def sanitize_filename(name: str) -> str:
    """Limpia un titulo para que sirva como nombre de carpeta/archivo."""
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def _format_bytes(b: float | int) -> str:
    if b < 1024:
        return f"{b:.0f}B"
    elif b < 1024 ** 2:
        return f"{b / 1024:.1f}KB"
    elif b < 1024 ** 3:
        return f"{b / 1024 ** 2:.1f}MB"
    return f"{b / 1024 ** 3:.1f}GB"


def progress_hook(d: dict) -> None:
    status = d.get("status")
    info = d.get("info_dict", {})
    idx = info.get("playlist_index", "")
    tag = f"[{idx}]" if idx else ""

    if status == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        pct = downloaded / total * 100 if total else 0
        speed = d.get("speed", 0)
        speed_s = f"{_format_bytes(speed)}/s" if speed else "?/s"
        eta = d.get("eta", 0)
        eta_s = f"{eta // 60:.0f}:{eta % 60:02.0f}" if eta else "?:??"
        bar_len = 20
        filled = int(pct / (100 / bar_len))
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\r  {tag} {bar} {pct:5.1f}%  {speed_s:>10}  ETA {eta_s:>5}", end="", flush=True)
    elif status == "finished":
        name = Path(d["filename"]).name
        print(f"\r  {tag} ✓ {name}")
    elif status == "error":
        print(f"\r  {tag} ✕ Error")


# ---------------------------------------------------------------------------
# Logica de descarga
# ---------------------------------------------------------------------------

def build_ydl_opts(config: DownloadConfig) -> dict:
    """Arma las opciones de yt-dlp segun lo que el usuario quiera descargar."""
    config.output_dir.mkdir(parents=True, exist_ok=True)

    opts = {
        "outtmpl": str(config.output_dir / "%(title)s.%(ext)s"),
        "noplaylist": not config.is_playlist,
        "ignoreerrors": True,
        "quiet": True,
        "progress_hooks": [progress_hook],
    }

    if config.is_audio:
        opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
        })

    return opts


def download(config: DownloadConfig) -> bool:
    """Ejecuta la descarga. Devuelve True si termino sin errores fatales."""
    opts = build_ydl_opts(config)
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([config.url])
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"✕ Error al descargar: {e}")
        return False


# ---------------------------------------------------------------------------
# Menu por consola
# ---------------------------------------------------------------------------

def ask_option(prompt: str, valid_options: tuple[int, ...]) -> int:
    """Pide un numero hasta que el usuario meta una opcion valida."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(f"  -> Ingresa un numero ({', '.join(map(str, valid_options))}).")
            continue
        if value in valid_options:
            return value
        print(f"  -> Opcion invalida. Elige entre {valid_options}.")


def main() -> None:
    print("=" * 60)
    print("           YouTube Downloader")
    print("=" * 60)

    print("1. Descargar MP3")
    print("2. Descargar MP4")
    formato = ask_option("\nIndica una opcion: ", (1, 2))
    is_audio = formato == 1

    print("=" * 60)
    url = input("\nEnlace de YouTube: ").strip()
    if not url:
        print("✕ No ingresaste ningun enlace.")
        sys.exit(1)

    print("\nAnalizando enlace...")
    try:
        info = inspect_url(url)
    except yt_dlp.utils.DownloadError as e:
        print(f"✕ No se pudo leer el enlace: {e}")
        sys.exit(1)

    is_playlist_url = info.get("_type") == "playlist" or "entries" in info
    is_playlist = False
    titulo_playlist = None

    if is_playlist_url:
        entries = info.get("entries") or []
        total = len(entries)
        titulo_playlist = info.get("title", "playlist")
        print(f"\n📋 Se detecto una playlist: \"{titulo_playlist}\" ({total} videos)")

        if has_specific_video(url):
            print("1. Descargar TODA la playlist")
            print("2. Descargar SOLO este video")
            eleccion = ask_option("\nIndica una opcion: ", (1, 2))
            is_playlist = eleccion == 1
        else:
            print("(No se detecto un video puntual en el enlace, se descargara la playlist completa)")
            is_playlist = True
    else:
        print("\n🎬 Se detecto un video individual.")

    print("=" * 60)
    carpeta_base = "music" if is_audio else "videos"

    if is_playlist:
        sugerido = sanitize_filename(titulo_playlist)
        subcarpeta = input(f"Nombre de carpeta para la playlist [{sugerido}]: ").strip() or sugerido
        output_dir = Path(carpeta_base) / subcarpeta
    else:
        output_dir = Path(carpeta_base)

    config = DownloadConfig(
        url=url,
        output_dir=output_dir,
        is_audio=is_audio,
        is_playlist=is_playlist,
    )

    print("\nDescargando...\n")
    ok = download(config)

    if ok:
        print(f"\n(✓) Descarga completa. Archivos guardados en: {output_dir.resolve()}")
    else:
        print("\n✕ Hubo un problema durante la descarga ✕")


if __name__ == "__main__":
    main()