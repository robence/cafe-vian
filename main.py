import requests

from lxml import html
from locale import str
from dotenv import load_dotenv
from builtins import list, set, dict, range, print
from pathlib import Path
import os
import datetime
import time

env_path = Path(__file__).parent.absolute() / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")


def get_cafe_vian_menu(weekday):
    BASE_URL = 'https://www.cafevian.com/ebedmenue'
    session_requests = requests.session()

    # returns inner iframe url
    def parse_main_html():
        result = session_requests.get(BASE_URL)
        tree = html.fromstring(result.text)

        # get inner data url to fetch
        id_selector = '//div[@id="gaax5inlineContent-gridContainer"]'
        iframe_element = tree.xpath(id_selector + '/wix-iframe/iframe')[0]
        src_url = iframe_element.attrib['data-src']
        return src_url

    def parse_iframe_html(src_url):
        iframe_result = session_requests.get(src_url)
        iframe_tree = html.fromstring(iframe_result.text)
        return iframe_tree

    src_url = parse_main_html()
    iframe_tree = parse_iframe_html(src_url)

    # declare selectors
    div_selector = '//div[@id="mainDiv"]'
    place_selector = '/div/div/section/div/ul/li[3]'

    day_selector = div_selector + place_selector + \
        "/ul/li[" + str(weekday+1) + "]"
    main_course_selector = day_selector + '/div/div[2]'
    appetizer_selector = day_selector + '/ul/li/div/div/span'

    # menu information
    title = "Café Vian Bisztró"
    place = iframe_tree.xpath(div_selector + place_selector + "/h3")[0].text

    day = iframe_tree.xpath(day_selector + '/div/div/div/span/span')[0].text
    main_course = iframe_tree.xpath(main_course_selector)[0].text
    appetizer = iframe_tree.xpath(appetizer_selector)[0].text

    def strip_text(x): return ' '.join(x.split()).replace("\uf077", "-")
    formatted_main_course = strip_text(main_course)

    menu = '%s | %s\n\n%s\n%s\n' % (
        title, place, formatted_main_course, appetizer)

    # print(day)
    return menu


def get_weekday():
    weekday = datetime.datetime.today().weekday()
    return weekday


def main():
    weekday = get_weekday()
    menu = get_cafe_vian_menu(weekday)
    print(menu)

    # print(SLACK_API_TOKEN)
    # x = SLACK_API_TOKEN.split(',')
    # print("x")
    # print(x)


if __name__ == "__main__":
    main()
