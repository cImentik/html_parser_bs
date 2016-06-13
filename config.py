# -*- coding: utf-8 -*-

"""
Файл конфигурации скрипта. Для настройки фильтров контента.
Один набор фильтров для одного сайта
"""

# lenta.ru
# url = "https://lenta.ru/news/2016/05/08/canadabridge/"
H_TAG = "h1" # тег заголовка контента
H_ATR = {} # атрибуты заголовка контента
C_TAG = "div" # тег в котором ищем контент
C_ATR = {'class' : 'b-topic__content'} # атрибуты тега в котором ищем контент
T_TAG = ['p'] # теги в которых ищем текст (может быть много)


# gazeta.ru
# url = "http://www.gazeta.ru/army/news/8611511.shtml"
# H_TAG = "h1"
# H_ATR = {'class': 'news-body__title'}
# C_TAG = "div"
# C_ATR = {'class' : 'news-body__text'}
# T_TAG = ['p']


# H_TAG = 'h1'
# H_ATR = {}
# C_TAG = 'div'
# C_ATR = {'class':'b-material-text'}
# T_TAG = ['p']


# headers запроса серверу, в данном случае поле User-Agent. 
headers = {'User-Agent': 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

MAX_TEXT = 80 # Максимальное количество символов в строке
