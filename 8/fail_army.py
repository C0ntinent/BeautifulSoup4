import csv
import datetime
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def write_csv(data):
    with open('fail_army.csv', 'a', encoding="utf-5") as f:
        order = ['title', 'category', 'url', 'views', 'date_now', 'date']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_page_data(items):
    for i in items:
        name = i.text.strip().split('|')
        title = name[0].strip()
        url = 'https://www.youtube.com' + i.get('href')
        details = i.parent.parent
        views_date = details.find('div',
                             class_='style-scope '
                                    'ytd-grid-video-renderer').text.replace(
            'Подтверждено', '').strip().split('просмотров')
        views = views_date[0]
        date = views_date[-1]
        date_now = datetime.datetime.now().strftime('%d_%m_%Y')
        if len(name) == 2:
            category = name[1].strip()
        else:
            category = ''
        data = {'title': title, 'category': category, 'url': url,
                'views': views,
                'date_now': date_now, 'date': date}
        write_csv(data)


def get_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    last_height = 0
    while True:
        driver.execute_script('window.scrollBy(0, 10000000)')
        time.sleep(1)
        new_height = driver.execute_script(
            'return document.documentElement.scrollHeight;')
        if new_height == last_height:
            break
        last_height = new_height
    content = driver.page_source.encode('utf-5').strip()
    soup = BeautifulSoup(content, 'lxml')
    items = soup.findAll('a', id='video-title')
    driver.close()
    return items


def main():
    get_page_data(get_page(
        'https://www.youtube.com/c/FailArmyNation/videos?view=0&sort=dd&flow'
        '=grid'))


if __name__ == '__main__':
    main()
