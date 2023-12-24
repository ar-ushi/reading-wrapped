from fetch_book_details import BookDetails
from flask import Flask, request
import requests

app = Flask(__name__) 

@app.route('/wrapped', methods=['GET'])
def fetch_goodreads_data():
    id = request.args.get('gr_user_id')
    year= request.args.get('year')
    bd = BookDetails(19117004, 2023)
    book_details_data = bd.get_parsed_html()
    return book_details_data

if __name__ == "__main__":
    app.run(debug=True)