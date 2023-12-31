import re
import html
import json
import os
import sys
from datetime import datetime

def removeHtmlTags(text):
    clean = re.compile('<.*?>|</.*?>|<.*?/>')
    return re.sub(clean, '', text)

def containHtmlTags(text):
    pattern = re.compile('<.*?>|</.*?>|<.*?/>')
    return bool(pattern.search(text))

def removeHtmlEntities(text):
    clean = re.compile('&.*?;')
    return re.sub(clean, '', text)

def containHtmlEntities(text):
    pattern = re.compile('&.*?;')
    return bool(pattern.search(text))

def convertHtmlEntities(text):
    return html.unescape(text).replace('\xa0',' ')

def LoadJsonFile(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            _jsonData = json.load(f)
            return _jsonData
    except Exception:
        return None
    
def getHomePath(path):
    home=os.environ.get('GDSPATH', os.environ.get('HOME')+'\\2023-02-CECD2-6')
    ret=os.path.join(home, path).replace('\\','/')
    return ret

# time1이 더 빠르면 -1, 느리면 1, 같으면 0
def CompareTimeStamp(time1,time2):
    t1=datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    t2=datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')

    if(t1<t2):
        return -1
    elif(t1>t2):
        return 1
    else:
        return 0
    
def ConvertRFC2822(s):
    ret=datetime.strptime(s, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
    return ret