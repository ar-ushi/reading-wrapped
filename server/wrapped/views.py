from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from fetch_book_details import BookDetails
from validate_users import Users

@require_http_methods(["GET"])
async def fetch_goodreads_data(request: HttpResponse):
    id = request.GET['uid']
    year= request.GET['year']
    bd = BookDetails(19117004, 2022)
    return await JsonResponse(bd.get_parsed_html())

@require_http_methods(["GET"])
def validate_users(request: HttpResponse):
    id = request.GET['uid']
    users = Users(id)
    return JsonResponse(users.validate())
# Create your views here.
