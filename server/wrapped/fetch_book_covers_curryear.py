from wrapped.scrap_book_info import fetch_overall_stats, load_read_books_page, process_read_books


class BookDetailsforCurrentYear():
    def __init__(self, userid, year):
        self.id = userid
        self.year = year
        self.curr_year_books =  {'username': '', 'books': []}
    
    async def get_parsed_html(self):
        load_read_books_page(self.id, self.year)
        self.curr_year_books['books'] = await process_read_books()
        overallstats = fetch_overall_stats()
        self.curr_year_books['username'] = overallstats['username']
        return self.curr_year_books