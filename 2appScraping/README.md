Fonctionnement des fichiers et du code contenu à l'intérieur :

A. Scraping1Livre correspond au code nécessaire pour scraper un seul livre, en utilisant la fonction book_scraper qui prend en paramètre l'url de la page du livre

B. Scraping2Categorie correspond au code nécessaire pour scraper toute une catégorie, en utilisant book_scraper à l'intérieur de la fonction category_scraper,
qui prend en paramètre l'url de la page de la catégorie souhaitée. Un fichier .csv du nom de la catégorie sera crée avec les informations des livres qui y sont contenus.

C. Scraping3SiteBooks correspond au code nécessaire pour scraper tout le site de book.toscrape, en utilisant les fonctions book_scraper et category_scraper à l'intérieur
de la fonction book_site_scraper.
Par défaut, tous les fichiers .csv seront enregistrés dans un dossier Csv_and_Images. Il prend en paramètre l'url de la page d'acceuil du site.

D. Scraping4DownloadImg correspond au code nécessaire pour scraper les informations du site de books.toscrape ET enregistrer toutes les images des livres
du site dans le même dossier Csv_and_Images. La même fonction book_site_scraper est utilisée, avec un argument supplémentaire, download_img = False, qu'il faut régler
sur True. Régler ce paramètre sur True permet que toutes les images des livres soient téléchargées en même temps que les autres informations sont scrappées, sinon aucune
image ne sera scrappée et il n'y aura que les fichiers .csv qui seront crée dans le dossier Csv_and_Images.

Il est possible d'ouvrir uniquement le fichier Scraping4DownloadImg  pour pouvoir voir toutes les fonctions crées, book_scraper, category_scraper et
book_site_scraper.

Instructions temporaires pour faire fonctionner l'algorithme :

- Installer Python

- utiliser la commande dans un éditeur de commande à l'endroit où on veut installer l'application :
----------------------
python -m venv myapp
----------------------
où myapp est le nom que vous voulez donner à votre environnement virtuel.

- Télécharger à partir de github les fichiers requirements.txt, README.md, Scraping1Livre, Scraping2Categorie, Scraping3SiteBooks, Scraping4DownloadImg dans le dossier
de votre environnement virtuel.

- Utiliser la commande dans un éditeur de commande
 ---------------------
 pip install -r /path/to/requirements.txt 
 ---------------------
 où /path/to/requirements.txt est le chemin d'accès vers votre fichiers requirements.txt
 
 - Exécuter le fichier correspondant selon le sougait de scraper les informations d'un livre, d'une catégorie de livres, du site entier books.toscrape, ou les images de
 tous les livres contenues sur le site.
