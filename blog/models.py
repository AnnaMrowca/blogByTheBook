from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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

    # """ Class meta contains metadata, '-publish' means that we want to display posts sorted descending =
    #   = last published posts will be on the top"""


    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title
