import requests 
from bs4 import BeautifulSoup
import re
import csv


def book_scraper(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    #titre du livre
    book_title = soup.select("div h1")
    book_title = book_title[0].string
    #page web du livre
    product_page_url = url
    #scraping de la table des prix
    table_scraping = soup.select("td")
    #code_upc
    universal_product_code = table_scraping[0].string
    #les prix
    price_excluding_tax = table_scraping[2].string
    print(str(price_excluding_tax))
    price_including_tax = table_scraping[3].string
    #le nombre d'exemplaires disponibles
    number_available = table_scraping[5].string
    number_available = re.findall('\d+', number_available)[0]
    #scraping de la description du livre
    paragraph_scraper = soup.select("p")
    paragraph_printer = []
    for p in paragraph_scraper:
        paragraph_printer.append(p.string)
    product_description = paragraph_printer[3]
    #la catégorie
    category = soup.select("ul li a")
    a_list = []
    for a in category:
        a_list.append(a.string)
    category = a_list[2]
    # la note du livre
    review_rating = soup.select("div p")
    '''"def has_a_rating(tag):
        return tag.attr('class') == "star-rating Four"'''
    review_printer = []
    dictionnary_printer = []
    list_printer = []
    for text in review_rating:
        review_printer.append(text.attrs)
    for dictionnary in review_printer:
        dictionnary_printer.append(list(dictionnary.values()))
    for element in dictionnary_printer:
        for kelement in element:
            list_printer.append(kelement)
    review_rating = list_printer[2][1]
    # l'url de l'image
    url_img = soup.find("img")
    url_img = url_img["src"] 
    image_url = "http://books.toscrape.com/" + re.sub('^\W{6}', '', url_img)
    
    with open('book.csv', 'w') as out:
        csv_writing = csv.writer(out, delimiter = ';', quoting = csv.QUOTE_MINIMAL)
        list_of_entete = ['product_page_url', 'universal_product_code(upc)',' title', 'price_including_tax', 'price_excluding_tax', \
'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        list_of_rowvalues = [product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, \
number_available, product_description, category, review_rating, image_url]
        """csv_writing.writerow(list_of_entete)
        csv_writing.writerow(product_page_url + ';' + universal_product_code + ';' + book_title + ';' + price_including_tax + ';' + \
        price_excluding_tax + ';' + number_available + ';' + product_description + ';' + category + ';' + review_rating + ';' + \
        image_url)"""
        csv_writing.writerow(list_of_entete)
        csv_writing.writerow(list_of_rowvalues)

    

def category_scraper(category_url):
    category_webpage = requests.get(category_url)
    soup_category = BeautifulSoup(category_webpage.content, "html.parser")

    next_page_button = soup_category.find(attrs={'class':'next'})
    
    # met la premiere page parsée par BeautifulSoup dans une liste
    soups = [soup_category]

    #tant qu'il y a un bouton next en bas de la page, on rajoute un nouvel élément soup dans la liste et on passe à la prochaine page
    while next_page_button:
        for text in next_page_button:
            # va trouver l'url de la prochaine page si il y en a une
            category_url = re.sub('[indexpage-]*\d*\.html$', '', category_url)
            next_page_button_url = category_url + text.attrs['href']   
        new_category_webpage = requests.get(next_page_button_url)
        new_soup = BeautifulSoup(new_category_webpage.content, "html.parser")
        soups.append(new_soup) 
        next_page_button = new_soup.find(attrs={'class':'next'})
    
    links = []
    
    #Scrapage de tous les liens présents sur la page
    for soup_parsing in soups:
        lis = soup_parsing.select("li h3 a")
        for a in lis:
            links.append(a.attrs["href"])

    #Chaque lien se voit attribuer le bon début pour accéder à une page au lieu de ../..
    for index in range(len(links)):
        links[index] = "http://books.toscrape.com/catalogue/" + re.sub('^\W{9}', '', links[index])
    
    print(links)

            
category_scraper("http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html")       
    

    
    

'book_scraper("http://books.toscrape.com/catalogue/sharp-objects_997/index.html")'
"""
books_titles = soup.select("li h3 a")

paragraph_printer = []
for text in books_titles:
    paragraph_printer.append(text.attrs["title"])

for i in paragraph_printer:
    print(i)

books_prices = soup.find_all(attrs={'class':'price_color'})

for price in books_prices:
    print(price.string)"""

