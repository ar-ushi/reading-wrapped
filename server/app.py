from fetch_book_details import BookDetails
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__) 

CORS(app, resources={r'/*' : {'origins': '*'}})

@app.route('/wrapped', methods=['GET'])
def fetch_goodreads_data():
    id = request.args.get('gr_user_id')
    year= request.args.get('year')
    bd = BookDetails(id, year)
    book_details_data = bd.get_parsed_html()
    return book_details_data

if __name__ == "__main__":
    app.run(debug=True)