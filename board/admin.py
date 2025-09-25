from django.contrib import admin
from .models import Post, Reply

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('category',)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('post__title', 'author__username')
