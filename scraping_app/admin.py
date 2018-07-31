from django.contrib import admin
from scraping_app.models import Subject,Author,Article


class ArticleAdmin(admin.ModelAdmin):
    list_display=('id','title','subject','publish_date','author')


admin.site.register(Subject)
admin.site.register(Author)
admin.site.register(Article,ArticleAdmin)