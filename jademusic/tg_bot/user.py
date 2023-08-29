import requests
import logging

import utils
import tracks

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='INFO')


def make_user_dict(message):
    return {
        'username': message.from_user.username,
        'telegram_user_id': message.from_user.id,
        'password': utils.create_user_password()
    }


def register_user(message):
    register_url = f'{tracks.API_URL}/auth/users/'
    tg_username = message.from_user.username
    tg_user_id = message.from_user.id
    user_dict = make_user_dict(message)
    response = requests.post(url=register_url, data=user_dict)
    logger.info(f'Зарегистрирован новый пользователь: имя: {tg_username}, ID: {tg_user_id}.')
    # authorize_user(user_dict, message)


# def get_user_id(message):
#     get_user_id_url = f'{tracks.API_URL}/user/get_by_tg_id?tg_id={message.from_user.id}'
#     response = requests.get(url=get_user_id_url)
#     return response.json().get('user_id')


def check_user_is_registered(message):
    check_url = f'{tracks.API_URL}/user/register/check?user_id={message.from_user.id}'
    response = requests.get(check_url)
    user_is_registered = response.json()['is_registered']
    if user_is_registered:
        return True
    return False
