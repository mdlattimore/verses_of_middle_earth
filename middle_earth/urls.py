from django.contrib import admin
from django.urls import path
from .views import VersesListView, VerseDetailView, CharactersListView, CharacterDetailView, BibliographyView 

urlpatterns = [
    path('verses_list/', VersesListView.as_view(), name="verses_list"),
    path('verse_detail/<int:pk>/', VerseDetailView.as_view(), name="verse_detail"),
    path('characters_list/', CharactersListView.as_view(), name="characters_list"),
    path('character_detail/<int:pk>/', CharacterDetailView.as_view(), name="character_detail"),
    path('bibliograpy', BibliographyView.as_view(), name="bibliography"),
]