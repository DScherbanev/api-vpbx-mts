import requests
import os
import json
import csv
# import pprint
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VPBX_API_TOKEN = os.getenv('VPBX_API_TOKEN')
CALL_HISTORY_ENDPOINT = 'https://vpbx.mts.ru/api/v1/callHistory/enterprise'
CALL_REC_ENDPOINT = 'https://vpbx.mts.ru/api/callRecording/mp3/'
PAGE_SIZE = 10
DATE_FROM = '01/01/2022'
DATE_TO = '19/04/2022'


def date_to_timestamp(date_time):
    """Преобразование даты в UNIX timestamp."""
    return int(datetime.strptime(date_time, '%d/%m/%Y').timestamp() * 1000)


def timestamp_to_date(timestamp):
    """Преобразование UNIX timestamp в дату."""
    return datetime.fromtimestamp(timestamp / 1000).strftime('%d-%m-%Y')


def timestamp_to_date_time(timestamp):
    """Преобразование UNIX timestamp в дату-время."""
    return datetime.fromtimestamp(timestamp / 1000).strftime('%d-%m-%Y_%H-%M-%S')


def get_api_response(page):
    params = {
        'status': 'PLACED',
        'dateFrom': date_to_timestamp(DATE_FROM),
        'dateTo': date_to_timestamp(DATE_TO),
        'page': page,
        'size': PAGE_SIZE,
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }
    response = requests.get(CALL_HISTORY_ENDPOINT, params=params)
    total_elements = response.json()['totalElements']
    total_pages = response.json()['totalPages']
    call_history = response.json()['content']
    return total_elements, total_pages, call_history


def save_call_record_mp3(call_id, calling_num, called_num, call_time_ts, call_duration):
    rec_params = {
        'X-AUTH-TOKEN': VPBX_API_TOKEN,
        'cache-control': 'no-cache'
    }
    response = requests.get(CALL_REC_ENDPOINT + call_id,
                            params=rec_params, allow_redirects=True)
    if response.status_code == 200:
        filename = (calling_num + '_' + called_num + '_' +
                    timestamp_to_date_time(call_time_ts) +
                    '_' + str(call_duration) + '.mp3')
        open(filename, 'wb').write(response.content)
        print('Записан файл:', filename)
    # else:
    #     print('Код ответа:', response.status_code)


def main():
    total_elements, total_pages, call_history = get_api_response(0)

    csv_file = open('call_history.csv', 'w')
    with csv_file:
        fieldnames = ['callTime', 'redirectingNumber', 'callingNumber', 'answerDuration', 'callGroupId', 'status', 'calledNumber', 'userId', 'duration', 'redirectingReason',
                      'timeZone', 'departmentBwksId', 'groupBwksId', 'direction', 'abonentName', 'recordAbonentId', 'terminationCause', 'extTrackingId', 'enterpriseBwksId']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(total_pages):
            call_history = get_api_response(page)[2]
            elements_on_page = len(call_history)

            for element in range(elements_on_page):
                call_id = call_history[element]['extTrackingId']
                calling_num = call_history[element]['callingNumber'].replace(
                    '+7', '8')
                called_num = call_history[element]['calledNumber'].replace(
                    '+7', '8')
                call_time_ts = call_history[element]['callTime']
                call_duration = call_history[element]['duration']
                # print(call_id, calling_num, called_num, timestamp_to_date_time(call_time_ts), call_duration)
                save_call_record_mp3(call_id, calling_num,
                                     called_num, call_time_ts, call_duration)
                writer.writerow(call_history[element])


if __name__ == '__main__':
    main()
