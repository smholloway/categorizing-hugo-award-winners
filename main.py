from bs4 import BeautifulSoup
import urlparse
import re
import requests

def main():
    url = "http://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novel#Winners_and_nominees"
    soup = soup_from_url(url)
    winners_and_nominees = soup.find_all('table', class_='wikitable')[0].find_all('tr')[1:]
    print_all(winners_and_nominees)

def print_all(winners_and_nominees):
    for book in winners_and_nominees:
        year   = get_year(book)
        author = get_author_name(book)
        title  = get_book_title(book)
        genre  = get_genre(book)
        print "{0} by {1} ({2}) | {3}".format(title, author, year, genre)

def print_fantasy(winners_and_nominees):
    for book in winners_and_nominees:
        year   = get_year(book)
        author = get_author_name(book)
        title  = get_book_title(book)
        genre  = get_genre(book)
        if re.search("fantasy", genre, re.IGNORECASE):
            print "{0} by {1} ({2})".format(title, author, year)

def soup_from_url(url):
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    return soup

def get_year(book):
    try:
        year = str(book.find_all('td')[0].find_all('a')[0].text)
    except:
        return "none"
    return year

def get_author_name(book):
    try:
        #author = str(book.find_all('td')[1].find_all('span')[0].text.encode('utf8'))
        author = str(book.find_all('td')[1].find_all('a')[0].text.encode('utf8'))
    except:
        return "none"
    return author

def get_book_title(book):
    try:
        title = str(book.find_all('td')[2].find_all('a')[0].text)
    except:
        try:
            title = str(book.find_all('td')[2].find_all('i')[0].text)
        except:
            return "none"
    return title

def get_book_link(book):
    try:
        book_link = str(book.find_all('td')[2].find_all('a')[0].get('href'))
    except:
        return "none"
    return make_link_absolute(book_link, 'http://en.wikipedia.org/')

def make_link_absolute(relative_url, base_url):
    return urlparse.urljoin(base_url, relative_url)

def get_genre(book):
    book_link = get_book_link(book)
    if book_link is "none" or not book_link:
        return "unknown"
    soup = soup_from_url(book_link)
    try:
        genre_th = soup.find_all('th', text='Genre')[0]
        genre = genre_th.parent.td.a.text
    except:
        return "unknown"
    return genre

if __name__ == "__main__":
    main()
