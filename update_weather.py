# -*- coding: utf-8 -*-
import time
import requests
import xml.etree.ElementTree as ET

from os import fdopen, remove
from tempfile import mkstemp
from shutil import move


def update(file_path, content, icon):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.startswith('content'):
                    new_file.write('content: %s\n' % content)
                elif line.startswith('icon'):
                    new_file.write('icon: %s\n' % icon)
                else:
                    new_file.write(line)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def get_weather():
    r = requests.get('http://php.weather.sina.com.cn/xml.php?city=%C9%CF%BA%A3&password=DJOYnieT8234jlsK&day=0')
    # print type(r.text)    --> unicode
    # inner encoding transfer
    r.encoding = 'utf-8'
    raw_xml = r.text
    # print type(raw_xml)   --> unicode
    # print type(raw_xml.encode('utf-8'))   --> str

    tree = ET.fromstring(raw_xml.encode('utf-8'))
    city = tree.find('./Weather/city')
    status = tree.find('./Weather/status1')
    # print type(city.text) --> unicode
    return "%s %s" % (city.text, status.text)


def find_icon(content):
    icons = {'晴': 'sun', '云': 'cloud', '雨': 'rain', '雪': 'snowflake', '风': 'cloud'}
    for key in icons:
        if key in content:
            return icons[key]
    return '点击查询'


if __name__ == '__main__':
    while True:
        content = get_weather().encode('utf-8')     # unicode --> str
        icon = find_icon(content)
        update('./_data/message.yml', content, icon)
        time.sleep(60*60*3)
