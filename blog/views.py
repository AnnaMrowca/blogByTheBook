from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

def post_list(request):

    """View with list of posts"""

    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #three posts on every page, creating exemplary of Paginator class
    page = request.GET.get('page') #this takes paramether of the page showing number of current page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if variable is not an integer, then first page of results is collected
        posts = paginator.page(1)

    except EmptyPage:
        #if variable has value > than number of last page with results, then we take last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):

    # """View with post detail"""

   post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

   return render(request, 'blog/post/detail.html', {'post': post})


