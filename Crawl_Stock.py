from numpy.lib.npyio import load
import requests
import json
from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

resp = requests.get(
    'https://cn.investing.com/equities/apple-computer-inc-historical-data', headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

# print(soup.find('table', 'genTbl closedTbl historicalTbl'))


th_data = soup.find(
    'table', 'genTbl closedTbl historicalTbl').find('thead').find_all('th')
td_data = soup.find(
    'table', 'genTbl closedTbl historicalTbl').find('tbody').find_all('td')

th_list_data = []
td_list_data = []

for th_d in th_data:
    th_list_data.append(th_d.text.strip())
# print(th_list_data)

for td_d in td_data:
    td_list_data.append(td_d.text.strip())
# print(td_list_data)

dict_data = defaultdict(list)
for idx in range(0, len(td_list_data)):
    dict_data[th_list_data[idx % 7]].append(td_list_data[idx])
# print(dict_data)

json_data = json.dumps(dict_data, ensure_ascii=False)
# print(json_data)

loads_data = json.loads(json_data)  # Revert to dict
# print(loads_data)


# 輸入想要擷取的日期（一個月內），會顯示出日期範圍內的股價資料
def get_data_by_day(find_day):
    if find_day not in loads_data['日期']:
        print('日期可能為假日或太久遠')
        return
    print('    日期     ', ' 收盘 ', ' 开盘 ', '  高  ', '  低  ', '交易量', '涨跌幅')
    for idx in range(len(loads_data['日期'])):
        if loads_data['日期'][idx] != find_day:
            print(loads_data['日期'][idx], loads_data['收盘'][idx], loads_data['开盘'][idx], loads_data['高']
                  [idx], loads_data['低'][idx], loads_data['交易量'][idx], loads_data['涨跌幅'][idx])


def get_data_with_datatable(days=10):
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    df = pd.DataFrame(loads_data)
    print(df.head(days))


if __name__ == '__main__':
    get_data_by_day('2021年6月23日')
    get_data_with_datatable()
