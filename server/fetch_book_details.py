from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'totalbooksread': 0, 'totalpagesread': 0 , 'username': '', 'books': []}
        self.rows = []

    def login_to_goodreads(self, driver):
        login_url = 'https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=102cb5ef9d6283aecfd2282191b29742'

        # Open the login page
        driver.get(login_url)

        # Find the username and password input fields and submit button
        username_field = driver.find_element(By.ID, 'ap_email')
        password_field = driver.find_element(By.ID, 'ap_password')
        submit_button = driver.find_element(By.ID, 'signInSubmit')

        # Input your username and password
        username_field.send_keys('aggarwalarushi5@gmail.com')
        password_field.send_keys('lifeisme123')

        # Click the submit button
        submit_button.click()

        # Wait for the login to complete (you might need to adjust the waiting time)
        time.sleep(5)

        # Return the driver after login
        return driver

    def get_parsed_html(self):
        driver = webdriver.Chrome()
        self.login_to_goodreads(driver)
        url = f'https://www.goodreads.com/review/list/{self.id}?shelf=read&utf8=%E2%9C%93&per_page=100e&read_at={self.year}&view=table'        
        driver.get(url)

        try:
            # Set a maximum number of scrolls to avoid an infinite loop
            max_scrolls = 10
            current_scroll = 0

            while current_scroll < max_scrolls:
                # Scroll to the bottom of the page
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

                # Wait for a short period to allow content to load
                time.sleep(2)  # Adjust as needed

                # Check if the target element is present
                target_element_present = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'responsiveSiteFooter'))
                )

                if target_element_present:
                    break

                current_scroll += 1
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        self.fetch_book_details(soup)
        return self.store_book_details
    
    def fetch_book_details(self, soup):
        username= (soup.find("title").text.split(chr(8217)))[0]
        self.store_book_details['username'] = username
        date_read_rows = []
        for element in soup.select(f'.date_read_value:-soup-contains("{self.year}")'):
            month = re.sub("[^a-zA-Z]", "", element.text.strip())
            self.update_count('month', month)
            date_read_rows.append(element.find_parent('tr'))
        #parsing over year()
        self.store_book_details['totalbooksread'] += len(date_read_rows)
        for i, book_rows in enumerate(date_read_rows):
            self.rows = book_rows
            obj_name = str(i)
            title=self.format_element('title', tag='a')
            author= self.format_element('author',tag='a')
            page = int(re.findall(r'\d+', self.format_element('num_pages'))[0])
            rating= book_rows.find_next('td', class_=f'field rating').find('div', class_='stars')['data-rating']
            avgrating = float(self.format_element('avg_rating'))
            booklink = 'https://www.goodreads.com' + book_rows.find_next('td', class_=f'field cover').find('a')['href']
            bookcover_comp = book_rows.find_next('td', class_=f'field cover').find('img')['src']
            bookcover = re.sub(r'\.(?:_SY|_SX)\d+_', '', bookcover_comp)
            genre = self.get_genres(booklink)
            #create book object

            obj_name = { 'title': title,
            'author': author,
            'page': page,
            'rating': rating,
            'avgrating': avgrating,
            'booklink': booklink,
            'bookcover': bookcover,
            'genre' : genre
            }
            self.store_book_details['books'].append(obj_name)
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
        print(str_rating)
        return rating_map[str_rating]

    def get_genres(self, booklink):
        forbidden_genres = ['Fiction', 'Nonfiction', 'Short Stories', 'Anthology', 'Adult']
        res = requests.get(booklink)
        if (res.status_code == 200):
            intended_class = 'BookPageMetadataSection__genres'
            parse_only= SoupStrainer(class_= intended_class)
            soup = BeautifulSoup(res.content, 'html.parser', parse_only=parse_only)
            genres = [span.text.strip() for span in soup.find_all('span', class_='Button__labelItem')]
            for genre in genres:
                if genre not in forbidden_genres:
                    return genre
    def update_count(self, key,value, inc = 1):
        self.store_book_details.setdefault((key), {})
        self.store_book_details[key][value] = self.store_book_details[key].get(value, 0) + inc
    
    def format_element(self,class_name, tag='div'):
        return self.rows.find_next('td', class_=f'field {class_name}').find(tag).text.strip()