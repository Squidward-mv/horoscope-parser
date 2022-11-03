from aiohttp import ClientSession
from bs4 import BeautifulSoup
from config import *

async def get_horoscope(sign, period='сегодня'):    
    ###Set the default period if users input incorrect
    if period not in zodiac_sign_route:
        period = 'сегодня'
    async with ClientSession() as session:
        async with session.get(zodiac_sign_urls[sign] + zodiac_sign_route[period], headers=HEADERS) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            items = soup.findAll('div', class_='article__item article__item_alignment_left article__item_html')
            comps = []

            for item in items:
                comps.append({
                'data': item.findAll('p')
                })

            string = comps[0]['data'][0].get_text(strip=True) + "\n" + comps[0]['data'][1].get_text(strip=True)
            result = f"🌟 Гороскоп на {period}: {sign} {zodiac_signs[sign]} \n\n🟠 {string}"

            return result
