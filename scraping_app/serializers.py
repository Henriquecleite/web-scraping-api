from rest_framework import serializers
from . import models


class ArticleSerializerVersion1(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name')
    author_name = serializers.CharField(source='author.name')
    hero__image=serializers.CharField(source='hero_image')

    class Meta:
            model=models.Article
            fields=('slug',
                    'title',
                    'hero__image',
                    'author_name',
                    'subject_name',
                    'publish_date',
                    'text',)


class SubjectSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model=models.Subject
        fields=('name','color',)
