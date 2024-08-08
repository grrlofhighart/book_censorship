import argparse
from datetime import datetime
import json
import os
import re
import time

from urllib.request import Request, urlopen
from urllib.error import HTTPError
import bs4
import pandas as pd


def get_all_lists(book_id):

    lists = []
    list_count_dict = {}

    lists_url = 'https://www.goodreads.com/list/book/'

    list_source = urlopen(lists_url + book_id)
    soup = bs4.BeautifulSoup(list_source, 'lxml')
    lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

    i = 0
    while soup.find('a', {'class': 'next_page'}) and i <= 10:

        time.sleep(2)
        next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
        source = urlopen(next_url)
        soup = bs4.BeautifulSoup(source, 'lxml')

        lists += [node.text for node in soup.find_all('div', {'class': 'cell'})]
        i += 1

    # Format lists text.
    for _list in lists:
        _list_name = ' '.join(_list.split()[:-8])
        _list_rank = int(_list.split()[-8][:-2]) 
        _num_books_on_list = int(_list.split()[-5].replace(',', ''))
        list_count_dict[_list_name] = [_list_rank, _num_books_on_list]
    
    return list_count_dict


def check_element(e):
    if e:
        return (e)
    else:
        return ('')


def get_reviews(soup):
    review_base = 'https://www.goodreads.com'  
    try:
        review_suffix = check_element(soup.find("a", {"class": "Button Button--transparent Button--medium"})['href'])
        if review_suffix:
            review_url = review_base + review_suffix
            return review_url
        else:
            review_url = 'None'
            return review_url
    except:
        review_url = 'None'
    
    return review_url

def get_shelves(soup):

    shelf_count_dict = {}
    legacyID = re.findall(r'\"Work\"\,\"legacyId\"\:[0-9]+', str(soup))[0]
    suffix = re.sub('[^0-9]', '', legacyID)

    if suffix:

        # Find shelves text.
        shelves_url = 'https://www.goodreads.com/work/shelves/'
        source = urlopen(shelves_url + suffix)
        soup = bs4.BeautifulSoup(source, 'lxml')
        shelves = [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'shelfStat'})]
        
        # Format shelves text.
        shelf_count_dict = {}
        for _shelf in shelves:
            _shelf_name = _shelf.split()[:-2][0]
            _shelf_count = int(_shelf.split()[-2].replace(',', ''))
            shelf_count_dict[_shelf_name] = _shelf_count

    return shelf_count_dict


def get_genres(soup):
    genres = []
    for node in soup.find_all('span', {'class': 'BookPageMetadataSection__genreButton'}):
        current_genres = node.find_all('a', {'class': 'Button Button--tag-inline Button--medium'})
        current_genre = ' > '.join([g.text for g in current_genres])
        if current_genre.strip():
            genres.append(current_genre)
    return genres


def get_series_name(soup):
    series_block = re.findall(r'(?<=Series\"\,\"title\"\:\")([a-zA-Z\s]*)(?=\"\,\"webUrl\"\:\"https\:)', str(soup))
    if series_block:
        series_name = series_block[0]
        return series_name
    else:
        return ""


def get_series_uri(soup):
    series_url = 'https://www.goodreads.com/series/'
    series = re.findall(r'https\:\/\/www\.goodreads\.com\/series\/([^\n">]*)', str(soup))
    if series:
        series_uri = series_url + series[0]
        return series_uri
    else:
        return ""

def get_top_5_other_editions(soup):
    other_editions = []
    editions_url = 'https://www.goodreads.com/work/editions/'
    try:
        legacyID = re.findall(r'\"Work\"\,\"legacyId\"\:[0-9]+', str(soup))[0]
        suffix = re.sub('[^0-9]', '', legacyID)
        other_editions = editions_url + suffix
        return other_editions
    except:
        return "other editions not found"

def get_isbn(soup):
    try:
        isbn = re.findall(r'(?<=isbn\"\:\")\d{10}' , str(soup))[0]
        return isbn
    except:
        return "isbn not found"

def get_isbn13(soup):
    try:
        isbn13 = re.findall(r'(?<=isbn13\"\:\")\d{13}' , str(soup))[0]
        return isbn13
    except:
        return "isbn13 not found"


def get_rating_distribution(soup):
    distribution = re.findall(r'ratingsCountDist\"\:[\s]*\[[0-9,\s]+', str(soup))[0]
    distribution = ' '.join(distribution.split())
    distribution = [int(c.strip()) for c in distribution.split('[')[1].split(',')]
    distribution_dict = {'5 Stars': distribution[0],
                         '4 Stars': distribution[1],
                         '3 Stars': distribution[2],
                         '2 Stars': distribution[3],
                         '1 Star':  distribution[4]}
    return distribution_dict


def get_num_pages(soup):
    pages = soup.find('div', attrs={'class':'FeaturedDetails'}).text
    if pages:
        num_pages = re.search(r'[0-9]+(?=\spages)', pages).group(0)
    return int(num_pages)


def get_year_first_published(soup):
    year_first_published = soup.find('div', attrs={'class':'FeaturedDetails'})
    if year_first_published:
        year_first_published = year_first_published.text
        return re.search(r'((January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}\,\s\d{4})', year_first_published).group(1)
    else:
        return ''

def get_id(bookid):
    pattern = re.compile("([^.-]+)")
    return pattern.search(bookid).group()

def get_cover_image_uri(soup):
    series = soup.find('div', {'class' : 'BookCover__image'})
    if series:
        series_uri = series.find('img').get('src')
        return series_uri
    else:
        return ""
    
def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }
    
    request = Request(url, headers=header)
    
    source = urlopen(request)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    time.sleep(2)

    return {'book_id_title':        book_id,
            'book_id':              get_id(book_id),
            'cover_image_uri':      get_cover_image_uri(soup),
            'book_title':           ' '.join(soup.find('h1', {'data-testid': 'bookTitle'}).text.split()),
            'book_series':          get_series_name(soup),
            'book_series_uri':      get_series_uri(soup),
            'top_5_other_editions': get_top_5_other_editions(soup),
            'isbn':                 get_isbn(soup),
            'isbn13':               get_isbn13(soup),
            'year_first_published': get_year_first_published(soup),
            'authorlink':           soup.find('a', {'class': 'ContributorLink'})['href'],
            'author':               ' '.join(soup.find('span', {'class': 'ContributorLink__name'}).text.split()),
            'num_pages':            get_num_pages(soup),
            'genres':               get_genres(soup),
            'shelves':              get_shelves(soup),
            'lists':                get_all_lists(book_id),
            'num_ratings':          soup.find('span', {'data-testid': 'ratingsCount'}).text.strip('\xa0ratings'),
            'num_reviews':          soup.find('span', {'data-testid': 'reviewsCount'}).text.strip('\xa0reviews'),
            'average_rating':       soup.find('div', {'class': 'RatingStatistics__rating'}).text.strip(),
            'rating_distribution':  get_rating_distribution(soup),
            'reviews_page':         'https://www.goodreads.com/book/show/'+ book_id + '/reviews'}

def condense_books(books_directory_path):

    books = []
    
    # Locate all files containing "book-metadata," and combine into a single file
    for file_name in os.listdir(books_directory_path):
        if file_name.endswith('.json') and not file_name.startswith('.') and file_name != "all_books.json" and "book-metadata" in file_name:
            _book = json.load(open(books_directory_path + '/' + file_name, 'r')) #, encoding='utf-8', errors='ignore'))
            books.append(_book)

    return books

def main():

    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    parser.add_argument('--format', type=str, action="store", default="json",
                        dest="format", choices=["json", "csv"],
                        help="set file output format")
    args = parser.parse_args()

    book_ids              = [line.strip() for line in open(args.book_ids_path, 'r') if line.strip()]
    books_already_scraped =  [file_name.replace('_book-metadata.json', '') for file_name in os.listdir(args.output_directory_path) if file_name.endswith('.json') and not file_name.startswith('all_books')]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]
    condensed_books_path   = args.output_directory_path + '/all_books'

    for i, book_id in enumerate(books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(i+1+len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            book = scrape_book(book_id)
            # Add book metadata to file name to be more specific
            json.dump(book, open(args.output_directory_path + '/' + book_id + '_book-metadata.json', 'w'))

            print('=============================')

        except HTTPError as e:
            print(e)
            exit(0)


    books = condense_books(args.output_directory_path)
    if args.format == 'json':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
    elif args.format == 'csv':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
        book_df = pd.read_json(f"{condensed_books_path}.json")
        book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding='utf-8')
        
    print(str(datetime.now()) + ' ' + script_name + f':\n\n🙌 Success! All book data scraped. 🙌\n\nData files output to /{args.output_directory_path}\nTotal scraping run time = ⏳ ' + str(datetime.now() - start_time) + ' ⌛')



if __name__ == '__main__':
    main()