from django.contrib import admin
from .models import Post

""" registering Post on admin.py allows us to make it available in admin site: url: http://127.0.0.1:8000/admin/ """

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #these fiels will display in admin
    list_filter = ('status', 'created', 'publish', 'author') #responds to fiels in admin on right side
    search_fields = ('title', 'body') #responds to search function
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' #hierarchy by publish
    ordering = ('status', 'publish') #sorted by status and publish

