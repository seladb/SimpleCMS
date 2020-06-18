from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.title[:40] + "...") if len(self.title) > 43 else self.title


class Like(models.Model):
    class Meta:
        unique_together = ['added_by', 'blog_post']

    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Blog post: ' + str(self.blog_post.id) + ' liked by: ' + self.added_by.username


class Comment(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return (self.text[:40] + "...") if len(self.text) > 43 else self.text
