#%%
from json import encoder
import os, sys, json, csv
from typing import OrderedDict
from urllib.parse import urlencode, unquote, quote_plus
from pandas.core.frame import DataFrame
import xmltodict
import pandas as pd
from collections import OrderedDict
from tqdm import tqdm

if sys.version_info[0]==3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

# Set Base DIR
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API Key File Load
secret_file = os.path.join('./', 'secret.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

KEY = unquote(secrets['Decoding'])
URL = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo'

""" Get 전유부 Data from Open API"""
def querySender(URL, KEY, sigunguCd='36110', bjdongCd='', platGbCd='', bun='', ji='', startDate='', endDate='', numOfRows='1', pageNo='', maxRows=False) -> json:
    # 번지 = 00+번지수
    if bun: bun = '0'*(4-len(bun))+str(bun)
    if ji: ji = '0'*(4-len(ji))+str(ji)

    queryParams = '?' + urlencode(
        {
            quote_plus('serviceKey') : KEY, # API KEY
            quote_plus('sigunguCd') : sigunguCd, # 시군구 코드
            quote_plus('bjdongCd') : bjdongCd, # 법정동 코드
            quote_plus('platGbCd') : platGbCd, # 대지구분 코드
            quote_plus('bun') : bun, # 번
            quote_plus('ji') : ji, # 지
            quote_plus('startDate') :startDate,
            quote_plus('endDate') : endDate,
            quote_plus('numOfRows') : numOfRows,
            quote_plus('pageNo') : pageNo,
            }
    )

    response = urlopen(URL + queryParams).read()
    decode_data = response.decode('utf-8')
    xml_parse =  xmltodict.parse(decode_data)
    xml_dict = json.loads(json.dumps(xml_parse))
    return xml_dict

# Write JSON file
def writeJSON(file_name, data, mode) -> None:
    with open(file_name, mode) as outfile:
        json.dump(data, outfile, ensure_ascii=False)

# Write CSV file
def writeCSV(file_name, data, mode) -> None:
    with open(file_name, mode, encoding='utf-8-sig', newline='') as f:
        cw = csv.writer(f)
        cw.writerow(data)

# get data from request parameter
def getDataFromPara(item):
    data = [
        isNone(item['platPlc']),# 대지주소
        isNone(item['sigunguCd']),# 시군구코드
        isNone(item['bjdongCd']),# 법정동코드
        isNone(item['dongNm']),# 동명칭
        isNone(item['hoNm']),# 호명칭
        isNone(item['flrGbCd']),# 층구분코드
        isNone(item['flrNo']),# 층번호
        isNone(item['area']),# 면적(전용면적)
        isNone(item['bldNm']),# 건물명
        isNone(item['bun']),# 번
        isNone(item['ji']),# 지
        isNone(item['mainPurpsCdNm']),# 용도코드명
        isNone(item['mainPurpsCd']),# 주용도코드
        isNone(item['etcPurps']),# 기타용도
    ]
    return data

def isNone(item):
    if not item:
        return ''
    else: return str(item)


# get bjdongCd(법정동) codes
b_info = pd.read_csv('data/2.세종시_표제부.csv',  dtype={'로트':object, '법정동코드': str})
law_codes = b_info['법정동코드'].unique().tolist()

#%%
# get Count Data from API
count = OrderedDict()
for law_code in law_codes:
    bld_info = querySender(URL, KEY, bjdongCd=law_code)
    totalCount = bld_info['response']['body']['totalCount']
    count[law_code] = totalCount


# Columns setting
columns = ['대지주소', '시군구코드', '법정동코드', '동명칭', '호명칭', '층구분코드', '층번호', '면적(전용면적)', '건물명', '번', '지', '용도코드명', '주용도코드', '기타용도']
writeCSV(file_name='전유부.csv', data=columns, mode='w')

#%%

for law_code in law_codes:
    data_count = int(count[law_code])

    # case of None in item
    if not data_count:
        continue

    # Data Partition
    numOfRows = (data_count // 4)
    maxPage = 4 + 1

    for pageNo in tqdm(range(1, maxPage+1)):
        try:
            query = querySender(URL, KEY, bjdongCd=law_code, numOfRows=numOfRows, pageNo=pageNo)
        except:
            print("Not success : ",law_code)
            continue

        items = query['response']['body']['items']

        if items:
            if isinstance(items['item'], list):
                for item in items['item']:
                    data = getDataFromPara(item)
                    writeCSV('전유부.csv', data, "a")
            else:
                data = getDataFromPara(item)
                writeCSV('전유부.csv', data, "a")

#%%
