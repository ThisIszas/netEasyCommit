import requests
import re
import get_params_and_encSecKey
from MySqlConnection import MysqlConnections
import json
import time
import random


def get_params_and_enc_sec_key(first_params):
    get_p_and_e = get_params_and_encSecKey
    params = get_p_and_e.get_params(first_params)
    encSecKey = get_p_and_e.get_encSecKey()
    return params, encSecKey


def get_json(url, params, encSecKey):
    headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
    }
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


def make_first_params(offset):
    first_param = "{rid:\"\", offset:\"%s\", total:\"true\", limit:\"20\", csrf_token:\"\"}" % offset
    return first_param

if __name__ == '__main__':
    offset = 2910
    first_params = make_first_params(0)
    my_sql_tool = MysqlConnections()
    start_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_479219553?csrf_' \
                'token=5119e36713988578f9ab77e2ee52a010'
    music_id = re.findall('R_SO_4_(.*?)\?', start_url, re.S)[0]
    while True:
        params, enc_sec_key = get_params_and_enc_sec_key(first_params)
        response_text = get_json(start_url, params, enc_sec_key)
        json_dict = json.loads(response_text)
        print json_dict['total']
        for item in json_dict['comments']:
            print "Music ID: " + str(music_id)
            comments = item['content'].encode('utf-8', 'ignore')
            print comments
            my_sql_tool.insert_info(music_id, comments)
        interval_time = random.uniform(3, 6)
        time.sleep(interval_time)
        if not json_dict:
            break
        else:
            first_params = make_first_params(offset)
            offset += 10
            print "Offset " + str(offset)


