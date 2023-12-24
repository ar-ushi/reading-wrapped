from bs4 import BeautifulSoup
import requests
import re
import sys

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'totalbooksread': 0, 'totalpagesread': 0, 'avgbooklength': 0, 'longestbook': '', 'longestpg': 0, 'shortestbook': '', 'shortestpg':0 }
        self.rows = []

    def get_parsed_html(self):
        url = f'https://www.goodreads.com/review/list/{self.id}?shelf=read&utf8=%E2%9C%93&per_page=infinite&sort=date_read&view=table'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.fetch_book_details(response)
        return self.store_book_details

    def fetch_book_details(self, res):
        soup = BeautifulSoup(res.content, 'html.parser')
        date_read_rows = []
        for element in soup.select(f'.date_read_value:-soup-contains("{self.year}")'):
            month = re.sub("[^a-zA-Z]", "", element.text.strip())
            self.update_count('month', month)
            date_read_rows.append(element.find_parent('tr'))
        #parsing over year()
        self.store_book_details['totalbooksread'] += len(date_read_rows)
        for book_rows in date_read_rows:
            self.rows = book_rows
            title=self.format_element('title')
            author= self.format_element('author')
            page = self.format_element('num_pages', tag='div')
            rating = self.format_element('rating', tag='div')

            page = int(re.findall(r'\d+', page)[0])

            self.store_book_details.setdefault('title', []).append(title)
            self.update_count('author', author)
            self.store_book_details.setdefault('numpage', []).append(page)
            self.update_count('rating', rating)
            self.store_book_details['totalpagesread'] += int(page)
        self.find_book()
        self.store_book_details['avgbooklength'] = int(self.store_book_details['totalpagesread']/self.store_book_details['totalbooksread'])
        print(self.store_book_details)

    def find_book(self):
        shortest = sys.maxsize
        longest = 0
        shortestindex = 0
        longestindex = 0
        for i, value in enumerate(self.store_book_details['numpage']):
            if value < shortest:
                shortest = value
                shortestindex = i
            elif value > longest:
                longest = value
                longestindex = i
        self.store_book_details['longestpg'] = longest
        self.store_book_details['shortestpg'] = shortest
        self.store_book_details['longestbook'] = self.store_book_details['title'][longestindex]
        self.store_book_details['shortestbook'] = self.store_book_details['title'][shortestindex]

    def update_count(self, key,value):
        self.store_book_details.setdefault((key), {})
        self.store_book_details[key][value] = self.store_book_details[key].get(value, 0) + 1
    
    def format_element(self,class_name, tag='a'):
        return self.rows.find_next('td', class_=f'field {class_name}').find(tag).text.strip()