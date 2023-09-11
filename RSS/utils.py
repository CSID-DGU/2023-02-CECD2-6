import re
import html

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