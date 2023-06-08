
from django.contrib import admin
from django.urls import include, path
from dictionary.views import add_scraped_words
urlpatterns = [
    path("admin/", admin.site.urls),
    path("scraped/", add_scraped_words, name='scrape-words'),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/definitions/', include('dictionary.urls'))
]
