import requests;
from bs4 import BeautifulSoup;

class Users():
    def __init__(self,id):
        self.id = id
        self.result = {'Status' : True, 'Message': 'User exists!'}
        
    def validate(self):
        url = f'https://goodreads.com/user/show/${id}'
        res = requests.get(url)
        if (res.status_code == 200):
            soup = BeautifulSoup(res.content, 'html.parser')
            if (soup.find('a', class_='gr-button')['href'] == 'https://www.goodreads.com/'):
                self.result['Status'] = False
                self.result['Message'] = 'Invalid User ID. Please enter the correct ID'
        return self.result
