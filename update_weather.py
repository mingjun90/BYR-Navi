# -*- coding: utf-8 -*-
import time
import datetime
import requests
import xml.etree.ElementTree as ET

from os import fdopen, remove
from tempfile import mkstemp
from shutil import move


def update(file_path, content, icon):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, "w") as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.startswith("content"):
                    new_file.write("content: %s\n" % content)
                elif line.startswith("icon"):
                    new_file.write("icon: %s\n" % icon)
                else:
                    new_file.write(line)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def get_weather():
    try:
        r = requests.get("http://php.weather.sina.com.cn/xml.php?city=%C9%CF%BA%A3&password=DJOYnieT8234jlsK&day=0")
        # print type(r.text)    --> unicode
        # inner encoding transfer
        r.encoding = "utf-8"
        raw_xml = r.text
        print raw_xml
        # print type(raw_xml)   --> unicode
        # print type(raw_xml.encode("utf-8"))   --> str

        tree = ET.fromstring(raw_xml.encode("utf-8"))
        city = tree.find("./Weather/city")
        # print type(city.text) --> unicode
        status = tree.find("./Weather/status1")
        if city and status:
            result = "%s %s" % (city.text, status.text)
            result = result.encode("utf-8")     # unicode --> str
    except Exception as e:
        print datetime.datetime.now(), e
        result = "点击查询"
    return result


def find_icon(content):
    icons = {"晴": "sun", "云": "cloud", "雨": "rain", "雪": "snowflake", "风": "cloud"}
    for key in icons:
        if key in content:
            return icons[key]
    return "sun"


if __name__ == "__main__":
    while True:
        content = get_weather()     # unicode --> str
        icon = find_icon(content)
        update("./_data/message.yml", content, icon)
        time.sleep(60*60*3)
