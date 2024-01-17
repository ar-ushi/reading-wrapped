from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'totalbooksread': 0, 'totalpagesread': 0 , 'username': '', 'books': []}
        self.rows = []

    async def get_parsed_html(self):
        driver = webdriver.Chrome()
        url = f'https://www.goodreads.com/review/list/{self.id}?shelf=read&utf8=%E2%9C%93&per_page=infinite&read_at={self.year}&view=table'        
        driver.get(url)
        try:
            # Set a maximum number of scrolls to avoid an infinite loop
            while not self.areAllBooksLoaded(driver):
                # Scroll to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
            # Wait for the page to load after scrolling
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'infiniteStatus')))
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        await self.process_read_books(soup)
        return self.store_book_details

    def areAllBooksLoaded(self,driver):
        infinite_status_element = driver.find_element(By.ID, 'infiniteStatus')
        # Extract numbers from the text and check if they are equal
        numbers = [int(s) for s in infinite_status_element.text.split() if s.isdigit()]
        return numbers[0] == numbers[1]
    
    async def process_read_books(self, soup):
        username= (soup.find("title").text.split(chr(8217)))[0]
        self.store_book_details['username'] = username
        date_read_rows = []
        for element in soup.select(f'.date_read_value:-soup-contains("{self.year}")'):
            month = re.sub("[^a-zA-Z]", "", element.text.strip())
            self.update_count('month', month)
            date_read_rows.append(element.find_parent('tr'))
        #parsing over year()
        self.store_book_details['totalbooksread'] += len(date_read_rows)
        tasks = []
        for i, book_rows in enumerate(date_read_rows):
            self.rows = book_rows
            tasks.append(self.fetch_book_details(book_rows, i))
        await asyncio.gather(*tasks)
    
    async def fetch_book_details(self, book_rows, i):
        obj_name = str(i)
        title=self.format_element('title', tag='a')
        author= self.format_element('author',tag='a')
        readcount = self.format_element('read_count')
        page = int(re.findall(r'\d+', self.format_element('num_pages'))[0])
        rating= self.map_rating()            
        avgrating = float(self.format_element('avg_rating'))
        booklink = 'https://www.goodreads.com' + book_rows.find_next('td', class_=f'field cover').find('a')['href']
        bookcover_comp = book_rows.find_next('td', class_=f'field cover').find('img')['src']
        bookcover = re.sub(r'\.(?:_SY|_SX)\d+_', '', bookcover_comp)
        genre = await self.get_genres(booklink)
        #create book object

        obj_name = {
        'title': title,
        'author': author,
        'page': page,
        'rating': rating,
        'avgrating': avgrating,
        'booklink': booklink,
        'bookcover': bookcover,
        'genre' : genre,
        'readcount' : readcount
        }
        self.store_book_details['books'].append(obj_name)
        self.store_book_details['totalpagesread'] += int(page)

    async def get_genres(self, booklink):
        forbidden_genres = ['Fiction', 'Nonfiction', 'Short Stories', 'Anthology', 'Adult']
        res = await self.parse_book_info_html(booklink)
        if (res.status_code == 200):
            intended_class = 'BookPageMetadataSection__genres'
            parse_only= SoupStrainer(class_= intended_class)
            soup = BeautifulSoup(res.content, 'html.parser', parse_only=parse_only)
            genres = [span.text.strip() for span in soup.find_all('span', class_='Button__labelItem')]
            for genre in genres:
                if genre not in forbidden_genres:
                    return genre
                
    async def parse_book_info_html(self, url):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, requests.get, url)
        return await future
    
    def update_count(self, key,value, inc = 1):
        self.store_book_details.setdefault((key), {})
        self.store_book_details[key][value] = self.store_book_details[key].get(value, 0) + inc
    
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
    
    def format_element(self,class_name, tag='div'):
        return self.rows.find_next('td', class_=f'field {class_name}').find(tag).text.strip()