# How to make templates?

PyDFannots uses the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/). Jinja2 is a templating language.

ou can create basic templates basic using the following structure:

``jinja2
% for annotation in highlights %}
..actions...
% endfor %}
``

e can access the highlight using **dot** notation. The list of variables in each highlight is listed in [annotation structure](Annotation_Structure.md).

he following example uses ``annotation`` as the current annotation in the loop. ``text`` is one field of annotation.  

``jinja2
% for annotation in highlights %}
{annotation.text}}
% endfor %}
``

ou can access all the fields this way:

``jinja2
% for annotation in annotations %}
{annotation.content}}
{annotation.text}}
{annotation.page}}
..etc...
% endfor %}
``


## Include content from other files

ou can split into multiple files for organizing your templates. To include another files in your file,  you can use include. If you want to include a CSS in your template,  you can use:

``jinja2
% include 'stylesheet.css' %}
``


 How can I use my templates?

o use custom templates,  you need import them first. To import a template,  you execute:

``
yDFannot --import-template <template1> <template2> ... <templaten>
``

o delete an unused template,  you execute:

``
yDFannot --delete-template <template1> <template2> ... <templaten>
``

If you want to add a custom
