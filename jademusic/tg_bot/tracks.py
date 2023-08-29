from pathlib import Path

from dotenv import load_dotenv
from os import getenv

from requests_html import HTMLSession
import json
from telebot import util, TeleBot
import logging

from telebot.types import Message

import keyboard, utils


cwd = Path('').cwd() 
env_file_path = cwd / 'jademusic' / '.env'
load_dotenv(env_file_path)
HOST = getenv('JADEMUSIC_HOST')
API_URL = HOST + '/' + getenv('API_URL')

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='WARNING', filename='../logs.log')


class TrackManager:
    query: str | None = None
    search_by_artist: int = 0
    tracks_to_download_count: int | None = None
    track_nums: str | None = None
    page: int = 1


def get_tracks_url(artist=0, page=1, popular=False, new=False):
    if popular:
        url = f'{API_URL}/track/get?popular=1'
    elif new:
        url = f'{API_URL}/track/get?new=1'
    else:
        url = f'{API_URL}/track/get?q={TrackManager.query}&artist={artist}&page={TrackManager.page}'
    return url


def get_tracks_json(artist=0, popular=False, new=False):
    url = get_tracks_url(artist=artist, popular=popular, new=new)
    session = HTMLSession()
    response = session.get(url)
    try:
        resp_json = json.loads(response.text)
        if resp_json.get('data'):
            if resp_json['data'].get('tracks'):
                return resp_json['data']['tracks']
            return {}
    except json.decoder.JSONDecodeError as e:
        logger.error(f'JSONDecodeError: {e}')
        return {'error': f'{e}'}
    except Exception as e:
        logger.error(f'Error: {e}')
        return {'error': f'{e}'}


def tracks_dict_is_empty(tracks_list: dict | None) -> bool:
    if tracks_list is None:
        return False
    return True if len(tracks_list) == 0 else False


def print_tracks_response(bot, message, tracks):
    tracks_string = ''
    if tracks is not None:
        if len(tracks) == 0:
            if TrackManager.page == 1:
                bot.send_message(message.chat.id, '✖️По запросу ничего не найдено. Либо треки по данному запросу отсутствуют на сайте, либо название трека/исполнителя введено неверно.')
            else:
                bot.send_message(message.chat.id, '✖️На этой и следующих страницах нет треков. Вы можете вернуться к предыдущим страницам или выйти из меню скачивания треков.')
        else:
            for track in tracks:
                tracks_string += str(track['id']) + ') ' + track['data']['full_title'] + '\n'
            tracks_info = f'📄Cтраница: {TrackManager.page}\nℹ️Найдено треков: {len(tracks)}\n\n{tracks_string}'
            for tracks_info_part in util.smart_split(tracks_info, 4000):
                bot.send_message(message.chat.id, tracks_info_part)


def get_tracks(bot, message, info_text, popular=False, new=False):
    bot.send_message(message.chat.id, info_text)
    if not (popular and new):
        tracks = get_tracks_json( popular=popular, new=new)
    else:
        tracks = get_tracks_json()
    if isinstance(tracks, list):
        print_tracks_response(bot, message, tracks)
        if popular:
            keyboard.show_popular_tracks_download_keyboard(message, bot)
        elif new:
            keyboard.show_new_tracks_download_keyboard(message, bot)


def get_popular_tracks(bot, message):
    get_tracks(bot, message, info_text='🔍Ищу популярные треки...', popular=True)


def get_new_tracks(bot, message):
    get_tracks(bot, message, info_text='🔍Ищу новинки...', new=True)


def get_tracks_by_query(bot, message):
    input_query_msg = bot.reply_to(message, '💬Введите запрос:')
    bot.register_next_step_handler(input_query_msg, save_query_and_input_artist_param, bot=bot)


def save_query_and_input_artist_param(msg, bot):
    TrackManager.query = msg.text
    artist_query_msg = bot.reply_to(msg, '💬Выберите режим поиска. Если хотите искать по исполнителю, введите "1", если по названию - введите "0".')
    bot.register_next_step_handler(artist_query_msg, save_artist_param, bot=bot)


def save_artist_param(message, bot):
    try:
        TrackManager.search_by_artist = int(message.text)
        assert TrackManager.search_by_artist in (0, 1)
        print_tracks(message, bot)
    except (ValueError, AssertionError) as exc:
        logger.error(exc)
        bot.send_message(message.chat.id, 'Режим поиска должен быть числом 0 или 1. Попробуйте ввести запрос снова.')
        keyboard.show_tracks_keyboard(bot, message)


def print_tracks(message, bot):
    bot.send_message(message.chat.id, f'🔍Ищу треки по запросу "{TrackManager.query}"...')
    tracks = get_tracks_json(artist=TrackManager.search_by_artist)
    print_tracks_response(bot, message, tracks=tracks)

    if not tracks_dict_is_empty(tracks):
        keyboard.show_tracks_menu_keyboard(bot, chat_id=message.chat.id, tracks_page=TrackManager.page)
        # keyboard.show_tracks_download_keyboard(bot, message)
    else:
        keyboard.show_back_button(bot, message)


def make_download_api_url(download_mode: str | None = None, popular=False, new=False) -> str:
    if popular:
        return f'{API_URL}/track/download?popular=1'
    elif new:
        return f'{API_URL}/track/download?new=1'
    else:
        artist = TrackManager.search_by_artist
        if download_mode:
            return f'{API_URL}/track/download?q={TrackManager.query}&mode={download_mode}&artist={artist}&page={TrackManager.page}'
        else:
            return f'{API_URL}/track/download?q={TrackManager.query}&mode=all&artist={artist}&page={TrackManager.page}'


def download_popular_tracks(bot, message):
    bot.send_message(message.chat.id, f'⏳Скачиваю популярные треки...')
    url = make_download_api_url(popular=True)
    get_musapi_response(bot, message, url)


def download_new_tracks(bot, message):
    bot.send_message(message.chat.id, f'⏳Скачиваю новинки...')
    url = make_download_api_url(new=True)
    get_musapi_response(bot, message, url)


def prepare_download_api_url(message, bot, download_mode):
    api_url = make_download_api_url(download_mode=download_mode)
    match download_mode:
        case 'first_n':
            n_input_msg = bot.reply_to(message, 'Режим скачивания первых нескольких треков. Сколько хотите скачать?')
            bot.register_next_step_handler(n_input_msg, prepare_to_download_first_n, bot=bot, api_url=api_url)
        case 'by_numbers':
            nums_input_msg = bot.reply_to(
                message, 'Режим скачивания треков по их номерам в списке.\nВведите номера нужных треков. Вводить номера треков нужно через запятую без пробелов. Например: 2,3,6,10,15'
            )
            bot.register_next_step_handler(nums_input_msg, prepare_to_download_by_numbers, bot=bot, api_url=api_url)


def prepare_to_download_first_n(message: Message, bot: TeleBot, api_url: str) -> None:
    try:
        TrackManager.tracks_to_download_count = int(message.text)
        assert TrackManager.tracks_to_download_count >= 1
        api_url += f'&n={TrackManager.tracks_to_download_count}'
        begin_tracks_download(message, bot, api_url, tracks_count=TrackManager.tracks_to_download_count)
    except ValueError as exc:
        logger.error(exc)
        bot.send_message(message.chat.id, '⚠️Количество треков должно быть числом.')
        keyboard.show_first_n_dmode_btn(bot, message)
    except AssertionError as exc:
        logger.error(exc)
        bot.send_message(message.chat.id, '⚠️Количество треков должно быть не меньше 1.')
        keyboard.show_first_n_dmode_btn(bot, message)


def prepare_to_download_by_numbers(message, bot, api_url):
    TrackManager.track_nums = message.text
    api_url += f'&track_nums={TrackManager.track_nums}'
    tracks_count = len(TrackManager.track_nums.split(','))
    begin_tracks_download(message, bot, api_url, tracks_count=tracks_count)


def begin_tracks_download(message, bot, api_url, tracks_count):
    track_word = utils.make_track_word(tracks_count=tracks_count)  # трек или треков (в зависимости от числа скачиваемых треков)
    bot.send_message(message.chat.id, f'⏳Идет скачивание {tracks_count} {track_word}...')
    download_by_url(bot=bot, msg=message, url=api_url)


def get_musapi_response(bot, message, url):
    session = HTMLSession()
    response = session.get(url)
    response_text = utils.make_response_message(response, logger, mode='tracks')
    keyboard.show_back_button(bot, message, response_text)


def common_download(bot, message, download_mode='all') -> None:
    url = make_download_api_url(bot, message, download_mode)
    get_musapi_response(bot, message, url)


def download_by_url(bot, msg, url) -> None:
    get_musapi_response(bot, msg, url)


def download_tracks(bot: TeleBot, message, download_mode='all', popular=False, new=False) -> None:
    # ''' Execute track/download API method. '''
    if popular:
        download_popular_tracks(message, bot)
    elif new:
        download_new_tracks(message, bot)
    else:
        if download_mode in ('all', 'only_one'):
            common_download(bot, message, download_mode)
        elif download_mode in ('first_n', 'by_numbers'):
            prepare_download_api_url(message, bot, download_mode)
        else:
            logger.error(f'В запросе к музыкальному API указан неверный параметр download_mode: {download_mode}')
