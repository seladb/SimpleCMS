from django.contrib import admin
from .models import BlogPost, Comment, Like

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class BlogPostAdmin(admin.ModelAdmin):

    def likes(self, blog_object):
        return blog_object.like_set.count()

    def comments(self, blog_object):
        return blog_object.comment_set.count()

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'writer'):
            obj.writer = request.user
        elif obj.writer is None:
            obj.writer = request.user
        obj.save()

    list_display = ('title', 'published', 'likes', 'comments')

    readonly_fields = ['published', 'writer']

    inlines = [LikeInline, CommentInline]


admin.site.register(BlogPost, BlogPostAdmin)
