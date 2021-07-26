import requests
import json
import datetime as dt
from collections import defaultdict
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
resp = requests.get(
    'https://cn.investing.com/equities/apple-computer-inc-historical-data', headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')


th_data = soup.find(
    'table', 'genTbl closedTbl historicalTbl').find('thead').find_all('th')
td_data = soup.find(
    'table', 'genTbl closedTbl historicalTbl').find('tbody').find_all('td')

th_list_data = []
td_list_data = []

for th_d in th_data:
    th_list_data.append(th_d.text.strip())
for td_d in td_data:
    td_list_data.append(td_d.text.strip())


loads_data = defaultdict(list)
for idx in range(0, len(td_list_data)):
    loads_data[th_list_data[idx % 7]].append(td_list_data[idx])


def chinese_day_trans_to_datetime(someday):
    year, temp = someday.split('年')[0], someday.split('年')[1]
    month, temp2 = temp.split('月')[0], temp.split('月')[1]
    day = temp2.split('日')[0]
    return dt.datetime(int(year), int(month), int(day))


def get_data_by_day(from_day, to_day):
    find_data = defaultdict(list)

    for someday in zip(loads_data['日期'], loads_data['收盘'], loads_data['开盘'], loads_data['高'], loads_data['低'], loads_data['交易量'], loads_data['涨跌幅']):
        someday_datetime = chinese_day_trans_to_datetime(someday[0])
        if from_day >= someday_datetime >= to_day:
            find_data['日期'].append(someday[0])
            find_data['收盘'].append(someday[1])
            find_data['开盘'].append(someday[2])
            find_data['高'].append(someday[3])
            find_data['低'].append(someday[4])
            find_data['交易量'].append(someday[5])
            find_data['涨跌幅'].append(someday[6])

    return find_data


if __name__ == '__main__':
    # 設定找尋範圍的「起始日期」與「最終日期」
    # from_day: 從哪個日期開始找, to_day: 找到哪個日期, 只能找一個月內交易日的資料
    from_day = dt.datetime(2021, 7, 23)
    to_day = dt.datetime(2021, 6, 28)

    # Transform to JSON
    json_data = json.dumps(get_data_by_day(
        from_day, to_day), ensure_ascii=False)
    print(json_data)
