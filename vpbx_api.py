#import time
import requests
import os
import json
import pprint
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VPBX_API_TOKEN = os.getenv('VPBX_API_TOKEN')
CALL_HISTORY_ENDPOINT = 'https://vpbx.mts.ru/api/v1/callHistory/enterprise'
CALL_REC_ENDPOINT = 'https://vpbx.mts.ru/api/callRecording/mp3/'
PAGE_SIZE = 50
DATE_FROM = '2022/01/01'
DATE_TO = '2022/04/11'


def date_to_timestamp(date_time):
    """Преобразование даты в UNIX timestamp."""
    return int(datetime.strptime(date_time, '%Y/%m/%d').timestamp()*1000)

def timestamp_to_date(timestamp):
    """Преобразование UNIX timestamp в дату."""
    return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')

def timestamp_to_date_time(timestamp):
    """Преобразование UNIX timestamp в дату-время."""
    return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d_%H-%M-%S')


def main():
    params = {
        'status': 'PLACED',
        'dateFrom': date_to_timestamp(DATE_FROM),
        'dateTo': date_to_timestamp(DATE_TO),
        'page': 0,
        'size': PAGE_SIZE,
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }
    response = requests.get(CALL_HISTORY_ENDPOINT, params=params)
    total_elements = response.json()['totalElements']
    total_pages = response.json()['totalPages']

    call_history = response.json()['content']

    print('totalElements', total_elements)
    print('Pages', total_pages)

    n = 10

    call_id = call_history[n]['extTrackingId']
    calling_num = call_history[n]['callingNumber']
    called_num = call_history[n]['calledNumber']
    call_time_ts = call_history[n]['callTime']

    print(call_id, calling_num, called_num, timestamp_to_date_time(call_time_ts))


    # Вывод информации по конкретному звонку
    pprint.pprint(call_history[n])

    rec_params = {
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }

    response = requests.get(CALL_REC_ENDPOINT  + call_id, params=rec_params, allow_redirects=True)

    if response.status_code == 200:
        filename = calling_num + '_'  + called_num + '_' + timestamp_to_date_time(call_time_ts) +'.mp3'
        open(filename, 'wb').write(response.content)
        print('Записан файл: ', filename)
    else:
        print('Код ответа:', response.status_code)


if __name__ == '__main__':
    main()
