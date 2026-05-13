from django.urls import reverse
from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(
            author=self, type='A'
        ).aggregate(total=models.Sum('rating')).get('total', 0) * 3

        authors_comments = Comment.objects.filter(
            user=self.user
        ).aggregate(total=models.Sum('rating')).get('total', 0)

        authors_posts_comments = Comment.objects.filter(
            post__author=self,
            post__type='A'
        ).aggregate(total=models.Sum('rating')).get('total', 0)

        self.rating = posts + authors_comments + authors_posts_comments
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    TYPES = [('A', 'Статья'), ('N', 'Новость')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        view_name = 'news_detail' if self.type == 'N' else 'article_detail'
        return reverse(view_name, args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()