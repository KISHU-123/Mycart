from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog
# Create your views here.
def index(request):
    myposts = Blog.objects.all()
    print(myposts)
    return render(request,'blogs/index.html',{'myposts':myposts})

def blogpost(request,id):
    post = Blog.objects.filter(post_id = id)[0]
    print(post)

    return render(request,'blogs/blogpost.html',{'post':post})
