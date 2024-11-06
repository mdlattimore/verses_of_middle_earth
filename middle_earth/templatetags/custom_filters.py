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