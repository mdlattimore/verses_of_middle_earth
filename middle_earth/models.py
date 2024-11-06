from django.db import models
from django.urls import reverse
from .templatetags import custom_filters
from django.utils.html import format_html

class Character(models.Model):
    class Meta:
        verbose_name_plural = "Characters"
    RACE_CHOICES = [
        ("Human", "Human"),
        ("Elf", "Elf"),
        ("Dwarf", "Dwarf"),
        ("Hobbit", "Hobbit"),
        ("Valar", "Valar"),
        ("Maiar", "Maiar"),
        ("Orc", "Orc"),
        ("Uruk-Hai", "Uruk-Hai"),
        ("Goblin", "Goblin"),
        ("Eagle", "Eagle"),
        ("Spider", "Spider"),
        ("Troll", "Troll"),
        ("Ent", "Ent"),
        ("Balrog", "Balrog"),
        ("Dragon", "Dragon"),
        ("Wight", "Wight"),
        ("Other/Unknown", "Other/Unknown"),
    ]
    name = models.CharField(max_length=100)
    aka = models.CharField(max_length=100, blank=True, null=True, verbose_name="AKA")
    race = models.CharField(max_length=100, choices=RACE_CHOICES)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='character_pictures/', blank=True)
    picture_credit = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('verse_detail', args=[str(self.id)])
    

class Verse(models.Model):
    """Page numbers for The Lord of the Rings (The Fellowship of the Ring, The Two Towers, 
    and The Return of the King) are taken from 
    Tolkien, J. R. R. 2021. The Lord of the Rings Illustrated. William Morrow & Company.
    Also, while the printed LOTR version referenced has the entire LOTR in one volume, references 
    are given in the name of each of the individual books (The Fellowship of the Ring, containing
    Books I and II; The Two Towers, containing Books III and IV; and The Return of the King,
    containing Books V and VI). 
    
    Unless necessary to avoid confusion or (as in the case of Tom Bombadil), the speaking character 
    is almost always referred to by his/her entire name, the speaker should only be listed using 
    the first or commonly used name. For example, Frodo instead of Frodo Baggins or Sam instead of
    Sam Gamgee. Where a speaker may have more than one common name, the name the speaker uses at
    the time of speaking the verse should be used. For example, the gray wizard may be called
    Mithrandir in The Silmirillion but Gandalf in The Hobbit.

    To address difficulties in searching texts containing unicode escape codes, all words have been 
    normalized to remove any diacritical marks so common in Middle Earth literature. So, for example,
    instead of Túrin, the character's name is saved and shown as Turin.

    For all books, there are also references to "Books" and Chapters
    to facilitate use of other printed versions that may not follow the same pagination as
    the cited versions. 
    """
    class Meta:
        verbose_name_plural = "Verses"

    SILMARILLION = "SI"
    HOBBIT = "HO"
    FELLOWSHIP = "FR"
    TOWERS = "TT"
    KING = "RK"
    UNFINISHED = "UT"
    CHILDREN = "CH"
    BEREN = "BL"
    GONDOLIN = "FG"
    NUMENOR = "FN"
    BOOK_CHOICES = {
        SILMARILLION: "The Silmarillion",
        HOBBIT: "The Hobbit",
        FELLOWSHIP: "The Fellowship of the Ring",
        TOWERS: "The Two Towers",
        KING: "The Return of the King",
        UNFINISHED: "Unfinished Tales",
        CHILDREN: "The Children of Hurin",
        BEREN: "Beren and Luthien",
        GONDOLIN: "The Fall of Gondolin",
        NUMENOR: "The Fall of Numenor"
        }
    
    text = models.TextField()
    speaker = models.ManyToManyField(Character)
    context = models.TextField()
    book = models.CharField(max_length=100, choices=BOOK_CHOICES)
    sub_book = models.CharField(max_length=20, blank=True, null=True)
    chapter = models.CharField(max_length=10, blank=True, null=True)
    page = models.CharField(max_length=10, blank=True, null=True)


    def __str__(self):
        return f"{self.text[:50]}"
    
    def get_absolute_url(self):
        return reverse('character_detail', args=[str(self.id)])
    
    @property
    def blurb(self):
        # Split the text at the first line break and return the first line.
        first_line = self.text.split('\n', 1)[0]
        blurb_text = custom_filters.add_tooltips(first_line)
        return format_html(blurb_text) 
    

class Place(models.Model):
    SUB_CONTINENTS_CHOICES = [
        ("Beleriand", "Beleriand"),
        ("Middle Earth at End of Third Age", "Middle Earth at End of Third Age")
    ]
    name = models.CharField(max_length=100)
    sub_continent = models.CharField(max_length=100, choices=SUB_CONTINENTS_CHOICES, blank=True, null=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='place_pictures/', blank=True)
    picture_credit = models.CharField(max_length=250, blank=True, null=True)


class Thing(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='thing_pictures/', blank=True)
    picture_credit = models.CharField(max_length=250, blank=True, null=True)