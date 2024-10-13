from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(null=True, blank=True) # (upload_to='posts/')
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts')


    def __str__(self):
        return self.title           # это для того чтобы определять что мы видим когда обращаемся к обьектам в таблице


class Category(models.Model):
    text = models.CharField(max_length=200)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.text