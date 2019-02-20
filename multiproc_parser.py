from multiprocessing import Pool
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
from datetime import datetime

print(UserAgent().chrome)


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, "lxml")
    trs = soup.find('table', id='fresh-table').find_all('tr')
    links = []
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            if td.text.strip() == "Россия":
                if tr.findChild('a') is not None:
                    a = tr.findChild('a').get('href')
            # n = tr.findChild('a').get_text()
            # if n == "FFENG":
            #     print(n)
                    link = 'http://catalog.expocentr.ru/' + a
                    links.append(link)
    return links

# Company_Name
# phone
# email
# url


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    head = soup.find('h3', class_='panel-title')
    source = soup.find('dl', class_="dl-horizontal")
    sdt = source.find_all('dt')
    phone = ''
    url_link = ''
    email = ''
    try:
        cn = head.text.strip()
    except:
        cn = ''
    for s in sdt:
        if s.text.strip() == 'Телефон:':
            try:
                phone = s.next_sibling.text.strip()
            except:
                phone = ''
        if s.text.strip() == 'Сайт:':
            try:
                url_link = s.next_sibling.text.strip()
            except:
                url_link = ''
        if s.text.strip() == 'E-mail:':
            try:
                email = s.next_sibling.text.strip()
            except:
                email = ''

    data = {'cn': cn,
            'phone': phone,
            'email': email,
            'url': url_link
            }
    return data


def write_csv(data):
    with open('expocentr-data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['cn'],
                         data['phone'],
                         data['email'],
                         data['url']))
    print(data['cn'], " parsed")


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'http://catalog.expocentr.ru/table.php?wyst_id=123&info_id=0'
    all_links = get_all_links(get_html(url))

    with Pool(40) as pool:
        pool.map(make_all, all_links)


    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()


