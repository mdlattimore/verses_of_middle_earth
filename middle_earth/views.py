from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Verse, Character


class VersesByBook(ListView):
    model = Verse
    template_name = "verses_by_book.html"
    context_object_name = "verses_by_book"
    ordering = ['book', 'sub_book', 'chapter', 'page']


    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter, for example 'category' or 'status'
        filter_param = self.request.GET.get('book')  # Replace 'filter_param' with your actual parameter name
        print(filter_param)
        
        if filter_param:
            queryset = queryset.filter(book=filter_param)  # Adjust filtering as needed for your model
            print(queryset)
        
        return queryset


class VersesListView(ListView):
    model = Verse
    template_name = "verses_list.html"
    context_object_name = "verses"
    ordering = ['book', 'sub_book', 'chapter', 'page']


class VerseDetailView(DetailView):
    model = Verse
    context_object_name = "verse"
    template_name = "verse_detail.html"
    

class CharactersListView(ListView):
    model = Character
    context_object_name = "characters"
    ordering = ['name']
    template_name = "characters_list.html"


class CharacterDetailView(DetailView):
    model = Character
    context_object_name = "character"
    template_name = "character_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verses'] = self.object.verse_set.all()
        return context


class BibliographyView(TemplateView):
    template_name = "bibliography.html"
    