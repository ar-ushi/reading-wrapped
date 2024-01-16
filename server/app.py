from fetch_book_details import BookDetails
from flask import Flask, request
from flask_cors import CORS
import asyncio

app = Flask(__name__) 

CORS(app, resources={r'/*' : {'origins': '*'}})

@app.route('/wrapped', methods=['GET'])
async def fetch_goodreads_data():
    id = request.args.get('gr_user_id')
    year= request.args.get('year')
    bd = BookDetails(19117004, 2022)
    return await bd.get_parsed_html()
    

if __name__ == "__main__":
    app.run(debug=True)