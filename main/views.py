from django.shortcuts import render
from .models import Specie
# Home Page
def home(request):
    return render(request, 'index.html')

def category_list(request):
    data = Specie.objects.all().order_by('-id')
    return render(request, 'category-list.html',{'data':data})