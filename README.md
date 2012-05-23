Night 1
========

Why django
--------

* python is developer friendly

* large, open development community

* internationalization

* easy(ish) and powerful (sort of)

Hello python
--------

```python
$ python
>>> print 'hello world'
>>> def hello(name):
        print "hello "+name+"!"
>>> my_name = 'sweetie'
>>> hello(my_name)
```

<!-- BRIEF ASIDE
show how to save a file and run it from the command line.
-->

Hello django
--------

The development runserver can be started in a terminal with the following command.

```bash
$ python manage.py runserver 0.0.0.0:8000
```

You can now view the django app on `http://[websiteurl]:8000`

As you can see, django gives us a very boring looking test page to let us know it is working.
This page can be replaced by adding a url in `intro/urls.py`.

```python
urlpatterns = patterns('',
    (r'','intro.views.home'),
    # Snip!!
)
````

<!-- BRIEF ASIDE
"What does this do?"
-->

Now it needs a function `home` in a file `views.py`. Create `intro/views.py` and enter in the following:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello Sweetie!")
```

This is fun, but tedious, so instead we use templates.

```python
from django.template.response import TemplateResponse

def home(request):
    values = {
        'name': 'Sweetie!'
    }
    return TemplateResponse(request,'base.html',values)
```

There is already a template in `intro/templates/base.html`. Add `{{ name }}` to it in the body

Simple Model (photos)
--------

Start a new django app with `$ python manage.py startapp photo`. Add the following lines to `photo/models.py`. Don't worry about a class is, for now just fake your way through it.

```python
from django.db import models

category_choices = (
  ('work','Work'),
  ('play','Play'),
)

class Photo(models.Model):
    src = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length='100')
    uploaded = models.DateTimeField(auto_now_add=True)
    credit = models.CharField(max_length=50,null=True,blank=True)
    category = models.CharField(max_length=50,blank=True,choices=category_choices)
```

Now add `photo` to the `INSTALLED_APPS` tuple in `intro/settings.py`. The photo app is now added to your project. However, it is not set up in the database. For that you need to run `$ python manage.py syncdb`. Full documentation on the built in types of fields can be found at:

https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

<!-- BRIEF ASIDE
Now would take a break and show off the model from the shell.
Also it might be useful to show how kwargs work.
"Take notes, but don't try to follow along. We'll see a lot more of this as we go on.
-->

The Django Admin - Great power, little responsibility
--------

Uncomment (remove the # from in front of) these lines in `intro/urls.py`:

```python
from django.contrib import admin
admin.autodiscover()

# and down the page in the big list of urls
    (r'^/admin/',include('admin.urls'),
```

Uncomment `'django.contrib.admin'` in `INSTALLED_APPS` halfway down the file `intro/settings.py`. The admin is now visible on `/admin/`. The photo app does not appear because it is not registered. Register it by creating `photo/admin.py` with the following content.

```python
from django.contrib import admin
from models import Photo

admin.site.register(Photo)
```

Now photos are accesible through the django admin. Try downloading a few images and adding them to the admin.

<!-- BRIEF ASIDE
Add choices to the category field.
Turn auto_now_add on and off to show off what it does
-->

Connecting views.py and models.py
--------

Open views.py and add the photos to the `values` dictionary

```python
from django.template.response import TemplateResponse
from photo.models import Photo

def home(request):
    values = {
        'name': 'Sweetie!',
        'photos': Photo.objects.all(),
    }
    return TemplateResponse(request,'base.html',values)
```

And inside the body of base.html, print the photos with:

```html
<ul>
  {% for photo in photos %}
  <li>
    <img src="{{ MEDIA_URL }}{{ photo.url }}" alt="{{ photo.name }}" />
    <p>
      {{ photo.name }}, by {{ photo.credit }}
    </p>
    <p>
      uploaded on {{ photo.uploaded }}
    </p>
  </li>
  {% empty %}
  <li>
    There are no photos :(
  </li>
  {% endfor %}
</ul>
```

Bonus 3rd party app: sorl.thumbnail
--------

* Add `sorl-thumbnail==11.12` to `requirements.txt`.

* Run `$ sudo pip install -r requirements.txt`.

* Add `sorl.thumbnail` to `INSTALLED_APPS` in the settings file.

* run `$ python manage.py syncdb`

* Change `base.html` to use this new app:

```html
{% load thumbnail %}
<ul>
  {% for photo in photos %}
  <li>
    <a href="{{ MEDIA_URL }}{{ photo.url }}">
      {% thumbnail photo.src "200x200" crop="center" as im %}
      <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}" alt="{{ photo.name }}" />
      {% endthumbnail %}
    </a>
    <p>
      {{ photo.name }}, by {{ photo.credit }}
    </p>
    <p>
      uploaded on {{ photo.uploaded }}
    </p>
  </li>
  {% empty %}
  <li>
    There are no photos :(
  </li>
  {% endfor %}
</ul>
```

Night 1
========

The Django Templating Language
--------

Template variables are are passed in as the third argument to a `TemplateResponse`. 
This is a dictionary, usually called "values". 
Any variable can be printed by placing the `{{ variable_name }}` in braces in a template. 
Any functions are executed, anything else is converted to strings. 
Any attribute can be called with a dot like `{{ variable_name.attribute }}`. 
For models, this is set with the `__unicode__` magic method. 

```python
class Photo(models.Model):
    src = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length='100')
    uploaded = models.DateTimeField(auto_now_add=True)
    credit = models.CharField(max_length=50,null=True,blank=True)
    category = models.CharField(max_length=50,blank=True,choices=category_choices)
    def __unicode__(self):
        return "A photo named " + self.name
```

Now in a template `{{ photo }}` has the same effect as writting `A photo named {{ photo.name }}`.

Other than variables the only programming that can be done in templates are done through filters and tags. 
Template filters are applied with the pip like this:

<table>
  <tr>
    <th>python</th>
    <th>template input</th>
    <th>template output</th>
    <th>notes</th>
  </tr>
  <tr>
    <td>x = "abcdef"</td>
    <td>{{ x }}</td>
    <td>abcdef</td>
  </tr>
  <tr>
    <td>x = "abcdef"</td>
    <td>{{ x|length }}</td>
    <td>6</td>
  </tr>
  <tr>
    <td>x = [1,2,3,4,5] </td>
    <td>{{ x|length }}</td>
    <td>5</td>
  </tr>
  <tr>
    <td>x = "abcdef"</td>
    <td>{{ x|upper }}</td>
    <td>ABCDEF</td>
  </tr>
  <tr>
    <td>x = 5</td>
    <td>{{ x|add:10 }}</td>
    <td>15</td>
  <tr>
    <td>x = "arst"</td>
    <td>{{ x|upper|add:" is "|add:x }}</td>
    <td>ARST is arst</td>
    <td>Template filter argument can be a variable.</td>
  </tr>
  <tr>
    <td>x = "arst"</td>
    <td>{{ x|add:5 }}</td>
    <td></td>
    <td>Can't add int and string, fails silently</td>
  </tr>
</table>

As you can see there is a lot you can do by "piping" variables together. 
Simple programming tools are available int tags.
Tags are denoted with braces and percents `{% tag %}`. 
Some tags require an end tag.

<table>
  <tr>
    <th>python</th>
    <th>template input</th>
    <th>template output</th>
    <th>notes</th>
  </tr>
  <tr>
    <td>a_list = range(4)</td>
    <td>{{ x }}</td>
    <td>[0,1,2,3]</td>
    <td>A list of length 4</td>
  </tr>
  <tr>
    <td>a_list = range(4)</td>
    <td>
{% for x in a_list %}<br />
{{ x }}<br />
{% endfor %}
    </td>
    <td>
0<br />
1<br />
2<br />
3
    </td>
    <td></td>
  </tr>
  <tr>
    <td>a_list = []</td>
    <td>
{% for x in a_list %}<br />
{{ x }}<br />
{% empty %}
There is nothing in a_list
{% endfor %}
    </td>
    <td>
There is nothing in a_list
    </td>
    <td>A list of length 4</td>
  </tr>
  <tr>
    <td>a_list = [1,2,3]</td>
    <td>
{% if a_list|length == 1 %}
There is one item in this list
{% elif not a_list %}
There are no items in this list
{% else %}
There are {{ a_list|length }} items in this list
{% endif %}
    </td>
    <td>
There are 3 items in this list.
    </td>
    <td>
`elif` is short for "else if"<br />
an empty list `[]` would be taken as `False`.<br />
`elif` and `else` are not required but `endif` is!
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
    {% now "m/d/Y" %}
    </td>
    <td>
    5/22/2012
    </td>
    <td>
    `now` requires a formatting string<br />
    it does not take an `endnow` tag.
    </td>
  </tr>
  <tr>
    <td>x = 'my name is chris'</td>
    <td>
{% comment %}
Anything in here will not be printed.
{{ x }}
{% endcomment %}
    </td>
    <td></td>
    <td>
    Useful for documentation and depracation.
    </td>
  </tr>
</table>

Custom templates (like thumbnail above) can be loaded with `{% load library_1 library_2 ... %}` as seen above. Full documentation for built in template tags and template filters can be found at:

https://docs.djangoproject.com/en/dev/ref/templates/builtins/


<!--
*** install sorl in requirements
*** load thumbnail library
*** show sorl crop tag
*** media directory
* Night two
** Static files
** generic models + tags
** model inheritance
** south
** abstract models
** extending models with inlines
** articles app
** overwritting the articles admin using 
** context processors
-->
