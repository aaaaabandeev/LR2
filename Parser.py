from bs4 import BeautifulSoup # импортируем библиотеку BeautifulSoup
import requests # импортируем библиотеку requests

msg1 = None #переменная для вывода сообщения с парсом, глобальная для легкого импорта
poisk = '' #переменная с содержанием запроса
def parse():
    global poisk #чтобы использовать переменную внутри
    global msg1
    msg1 = '' #обнуляем переменную вывода сообщения, чтобы не накапливался мусор

    #АПТЕЧНЫЙ САЙТ:
    url = 'https://farmakopeika.ru/search?query=' + poisk + '&limit=48'  # передаем необходимый URL адрес
    page = requests.get(url)  # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    #print(page.status_code)  # смотрим ответ
    soup = BeautifulSoup(page.text, "html.parser")  # передаем страницу в bs4

    block = soup.findAll(class_='product__body')  # находим  контейнер с нужным классом
    description1 = []  # Информация о результатах поиска
    for data in block:  # проходим циклом по содержимому контейнера
            a = data.text.replace("\n", "")
            a = a.replace("от", ", от")
            a = a.replace("В корзину", "")  # Косметический ремонт
            a = a.replace("На складе:", ", на складе: ")
            a = a.replace("В аптеках:", ", в аптеках: ")
            description1.append(a)



    for data in description1:  # ВЫВОД ЛИСТА В КОНСОЛЬ
       msg1 += (data)
       msg1 += ('\n')
