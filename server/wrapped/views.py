from urllib import request
from django.shortcuts import render
from django.http import JsonResponse
from fetch_book_details import BookDetails
from validate_users import Users

async def fetch_goodreads_data():
    id = request.args.get('uid')
    year= request.args.get('year')
    bd = BookDetails(19117004, 2022)
    return await JsonResponse(bd.get_parsed_html())

def validate_users():
    id = request.args.get('uid')
    users = Users(id)
    return JsonResponse(users.validate())
# Create your views here.
