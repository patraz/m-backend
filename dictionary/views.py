from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


from .serializers import DefinitionSerializer, SearchDefinitionSerializer
from .models import Definition
from .scrape import scrape_words

import random

from django.db.models import Q


class PostPagination(PageNumberPagination):
    page_size = 15

# class PostViewSet(viewsets.ModelViewSet):
#     pagination_class = PostPagination
#     serializer_class = SearchDefinitionSerializer

#     def get_queryset(self):
        
#         print(self.request.GET.items())
#         for param, value in self.request.GET.items():
#             print(f"Parameter: {param}, Value: {value}")
        # Access request.GET parameters
        # letter = self.request.GET.get('a')
        # queryset = Definition.objects.filter(word__startswith=letter)
        # # Use the param_value in queryset filtering if needed
        
        # return queryset

class DefinitionListViewByLetter(ListAPIView):
    pagination_class = PostPagination
    permission_classes = (AllowAny, )
    serializer_class = DefinitionSerializer

    def get_queryset(self):
        letter = self.kwargs.get('letter')
        if letter:
            queryset = Definition.objects.filter(word__startswith=letter)
        
        return queryset

def add_scraped_words(request):
    word_list = scrape_words(1)

    for word in word_list:
        Definition.objects.create(word=word['word'], meaning=word['meaning'])
    return HttpResponse("Here's the text of the web page.")

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def search_words(request):
    search_query = request.GET.get('q','')
    queryset = Definition.objects.filter(Q(word__icontains=search_query))
    serializer = SearchDefinitionSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_random(request):
    items = list(Definition.objects.all())
    random_item = random.choice(items)
    serializer = DefinitionSerializer(random_item)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    definitions = Definition.objects.all().order_by('-id')[0:10]
    serializer = DefinitionSerializer(definitions, many=True)
    return Response(serializer.data)


class DefinitionListView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DefinitionSerializer
    queryset = Definition.objects.all()


class DefinitionCreateView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DefinitionSerializer
    queryset = Definition.objects.all()

class DefinitionDetailView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DefinitionSerializer
    queryset = Definition.objects.all()
    lookup_field = 'slug'

class DefinitionUpdateView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DefinitionSerializer
    queryset = Definition.objects.all()

class DefinitionDeleteView(DestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = Definition.objects.all()