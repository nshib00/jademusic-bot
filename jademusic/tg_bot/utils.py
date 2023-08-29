import string, secrets
from pathlib import Path


class PathManager:
    download_path = Path('~').expanduser() / 'Downloads/JadeMusic'


def make_response_message(response, logger, downloading_object_title='', mode='playlist'):
    response_words = {'album': 'Альбом', 'playlist': 'Плейлист'}

    if response.status_code == 200:
        if mode == 'tracks':
            msg = f'✅Треки успешно скачаны!'
        else:
            msg = f'✅{response_words[mode]} "{downloading_object_title}" скачан успешно!'
        msg += f' Скачанная музыка находится в папке {PathManager.download_path}.'
    else:
        resp_text = response.html.find("title", first=True).text
        logger.error(f'{response.status_code} {response.reason}: {resp_text}')
        msg = f'❗️При попытке скачивания возникла ошибка: HTTP {response.status_code} {response.reason}.'
    return msg


def make_track_word(tracks_count):
    if tracks_count % 10 == 1:
        return 'трека'
    else:
        return 'треков'


def create_user_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))


