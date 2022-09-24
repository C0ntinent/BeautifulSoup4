from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    return requests.get(url).text


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        write = csv.writer(f)

        write.writerow([data['name'],
                        data['price'],
                        data['url'],
                        data['time'],
                        ])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[1].find('a').text
        price = tds[2].text
        url = 'https://www.investing.com/equities' + tds[1].find('a').get(
            'href')
        time_ = tds[8].text
        data = {'name': name,
                'price': price,
                'url': url,
                'time': time_
                }
        write_csv(data)


def main():
    url = 'https://www.investing.com/equities/'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
