## How to make templates?

PyDFannots uses the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/). Jinja2 is a templating language.

You can create basic templates basic using the following structure:

```jinja2
{% for annotation in highlights %}
...actions...
{% endfor %}
```

We can access the highlight using **dot** notation. The list of variables in each highlight is listed in [annotation structure](Annotation_Structure.md).

The following example uses ``annotation`` as the current annotation in the loop. ``text`` is one field of annotation.  

```jinja2
{% for annotation in highlights %}
{{annotation.text}}
{% endfor %}
```

You can access all the fields this way:

```jinja2
{% for annotation in annotations %}
{{annotation.content}}
{{annotation.text}}
{{annotation.page}}
...etc...
{% endfor %}
```

