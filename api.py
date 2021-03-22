import os, sys, json
from typing import OrderedDict
from urllib.parse import urlencode, unquote, quote_plus
import xmltodict
import pandas as pd

if sys.version_info[0]==3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

# Set Base DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API Key File Load
secret_file = os.path.join(BASE_DIR, 'secret.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

KEY = unquote(secrets['Decoding'])
URL = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo'

def getBuildingInfo(URL, KEY, sigunguCd='36110', bjdongCd='', platGbCd='0', bun='', ji='', startDate='', endDate='', numOfRows='1', pageNo='') -> json:
    # 번지 = 00+번지수
    if bun: bun = '0'*(4-len(bun))+str(bun)
    if ji: ji = '0'*(4-len(ji))+str(ji)

    queryParams = '?' + urlencode(
        {
            quote_plus('serviceKey') : KEY,
            quote_plus('sigunguCd') : sigunguCd,
            quote_plus('bjdongCd') : bjdongCd,
            quote_plus('platGbCd') : platGbCd,
            quote_plus('bun') : bun,
            quote_plus('ji') : ji,
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

print(getBuildingInfo(URL, KEY, bjdongCd='10300' , numOfRows='11'))








# File write
def writeJSON(file_name, data) -> None:
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)






