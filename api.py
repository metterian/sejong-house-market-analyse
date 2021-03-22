import os, sys, json, request
from xml.etree.ElementTree import parse
from urllib.parse import urlencode, unquote, quote_plus
import xmltodict

if sys.version_info[0]==3:
    from urllib.request import urlopen
else:
    from urllib import urlopen


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Secret File Load
secret_file = os.path.join(BASE_DIR, 'secret.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

KEY = unquote(secrets['Decoding'])

URL = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo'
queryParams = '?' + urlencode(
    {
        quote_plus('serviceKey') : KEY,
        quote_plus('sigunguCd') : '36110',
        quote_plus('bjdongCd') : '10300',
        quote_plus('platGbCd') : '0',
        quote_plus('bun') : '',
        quote_plus('ji') : '',
        quote_plus('startDate') : '',
        quote_plus('endDate') : '',
        quote_plus('numOfRows') : '5000',
        quote_plus('pageNo') : '1'
        }
)

response = urlopen(URL + queryParams).read()
decode_data = response.decode('utf-8')

xml_parse = xmltodict.parse(decode_data)
xml_dict = json.loads(json.dumps(xml_parse))


# File write
with open('api.json', 'w') as outfile:
    json.dump(xml_dict, outfile, ensure_ascii=False)






