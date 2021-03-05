import requests 
from bs4 import BeautifulSoup
import re
import csv
import os
import time


def book_scraper(url, category_name=0):
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
    
    if category_name == 0:
        with open('book.csv', 'w', encoding='utf-8') as out:
            csv_writing = csv.writer(out, delimiter = ';', quoting = csv.QUOTE_MINIMAL)
            list_of_entete = ['product_page_url', 'universal_product_code(upc)',' title', 'price_including_tax', 'price_excluding_tax', \
    'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            list_of_rowvalues = [product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, \
    number_available, product_description, category, review_rating, image_url]
            csv_writing.writerow(list_of_entete)
            csv_writing.writerow(list_of_rowvalues)
            print("category_name est égal à 0")

    else:
        list_of_rowvalues = [product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, \
    number_available, product_description, category, review_rating, image_url]
        return list_of_rowvalues

            
        

    

def category_scraper(category_url, dir_path=''):
    category_webpage = requests.get(category_url)
    soup_category = BeautifulSoup(category_webpage.content, "html.parser")

    next_page_button = soup_category.find(attrs={'class':'next'})
    
    # met la premiere page parsée par BeautifulSoup dans une liste
    soups = [soup_category]

    #tant qu'il y a un bouton next en bas de la page, on rajoute un nouvel élément soup dans la liste et on passe à la prochaine page
    if not next_page_button:
        category_url = re.sub('[indexpage-]*\d*\.html$', '', category_url)
    else:
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
    
    # on trouve le nom de la categorie pour pouvoir nommer le fichier csv
    category_name = re.sub('.+category\/books\/', '', category_url)
    print('CATEGORY_NAME :' + category_name)
    if category_name[-1] == '/':
        category_name = category_name[0:-1]
    else:
        category_name = category_name



    with open('{}.csv'.format(dir_path + category_name), 'w', encoding='utf-8') as out:
        csv_writing = csv.writer(out, delimiter = ';', quoting = csv.QUOTE_ALL)
        list_of_entete = ['product_page_url', 'universal_product_code(upc)',' title', 'price_including_tax', 'price_excluding_tax', \
'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        csv_writing.writerow(list_of_entete)
        for book in links:
            new_row = book_scraper(book, category_name)
            csv_writing.writerow(new_row)
        
    
    
def book_site_scraper(book_site_url):
    book_site_webpage = requests.get(book_site_url)
    book_site_soup = BeautifulSoup(book_site_webpage.content, "html.parser")

    # on récupère les liens vers les catégories dans le panneau à gauche du site
    categories = book_site_soup.select("aside div ul li a")
    category_links = []
    for text in categories:
        category_links.append(text.attrs['href'])
    # list slicing pour éviter de récupérer le 1er lien qui va vers la page d'acceuil
    category_links = category_links[1:]
    category_links = ["http://books.toscrape.com/" + link for link in category_links]

    
    # si il n'existe pas un dossier pour y mettre les csv, on en crée un
    dir_path = '../Csv_and_Images'
    try:
        os.mkdir(dir_path)
    except OSError:
        print ("la création du dossier %s pour mettre les fichiers csv et les images scrapées a échouée" % dir_path)
    else:
        print ("la création du dossier %s pour mettre les fichiers csv et les images scrapées a bien réussie" % dir_path)

    dir_path = dir_path + "/"

    for link in category_links:
        category_scraper(link, dir_path)
        print(link + ' ... Scraped!')
        time.sleep(1)

    

    
# exemple d'appel de la fonction book_site_scraper pour faire un scraping de toutes les cat. de books2scrape
# cet appel va mettre toutes les données dans un fichier csv différent par catégorie et ces fichiers csv 
# dans un dossier Csv_and_Images
book_site_scraper("http://books.toscrape.com/index.html")

# exemple d'appel de la fonction category_scraper pour uniquement scraper une catégorie,
# crée un fichier csv du nom de la cat.
'category_scraper("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")'