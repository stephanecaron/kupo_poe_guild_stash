import requests
from requests.cookies import RequestsCookieJar
import json
from dotenv import load_dotenv
import os
from os.path import join, dirname
from time import sleep

envpath = join(dirname(__file__),"../.env")

load_dotenv(envpath)

poe_session_id = os.getenv('poe_sess_id')
guild_profile_id = os.getenv('guild_profile_id')

cookie_jar = RequestsCookieJar()
cookie_jar.set('POESESSID', poe_session_id, domain='www.pathofexile.com', path='/')

headers = {
    'User-Agent': 'LHBA guild inventory/transaction tracker, @stephanecaron github'
}


def get_initial_fetch():
    print('initial fetch request...')
    response = requests.get(f'https://www.pathofexile.com/api/guild/{guild_profile_id}/stash/history', cookies=cookie_jar, headers=headers)

    if response.status_code == 200:
        print('received fetch, parsing..')
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
        

def get_further_fetch(last_time, last_id):
    response = requests.get(f'https://www.pathofexile.com/api/guild/{guild_profile_id}/stash/history?from={last_time}&fromid={last_id}', cookies=cookie_jar, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None