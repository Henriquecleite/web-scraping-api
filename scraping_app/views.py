from . import models,serializers
from rest_framework import mixins,generics,pagination


class ArticlesList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    queryset = models.Article.objects.all().order_by('-publish_date')
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return serializers.ArticleSerializerVersion1

    filter_fields=('subject__name',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubjectList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = models.Subject.objects.all()
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return serializers.SubjectSerializerVersion1

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
