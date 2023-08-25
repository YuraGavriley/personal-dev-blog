from django.contrib import admin

from .models import Post, Author, Tag, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "tags", "date",)
    list_display = ("title", "date", "author",)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ("user_name", "date", "user_email",)
    list_display = ("comment", "post", "user_name", "date",)
    search_fields = ("user_name", "user_email", "comment",)


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
