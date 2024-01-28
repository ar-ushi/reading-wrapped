from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from wrapped.fetch_book_details import BookDetails
from wrapped.validate_users import Users
from .models import BookData
from asgiref.sync import sync_to_async

@require_http_methods(["GET"])
async def fetch_goodreads_data(request: HttpRequest):
    id = request.GET['uid']
    year= request.GET['year']
    try:
        book_data = await sync_to_async(BookData.objects.get)(uid=id, year=year)
        return JsonResponse(book_data.yearlystats)
    except BookData.DoesNotExist: 
        bd = BookDetails(id, year)
        readingstats = await bd.get_parsed_html()
        try:
           await sync_to_async(BookData.objects.create)(uid=id, year=year, readingstats = readingstats)
        except IntegrityError:
            pass
        return JsonResponse(readingstats)

@require_http_methods(["GET"])
def validate_users(request: HttpRequest):
    id = request.GET['uid']
    users = Users(id)
    return JsonResponse(users.validate())