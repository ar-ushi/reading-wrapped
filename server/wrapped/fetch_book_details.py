from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import asyncio
from wrapped.scrap_book_info import fetch_overall_stats, load_read_books_page, process_read_books

class BookDetails():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.store_book_details = {'totalbooksread': 0, 'totalpagesread': 0 , 'username': '', 'books': []}
        self.rows = []

    async def get_parsed_html(self):
        load_read_books_page(self.id, self.year)
        self.store_book_details['books'] = await process_read_books(True)
        overallstats = fetch_overall_stats()
        self.store_book_details['username'] = overallstats['username']
        self.store_book_details['totalbooksread'] = overallstats['totalbooksread']
        self.store_book_details['totalpagesread'] = overallstats['totalpagesread']
        return self.store_book_details 