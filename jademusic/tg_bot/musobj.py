from requests_html import HTMLSession
import json

import keyboard


def get_response_json(url):
    session = HTMLSession()
    response = session.get(url)
    return json.loads(response.text)


def make_musobj_str(musobjs):
    musobj_string = ''
    for m in musobjs:
        musobj_string += str(m['id']) + ') ' + m['title'] + '\n'
    return musobj_string


def print_musobjs(bot, message, musobj, musobjs_string):
    if musobj:
        bot.send_message(message.chat.id, f'Найдено плейлистов: {len(musobj)}\n{musobjs_string}')
    else:
        keyboard.show_back_button(bot, message, text='✖️Плейлисты не найдены.')