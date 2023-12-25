from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import sys

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'totalbooksread': 0, 'totalpagesread': 0  }
        self.rows = []

    def get_parsed_html(self):
        url = f'https://www.goodreads.com/review/list/{self.id}?shelf=read&utf8=%E2%9C%93&per_page=infinite&read_at={self.year}&view=table'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.fetch_book_details(response)
        return self.store_book_details

    def fetch_book_details(self, res):
        soup = BeautifulSoup(res.content, 'html.parser')
        username= (soup.find("title").text.split(chr(8217)))[0]
        self.store_book_details.setdefault('username', '').append(username)
        date_read_rows = []
        for element in soup.select(f'.date_read_value:-soup-contains("{self.year}")'):
            month = re.sub("[^a-zA-Z]", "", element.text.strip())
            self.update_count('month', month)
            date_read_rows.append(element.find_parent('tr'))
        #parsing over year()
        self.store_book_details['totalbooksread'] += len(date_read_rows)
        for i, book_rows in enumerate(date_read_rows):
            self.rows = book_rows
            title=self.format_element('title', tag='a')
            author= self.format_element('author',tag='a')
            page = int(re.findall(r'\d+', self.format_element('num_pages'))[0])
            rating= self.map_rating()
            avgrating = float(self.format_element('avg_rating'))
            booklink = 'https://www.goodreads.com' + book_rows.find_next('td', class_=f'field cover').find('a')['href']
            bookcover = book_rows.find_next('td', class_=f'field cover').find('img')['src']
            #genre = self.get_genres(booklink)

            self.store_book_details[str(i)] = {
            'title': title,
            'author': author,
            'page': page,
            'rating': rating,
            'avgrating': avgrating,
            'booklink': booklink,
            'bookcover': bookcover,
            }
            self.store_book_details['totalpagesread'] += int(page)

    def map_rating(self):
        rating_map= {
            'it was amazing' : 5,
            'really liked it': 4,
            'liked it' : 3,
            'it was ok': 2,
            'did not like it': 1
        }
        str_rating = self.format_element('rating')
        return rating_map[str_rating]

    def get_genres(self, booklink):
        res = requests.get(booklink)
        if (res.status_code == 200):
            intended_class = 'BookPageMetadataSection__genres'
            parse_only= SoupStrainer(class_= intended_class)
            soup = BeautifulSoup(res.content, 'html.parser', parse_only=parse_only)
            return soup.find('span', class_='Button__labelItem').text

    def update_count(self, key,value, inc = 1):
        self.store_book_details.setdefault((key), {})
        self.store_book_details[key][value] = self.store_book_details[key].get(value, 0) + inc
    
    def format_element(self,class_name, tag='div'):
        return self.rows.find_next('td', class_=f'field {class_name}').find(tag).text.strip()