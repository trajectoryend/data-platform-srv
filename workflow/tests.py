import hashlib

from django.test import TestCase

# Create your tests here.
import time
import requests
timestamp = str(time.time())[:10]
ori_str = timestamp + '4e57d414-c6aa-11ea-9ed0-784f437daad6'
signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
headers = dict(signature=signature, timestamp=timestamp, appname='ops', username='admin')


get_data = dict(per_page=20, category='all')
r = requests.get('http://202.194.98.183/api/v1.0/tickets', headers=headers, params=get_data)
result = r.json()
print(result)
