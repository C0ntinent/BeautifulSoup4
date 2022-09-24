from random import choice

import requests
from bs4 import BeautifulSoup


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text

    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='table table-striped '
                                    'table-bordered').findAll(
        'tr')[1:]

    proxies1 = []
    proxies2 = []
    for tr in trs:
        tds = tr.findAll('td')
        if tds[6].text.strip() == 'no':
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            schema = 'http'
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies1.append(proxy)
        else:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            schema = 'https'
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies2.append(proxy)
    return choice(proxies1), choice(proxies2)


def get_html(url):
    # proxies = {'https': 'ipaddress:5000'}
    p = get_proxy()  # {'schema': 'http(s)', 'address': 'x.xxx.xx.xxx:xxxx'}

    proxy = {p[0]['schema']: p[0]['address'], p[1]['schema']: p[1]['address']}
    r = requests.get(url, proxies=proxy, timeout=3.0, verify=False)
    return r.json()['origin']


def main():
    url = 'https://httpbin.org/ip'
    print(get_html(url))


if __name__ == '__main__':
    main()
