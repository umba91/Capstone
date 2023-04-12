from django.shortcuts import render
from .models import Species
from .models import Bug

# Home Page
def home(request):
    return render(request, 'index.html')

def category_list(request):
    data = Species.objects.all().order_by('-id')
    return render(request, 'category-list.html',{'data':data})

def bug_entry(request):
    data = Bug.objects.all().order_by('-id')
    return render(request, 'bug-entry.html',{'data':data})

def placeholder(request):
    return render(request, 'bug_pages/placeholder.html')

def bug_page_manual(request):
    return render(request, 'bug_pages/placeholder{0}.html'.format('2'))