import requests
from bs4 import BeautifulSoup

#bank_id = 1771062 #ID банка на сайте banki.ru

# Ссылка, откуда будем пи@дить HTML
url = 'http://kraz-s-sdsrv.hq.root.ad/SD/SD_Reports/Rep_070?id_res=130933&idNode=149978' #% (bank_id) # url страницы
#отправляем HTTP запрос и получаем результат
r = requests.get(url)

# Запись в файл
#with open('test.html', 'w') as output_file:
#  output_file.write(r.text)

soup = BeautifulSoup(r.text, 'lxml')

print(soup)