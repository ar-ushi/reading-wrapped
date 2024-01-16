from fetch_book_details import BookDetails
from flask import Flask, request
from flask_cors import CORS
from validate_users import Users

app = Flask(__name__) 

CORS(app, resources={r'/*' : {'origins': '*'}})

@app.route('/wrapped', methods=['GET'])
async def fetch_goodreads_data():
    id = request.args.get('uid')
    year= request.args.get('year')
    bd = BookDetails(19117004, 2022)
    return await bd.get_parsed_html()

@app.route('/validate_users', methods=['GET'])
def validate_users():
    id = request.args.get('uid')
    users = Users(id)
    return users.validate()
    

if __name__ == "__main__":
    app.run(debug=True)