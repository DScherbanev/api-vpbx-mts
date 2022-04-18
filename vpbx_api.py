import time
import datetime
import requests
import os
import json
import pprint
from dotenv import load_dotenv

load_dotenv()

VPBX_API_TOKEN = os.getenv('VPBX_API_TOKEN')
CALL_HISTORY_ENDPOINT = 'https://vpbx.mts.ru/api/v1/callHistory/enterprise'
CALL_REC_ENDPOINT = 'https://vpbx.mts.ru/api/callRecording/mp3/'


def date_time_to_timestamp(date_time):
    return int(datetime.datetime.strptime(date_time, '%Y/%m/%d').timestamp()*1000)

def timestamp_to_date_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y_%m_%d ')


def main():
    params = {
        'status': 'PLACED',
        'dateFrom': date_time_to_timestamp('2022/01/01'),
        'dateTo': date_time_to_timestamp('2022/04/11'),
        'page': 0,
        'size': 50,
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }
    response = requests.get(CALL_HISTORY_ENDPOINT, params=params)
    call_history = response.json()['content']

    n = 2

    print('Всего записей в истории звонков:', len(call_history))
    call_id = call_history[n]['extTrackingId']
    calling_num = call_history[n]['callingNumber']
    called_num = call_history[n]['calledNumber']
    call_time_ts = call_history[n]['callTime']

    print(call_id, calling_num, called_num, timestamp_to_date_time(call_time_ts))
    print('totalElements', response.json()['totalElements'])
    print('Pages', response.json()['totalPages'])

    print('--------------------------------')
    print('DateFrom: ', date_time_to_timestamp('2022/01/01'), timestamp_to_date_time(date_time_to_timestamp('2022/01/01')))
    print('DateTo:', date_time_to_timestamp('2022/04/11'), timestamp_to_date_time(date_time_to_timestamp('2022/04/11')))
    print('--------------------------------')
    pprint.pprint(call_history[n])

    rec_params = {
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }

    response = requests.get(CALL_REC_ENDPOINT  + call_id, params=rec_params, allow_redirects=True)

    if response.status_code == 200:
        filename = calling_num + '_'  + called_num + '.mp3'
        open(filename, 'wb').write(response.content)
        print('Записан файл: ', filename)
    else:
        print('Код ответа: ', response.status_code)


if __name__ == '__main__':
    main()
