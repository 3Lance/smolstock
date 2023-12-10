import requests
from bs4 import BeautifulSoup
import base64

def web_scrap_news():

    url = 'https://cryptopotato.com/crypto-news/'
    requestcontent = requests.get(url)
    htmlcontent = requestcontent.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')

    newslist = []

    for u_list in soup.find_all('li' ,class_='rpwe-li'):
        for list_element in u_list.contents:
            for tag in list_element:
                try:
                    # get src
                    src = tag.get('src')
                    # get src in decrypyted base64
                    svg_src = base64.b64decode(src.split('base64,')[1])
                    # get image src from decrypted base64 src
                    html_src = str(svg_src).split('data-u="')[1].split('" data-w')[0]
                    # html decrpytion
                    html_src = html_src.replace('%3A',':')
                    html_src = html_src.replace('%2F','/')
                    # html_src has decrypted image src
                    image_url = html_src
                except:
                    try:
                        news_link = tag.get('href')
                        news_headline = tag.string
                    except:
                        pass
        newslist.append([news_headline, news_link, image_url])

    return newslist


def web_scrap_coins():

    url = 'https://www.binance.com/en/markets'
    requestcontent = requests.get(url)
    htmlcontent = requestcontent.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')

    coinslist = []

    for soup in soup.find_all('div', class_='css-leyy1t'):

        # COIN ABBREVIATION
        name_a = soup.find('a', class_='css-t4pmgu')
        name_d = name_a.find('div', class_='css-y492if')
        name = name_d.find('div', class_='css-1x8dg53')
        name = name.text

        # COIN PRICE
        price_d = soup.find('div', class_='css-ydcgk2')
        price_d = price_d.find('div', class_='css-ovtrou')
        price = price_d.string
        price = float(price.replace(',', '')[1:])

        # PRICE CHANGE PCT
        pct_d = soup.find('div', class_='css-18yakpx')
        pct = pct_d.find('div', class_='css-1vgqjs4')
        try:
            change_pct = float(pct.text[1:-1])
        except:
            change_pct = 0.0

        coinslist.append([name, price, change_pct])

    return coinslist