from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.response import Response
import random
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
from .serializers import DefinitionSerializer, SearchDefinitionSerializer
from .models import Definition
from .scrape import scrape_words

from django.db.models import Q


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