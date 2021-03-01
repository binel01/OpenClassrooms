import requests 
from bs4 import BeautifulSoup


webpage = requests.get('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')
soup = BeautifulSoup(webpage.content, "html.parser")

books_titles = soup.select("li h3 a")

paragraph_printer = []
for text in books_titles:
    paragraph_printer.append(text.attrs["title"])

"""for i in paragraph_printer:
    print(i)"""

books_prices = soup.find_all(attrs={'class':'price_color'})
"""
for price in books_prices:
    print(price.string)"""

