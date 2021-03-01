import requests 
from bs4 import BeautifulSoup


webpage = requests.get('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')

print(webpage.text)
