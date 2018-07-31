from django.db import models


class Subject(models.Model):
    name=models.CharField(max_length=200, unique=True)
    color=models.CharField(max_length=7,unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name=models.CharField(max_length=100,unique=True)
    picture=models.ImageField(upload_to='author_pics',max_length=400)

    def __str__(self):
        return self.name


class Article(models.Model):
    slug=models.SlugField(max_length=300, unique=True)
    title=models.CharField(max_length=300)    
    author=models.ForeignKey(Author)
    subject=models.ForeignKey(Subject)
    hero_image=models.ImageField(upload_to='hero_image_pics',max_length=400)
    publish_date=models.DateField()
    text=models.TextField()

    def __str__(self):
        return self.slug
