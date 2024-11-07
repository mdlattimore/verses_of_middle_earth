# Annotations  

The project supports annotations of text in the form of tooltips. The tooltips are powered by Tippy.js which is loaded by CDN in the "_base.html" file. The settings for the tooltips are in "static/js/tippyjs.js" which is added by script tag at the bottom of any individual page that uses it. Annotations are mostly easily created in Admin.

To create the annotation, wrap the word or phrase in double braces. After the word or phrase, add a '|' and then the annotation. So, in order to annotate the word "Mark" in the text, "Mark was a merry old soul.", the annotated line in the record would look like this:  

{{Mark|A really great guy!}} was a merry old soul.  

There's a lot of interesting "under the hood" stuff in working with these tooltip style annotations. The centerpiece of making this work in this context is the creation of a custom template filter which is found in "middle_earth/templatetags/custom_filters.py".  
```python
from django import template
import re

register = template.Library()


@register.filter
def add_tooltips(text):
    # Match the pattern for placeholders, e.g., {{word|definition}}
    pattern = r"\{\{(.*?)\|(.*?)\}\}"

    # Replace each placeholder with a <span> containing a title attribute
    def replace_with_tooltip(match):
        word = match.group(1)  # The word to display
        definition = match.group(2)  # The definition for the tooltip
        return f'<span data-tippy-content="{definition}">{word}</span>'

    # Substitute all occurrences in the text
    return re.sub(pattern, replace_with_tooltip, text)

# Make sure the filter allows safe HTML output
add_tooltips.is_safe = True
```  
Adding the "data-tippy-content" attribute to the span is what triggers Tippy. Then, it's just a matter of loading the custom filters in the approprate html files ({% load custom_filters %}) and applying them to the template. So for verse.text, the template tag looks like `{{ verse.text|add_tooltips|safe }}`  

This did create a challenge, however. The original model has a custom "blurb" property which returns the first line of the text (from the beginning up to the first '\n'). I used this for the the ListView of verses. As originally written, however, the blurb included the template tags so, in ListView, instead of displaying "Earendil was a mariner ...", it displayed "{{Earendil|...}} was a mariner." To fix that, the blurb property was modified (with the help of ChatGPT) to return the blurb as HTML, effectively stripping the template tags. But then, this gave rise to a new problem. The verse detail page used the verse.blurb to populate the `<title>` element. Because blurb now returned HTML, the title in the tab displayed the entire html element, `<span data-tippy-content=...><span>`. So, at the suggestion of ChatGPT, I created a second model property, "plain_blurb". The first version of plain_blurb looked just like the original blurb property, simply returning the first line of the text (up to the first '\n'). No more HTML. Great. Problem solved? No. Now I was back to displaying the annotation markup (e.g., {{Earendill|...}}), so the function was modified to extract the first line then, using a regex, strip the annotation markup, leaving us with the plain text for the title. Here are both model properties in their final form:
```python
    @property
    def blurb(self):
        # Split the text at the first line break and return the first line.
        first_line = self.text.split('\n', 1)[0]
        # filter text through tooltips to remove markup from list view
        blurb_text = custom_filters.add_tooltips(first_line)
        return format_html(blurb_text) 
    
    @property
    def plain_blurb(self):
        """Doesn't add the html that the 'blurb' property does
        and strips the annotation markup ({{...|...}})"""
        # Get the first line of the text
        first_line = self.text.split('\n', 1)[0]
        
        # Remove any {{...|...}} patterns (tooltip syntax) using regex
        plain_text = re.sub(r'\{\{(.*?)\|(.*?)\}\}', r'\1', first_line)
        
        return plain_text
    
```