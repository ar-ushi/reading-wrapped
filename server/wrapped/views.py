from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from wrapped.fetch_book_details import BookDetails
from wrapped.validate_users import Users

@require_http_methods(["GET"])
async def fetch_goodreads_data(request: HttpRequest):
    id = request.GET['uid']
    year= request.GET['year']
    bd = BookDetails(19117004, 2022)
    readingstats = await bd.get_parsed_html()
    return JsonResponse(readingstats)

@require_http_methods(["GET"])
def validate_users(request: HttpRequest):
    id = request.GET['uid']
    users = Users(id)
    return JsonResponse(users.validate())