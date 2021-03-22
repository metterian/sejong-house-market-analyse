import os, sys, json, request
from xml.etree.ElementTree import parse
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



SECRET_KEY = secrets['Enecoding']
END_POINT = secrets['EndPoint']




URL = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo?serviceKey=e6f2sK93S3aN6ATmb4IhF93YYBcgs3lWqWdouHYQi1UKR00yhYUsgXpdW7TWat1n91N07BnW7U3MGSQojJK6bw%3D%3D&sigunguCd=36110&bjdongCd=10200&platGbCd=0&bun=0531&ji=0000&numOfRows=100&pageNo=1"



response = urlopen(URL, timeout=60).read()

decode_data = response.decode('utf-8')

xml_parse = xmltodict.parse(decode_data)
xml_dict = json.loads(json.dumps(xml_parse))

with open('api.json', 'w') as outfile:
    json.dump(xml_dict, outfile, ensure_ascii=False)
# cc = xmltodict.parse(tree) # return collections.OrderedDict
# dd = json.loads(json.dumps(cc)) # return dict
# animals = dd['animals']['animal']
# print(animals) # 결과를 출력한다




