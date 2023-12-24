from bs4 import BeautifulSoup
import requests

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'title': [], 'author': [], 'numpage': []}
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
        date_read_rows = [element.find_parent('tr') for element in soup.select(f'.date_read_value:-soup-contains("{self.year}")')]
        #parsing over year
        for book_rows in date_read_rows:
            self.rows = book_rows
            title=self.format_element('title')
            author= self.format_element('author')
            page = self.format_element('num_pages', div)

            self.store_book_details['title'].append(title)
            self.store_book_details['author'].append(author)
            self.store_book_details['numpage'].append(page)
        print(self.store_book_details)

    def format_element(self,class_name, tag='a'):
        return self.rows.find_next('td', class_=f'field {class_name}').find(tag).text.strip()