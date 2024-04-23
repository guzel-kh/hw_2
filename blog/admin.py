from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}
