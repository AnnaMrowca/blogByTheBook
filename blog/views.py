from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):

    """ View with list of posts """

    object_list = Post.published.all()
    tag = None
    #wiev takes optional paramether tag_slug, which will be used in URL address

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        #inside of the view we build inital QuerySet, take all published posts and if it finds slug tag using
        #get_object_or_404(), we get Tag with presented slug
        object_list = object_list.filter(tags__in=[tag])
        #we filter list of posts, to get these with assigned tag; we used wyszukiwanie w polu - __in as we have
        # relation many to many and we need to filter along with tags being on the list.

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
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

   # Queryset list o active comments to a given post
    comments = post.comments.filter(active=True)

    if request.method == "POST":
       #comment has been published (request.POST) means that data were taken from this request
       comment_form = CommentForm(data=request.POST)
       if comment_form.is_valid():
           #creating new object Comment, however we do not save it in database yet
           new_comment = comment_form.save(commit=False)
           #Assigning comment to a current post
           new_comment.post = post
           #saving comment in the database
           new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


def post_share(request, post_id):

    """ sharing post via email """

    #takes post based in its id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #form has been sent
        form = EmailPostForm(request.POST)
        #verification of form's fields has been validated as correct
        if form.is_valid():
            cd = form.cleaned_data #if form is valid, we get access to verified data: form.cleaned_data allows us this
            post_url = request.build_absolute_uri(post.get_absolute_url()) #get absolute url helps us
            # taking ultimate (bezwględną) post access path.
            # This path is then used as input data for method request.build_absolute_uri
            # We then build complete url, with HTTP and host name.
            # get_absolute_url conveys data to get_absolute_uri = we get link to post in the email
            # subject and content of the message are taken from verified data taken from the form

            subject = '{} ({}) encourage to read "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read post "{}" on a page {}\n\n comment added by {}: {}'.format(post.title, post_url, cd['name'],
            cd['comments'])
            send_mail(subject, message, 'amrowca@gmail.com', [cd['to']]) #we should add our email and block in settings EMAIL BACKEND
            sent = True


    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
