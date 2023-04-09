## How to make templates?

PyDFannots uses the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/). Jinja2 is a templating language.

You can create basic templates basic using the following structure:

```jinja2
{% for annotation in highlights %}
...actions...
{% endfor %}
```