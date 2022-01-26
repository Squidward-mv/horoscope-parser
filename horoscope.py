from bs4 import BeautifulSoup
import requests

zz = {
        "овен": 'https://horo.mail.ru/prediction/aries/today/',
        "телец": 'https://horo.mail.ru/prediction/taurus/today/',
        "близнецы": 'https://horo.mail.ru/prediction/gemini/today/',
        "рак": 'https://horo.mail.ru/prediction/cancer/today/',
        "лев": 'https://horo.mail.ru/prediction/leo/today/',
        "дева": 'https://horo.mail.ru/prediction/virgo/today/',
        "весы": 'https://horo.mail.ru/prediction/libra/today/',
        "скорпион": 'https://horo.mail.ru/prediction/scorpio/today/',
        "стрелец": 'https://horo.mail.ru/prediction/sagittarius/today/',
        "козерог": 'https://horo.mail.ru/prediction/capricorn/today/',
        "водолей": 'https://horo.mail.ru/prediction/aquarius/today/',
        "рыбы": 'https://horo.mail.ru/prediction/pisces/today/'
    }

def parse(msg):
    URL = zz[msg]

    HEADERS = {
        'User_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='article__item article__item_alignment_left article__item_html')
    comps = []

    for item in items:
        comps.append({
            'data': item.findAll('p')

        })

    result = "Гороскоп на сегодня: " + msg + "\n\n" + comps[0]['data'][0].get_text(strip=True) + "\n" + comps[0]['data'][1].get_text(strip=True)

    return result