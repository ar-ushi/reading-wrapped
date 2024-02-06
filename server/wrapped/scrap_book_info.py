#common scrapper to get important info 
from bs4 import BeautifulSoup, SoupStrainer
import re
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


books_info = []
year = ''
store_book_details = {'totalbooksread': 0, 'totalpagesread': 0 , 'username': ''}
soup = ''

def load_read_books_page(id, new_year):
    global year
    year = new_year
    driver = webdriver.Chrome()
    url = f'https://www.goodreads.com/review/list/{id}?shelf=read&utf8=%E2%9C%93&per_page=infinite&read_at={year}&view=table'        
    driver.get(url)
    try:
        # Set a maximum number of scrolls to avoid an infinite loop
        while not areAllBooksLoaded(driver):
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load after scrolling
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'infiniteStatus')))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    parsed_html = BeautifulSoup(driver.page_source, 'html.parser')
    global soup
    soup = parsed_html
    driver.quit()
    return parsed_html

def areAllBooksLoaded(driver):
        infinite_status_element = driver.find_element(By.ID, 'infiniteStatus')
        # Extract numbers from the text and check if they are equal
        numbers = [int(s) for s in infinite_status_element.text.split() if s.isdigit()]
        return numbers[0] == numbers[1]
    
#generic function to process_read_books
async def process_read_books(capture_genres = False):
    global books_info
    books_info = []
    date_read_rows = []
    for element in soup.select(f'.date_read_value:-soup-contains("{year}")'):
        date_read_rows.append(element.find_parent('tr'))
    #parsing over year()
    tasks = []
    for i, book_rows in enumerate(date_read_rows):
        # self.rows = book_rows
        tasks.append(fetch_book_details(book_rows, i, capture_genres))
    await asyncio.gather(*tasks)
    return books_info

def fetch_overall_stats():
    username= (soup.find("title").text.split(chr(8217)))[0]
    global store_book_details    
    store_book_details['username'] = username
    store_book_details['totalbooksread'] += len(books_info)
    totalpagesread =sum(book['page'] for book in books_info)
    store_book_details['totalpagesread'] = totalpagesread
    return store_book_details
 
 
async def fetch_book_details(book, i, capture_genres):
    obj_name = str(i)
    title=format_element(book, 'title', 'a')
    author= format_element(book,'author','a')
    readcount = format_element(book,'read_count')
    page = int(re.findall(r'\d+', format_element(book,'num_pages'))[0])
    rating= map_rating(book)
    month = re.sub("[^a-zA-Z]", "", format_element(book, 'date_read', 'span'))
    avgrating = float(format_element(book,'avg_rating'))
    booklink = 'https://www.goodreads.com' + book.find_next('td', class_=f'field cover').find('a')['href']
    bookcover_comp = book.find_next('td', class_=f'field cover').find('img')['src']
    bookcover = re.sub(r'\.(?:_SY|_SX)\d+_', '', bookcover_comp)
    genre = (await get_genres(booklink)) if capture_genres else None
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
    'readcount' : readcount,
    'month' : month
    }
    global books_info
    books_info.append(obj_name)

async def get_genres(booklink):
    forbidden_genres = ['Fiction', 'Short Stories', 'Anthology', 'Adult', 'Young Adult']
    res = await parse_book_info_html(booklink)
    if (res.status_code == 200):
        intended_class = 'BookPageMetadataSection__genres'
        parse_only= SoupStrainer(class_= intended_class)
        soup = BeautifulSoup(res.content, 'html.parser', parse_only=parse_only)
        genres = [span.text.strip() for span in soup.find_all('span', class_='Button__labelItem')]
        for genre in genres:
            if genre not in forbidden_genres:
                return genre
            
async def parse_book_info_html(url):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url)
    return await future

def map_rating(book):
    rating_map= {
        'it was amazing' : 5,
        'really liked it': 4,
        'liked it' : 3,
        'it was ok': 2,
        'did not like it': 1
    }
    str_rating = format_element(book,'rating')
    return rating_map[str_rating]

def format_element(book,class_name, tag='div'):
    return book.find_next('td', class_=f'field {class_name}').find(tag).text.strip()