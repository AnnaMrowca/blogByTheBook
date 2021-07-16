from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):

    """Non standard manager 'Published', further reference to code in class Post"""

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):

    """Model of Post"""

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)

    # """Slug is used to create SEO (Search Engine Optimization) URLs, that will contain letters, numbers
    # and special characters, unique_for_date will help to build URLs with publication date and field slug"""

    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # """ Foreign Key = here relation one to many, CASCADE means that after object is deleted,
    # all related posts will be deleted as well """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() #default manager
    published = PublishedManager() #mon-standard manager


    # """ Class meta contains metadata, '-publish' means that we want to display posts sorted descending =
    #   = last published posts will be on the top"""


    class Meta:

        ordering = ('-publish',)


    def __str__(self):
        return self.title

    """absolute_url allows reverse to act. Reverse helps create url: it works this way: 
    we have route form Warsaw to Wroclaw through Lodz; we can give only beginning, end and stop point and Django based on that creates url"""

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:

        ordering = ('created',)

    def __str__(self):
        return f'Comment added by {self.name} for post {self.post}'