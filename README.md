Night 1
========

Why django
--------

* python is developer friendly

    batteries included

    human readable code

* large, open development community

* internationalization

* easy(ish) and powerful (sort of)

Hello python
--------

```python
$ python
>>> print 'hello world'
>>> function hello(name):
>>>     print "hello "+name+"!"
>>> hello('sweetie')
```

hello django
--------

The development runserver can be started in a terminal with the following command.

```bash
$ python manage.py runserver 0.0.0.0:8000
```

You can now view the django app on http://[websiteurl]:8000

As you can see, django gives us a very boring looking test page to let us know it is working.
This page can be replaced by adding a url in `intro/urls.py`.

```python
urlpatterns = patterns('',
    (r'','views.home'),
    # Snip!!
)
````

Now it needs a function	`home` in a file `views.py`. Create `intro/views.py` and enter in the following:

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

*** url - view - render template (slide)
** simple model (photos)
*** don't worry about classes!!
*** outline of the photo table (slide)
*** what information do we want to show?
*** create model
   image = FileField
   name = CharField
   uploaded = datetimefield
   credit = CharField
   category = charfield + choices
   mention id
*** sync db
** django admin
*** uncomment 2 lines in urls
*** uncomment 1 line in settings
*** create photo.admin and register app
** template for photo
*** base.html + extends
*** add view for photos
*** add a list of the photos
** sorl
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
