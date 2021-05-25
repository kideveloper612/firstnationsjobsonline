import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    return driver


def write(lines, file_name):
    with open(file=file_name, encoding='utf-8', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def do_request(page):
    url = "https://firstnationsjobsonline.com/"
    payload = "{\"action\":\"facetwp_refresh\",\"data\":{\"facets\":{\"job_classification\":[],\"job_region\":[],\"job_location\":[],\"keyword\":\"\",\"paged\":161},\"frozen_facets\":{},\"http_params\":{\"get\":{\"fwp_paged\":\"161\"},\"uri\":\"\",\"url_vars\":[]},\"template\":\"wp\",\"extras\":{\"sort\":\"default\"},\"soft_refresh\":1,\"is_bfcache\":1,\"first_load\":0,\"paged\":%s}}" % (page)

    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def get_request(url):
    res = requests.get(url)
    return res


def main():
    driver = get_driver()

    for i in range(1, 164):
        res = json.loads(do_request(i).text)

        soup = BeautifulSoup(res['template'], 'html5lib')
        cards = soup.select(".elementor-post__text")
        for card in cards:
            url = card.a['href']
            driver.get(url)
            response_soup = BeautifulSoup(driver.page_source, "html5lib")
            options = response_soup.select(".elementor-icon-list-item")
            for option in options:
                if "@" in option.text:
                    email = option.text.strip()
                    print(email)
                    write([[email]], "email.csv")
                    break


if __name__ == '__main__':
    main()
