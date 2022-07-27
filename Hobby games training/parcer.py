import requests
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()
header_random = ua.random
headers = {'User-Agent': header_random} #замена заголовка, чтобы сайт не понял, что это бот

def get_url():
    for count in range(1, 2):

        url = f'https://hobbygames.ru/nastolnie?page={count}&parameter_type=0'

        response = requests.get(url, headers=headers) #для получения ответа от сайта

        soup = BeautifulSoup(response.text, 'lxml') #lxml анализирует html код, для его передачи в нормальном виде
        #в beaitifulsoup, чтобы по нему можно было находить необходимые элементы

        data = soup.find_all('div', class_ = 'col-lg-4 col-md-6 col-sm-6 col-xs-12')

        for i in data: #цикл, чтобы пройти по всем товарам на одной странице
            url_game = i.find(class_='name').get('href')  # ссылка на товар
            yield url_game #создание генератора-функции, чтобы оптимизировать код. и не нагружать списком


def array():
    for card_url in get_url():

        response = requests.get(card_url, headers=headers)
        sleep(1)
        soup = BeautifulSoup(response.text, 'lxml')

        data = soup.find('div', class_ = 'desc-text').text.strip()
        name = soup.find(class_='col-lg-8').text.strip()
        price = soup.find(class_='price').text
        url_img = soup.find('a', class_ = 'lightGallery').get('href')

        yield name, price, data, url_img

