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

Installing django
--------

To use Django we'll need pip (a python package manager), git (a version control program), and several packages used in image manipulation. These packages are only needed to use sorl-thumbnail. On non-ubuntu systems, feel free to install PIL or skip any sections involving sorl or thumbnails.

```bash
sudo apt-get install python-pip git python-dev python libjpeg-dev zlib-dev libpng-dev python-imaging git-core
```

Next install django using pip. 

```bash 
sudo pip install django
```

And finally checkout the source material for this class. If you do this you can pull future changes when I update the site!

```bash
git clone git@github.com:chriscauley/intro-to-django.git
cd intro-to-django
```

Now your terminal will be in the directory where the course material lives. All future command should be run in this terminal.

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
    (r'^$','intro.views.home'),
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

Reload the page and the photos should appear as 200x200 cropped thumbnails instead of large photos.

Zinna
--------

To get a fully functioning web page, we're going to install a 3rd party blog app called Zinnia. The rest of the class will focus on modifying this application to make a custom blog. First install Zinnia using pip.

```bash
sudo pip install django-blog-zinnia
```

Now add the following 3 apps to the INSTALLED_APPS variable in intro/settings.py

```
INSTALLED_APPS = (
  ...
  'tagging',
  'mptt',
  'zinnia',
)
```

And finally add the zinna urls to the intro/urls.py file. This installs connects Zinnia's urls (and thus views) to your url file. 

```python
url(r'^weblog/', include('zinnia.urls')),
url(r'^comments/', include('django.contrib.comments.urls')),
```

Finally migrate the database. This adds the Zinnia models to the database.

```bash
python manage.py migrate
```

Now if you go to the "/weblog/" url in your browser, you'll see installed on your site.

Night 2
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
    <td></td>
  </tr>
  <tr>
    <td>x = "abcdef"</td>
    <td>{{ x|length }}</td>
    <td>6</td>
    <td></td>
  </tr>
  <tr>
    <td>x = [1,2,3,4,5] </td>
    <td>{{ x|length }}</td>
    <td>5</td>
    <td></td>
  </tr>
  <tr>
    <td>x = "abcdef"</td>
    <td>{{ x|upper }}</td>
    <td>ABCDEF</td>
    <td></td>
  </tr>
  <tr>
    <td>x = 5</td>
    <td>{{ x|add:10 }}</td>
    <td>15</td>
    <td></td>
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
    <td>x = range(4)</td>
    <td>{{ x }}</td>
    <td>[0,1,2,3]</td>
    <td>A list of length 4</td>
  </tr>
  <tr>
    <td>x = range(4)</td>
    <td>
{% for x in x %}<br />
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
    <td>x = []</td>
    <td>
{% for x in x %}<br />
{{ x }}<br />
{% empty %}<br />
There is nothing in x<br />
{% endfor %}
    </td>
    <td>
There is nothing in x
    </td>
    <td></td>
  </tr>
  <tr>
    <td>x = [1,2,3]</td>
    <td>
{% if x|length == 1 %}<br />
There is one item in the list<br />
{% elif not x %}<br />
There are no items in the list<br />
{% else %}<br />
There are {{ x|length }} items in the list<br />
{% endif %}
    </td>
    <td>
There are 3 items in this list.
    </td>
    <td>
- `elif` is short for "else if"<br />
- an empty list `[]` would be taken as `False`.<br />
- `elif` and `else` are not required but `endif` is!
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
    - `now` requires a formatting string<br />
    - it does not take an `endnow` tag.
    </td>
  </tr>
  <tr>
    <td>x = 'my name is chris'</td>
    <td>
{% comment %}<br />
Anything in here will not be printed.<br />
{{ x }}<br />
{% endcomment %}
    </td>
    <td></td>
    <td>
    - Useful for documentation and depracation.
    </td>
  </tr>
</table>

Custom templates can be loaded with `{% load thumbnail %}` as seen above. 
Full documentation for built in template tags and template filters can be found at:

https://docs.djangoproject.com/en/dev/ref/templates/builtins/

Back to the models
--------

Last time we made a photo model. 
This time we're going to improve on the (admittedly weak) category system.
Then we'll add a comment system. 
First we need to put everything under a migration system to change the database without writting SQL.

* South is already installed! Check `requirements.txt` if you don't believe me.

* Add 'south' to the list of `INSTALLED_APPS` in `settings.py`.

* Add south to the database with `$ python manage.py syncdb`.
  (`$` implies you run in terminal)

* Create an initial migration with `$ python manage.py schemamigration photo --init`.

* Fake the migration with `$ python manage.py migrate photo --fake`

The photo app is now controlled by south migrations.
Now we're ready to add a new model and modify the old `Photo` model. 
This uses a new field `models.ForeignKey`.

```python
class Category(models.Model):
    name = models.CharField(max_length='100')
    private = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    src = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length='100')
    uploaded = models.DateTimeField(auto_now_add=True)
    credit = models.CharField(max_length=50,null=True,blank=True)
    #category = models.CharField(max_length=50,blank=True,choices=category_choices)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return "A photo named " + self.name
```

* create migration with `$ python manage.py schemamigration --auto photo`

* run migration with `$ python manage.py migrate photo`

* add the following code to the admin file to make category appear (try without looking first).

```python
from photo.models import Category, Photo

admin.site.register(Category)
```

Now we can do the same with a comment model. At the end of `models.py` add the following. 
Then add run `schemamigration` and `migrate` using `manage.py` and we're ready to learn forms.

```python
class Comment(models.Model):
    photo = models.ForeignKey(Photo)
    screenname = models.CharField(max_length=20,null=True,blank=True)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
```

Clean Up the Templates
--------

With multiple views we'll need a base template to save us a lot of writting. 
In the templates folder make a file called `home.html`. 

```html
{% extends "base.html" %}

{% block content %}
PUT EVERYTHING INSIDE THE &lt;BODY&gt; TAG INSIDE HERE
{% endblock %}
```

And replace the body tag inside `base.html` with the following:

```html
<body>
<h1>
  <a href="/">
    My Photo Gallery!!
  </a>
</h1>
{% block content %}{% endblock %}
</body>
```

Change the `TemplateResponse` template string to `"home.html"` like

```python
    return TemplateResponse(request,'home.html',values)
```

If you don't have questions at this point, you aren't paying attention.

Display the comments on photo detail page
--------

Now we need need to add a url, view, and template for adding comments to photos. 
At this point `urlpatterns` in `urls.py` should look like.
The url function allows us to give the url a name

```python
urlpatterns = patterns('',
    (r'^$','intro.views.home'),
    url(r'^photo/(\d+)/$','intro.views.photo_detail',name='photo_detail')
)
```

Since there is no where that links to the `photo_detail` view, we need to modify `home.html`.
We use the template tag url like `{% url url_name arg1 arg2 ... %}`.
The url name was set in `urls.py` as `'photo_detail'`.
The only argument is the `photo.id` (the bit in parenthesis in the url string).
Django automatically looks up what url matches this and prints it as the tag output.

```html
    <a href="{% url photo_detail photo.id %}"> 
```

And we need a view at `'intro.views.photo_detail'`:

```python
def photo_detail(request,photo_id):
    photo = Photo.objects.get(id=photo_id)
    comments = photo.comment_set.all()
    comments = comments.filter(approved=True)
    values = {
        'photo': photo,
        'comments': comments,
    }
    return TemplateResponse(request,'photo_detail.html',values)
```

and a template (`photo_detail.html` in the templates directory):

```html
{% extends "base.html" %}

{% block content %}
<img src="{{ MEDIA_URL }}{{ photo.src }}" />
<div>{{ photo.name }}</div>

<ul>
  {% for comment in comments %}
  <li>
    "{{ comment.text }}"
    <br />
    {{ comment.screenname }} at {{ comment.added_on }}
  </li>
  {% empty %}
  <li>There are no comments.</li>
  {% endfor %}
</ul>

{% endblock %}
```

Fun with Forms!
--------

We're minutes away from having an (almost) useful app!! 
Normally you'd have to write a lot of html to show inputs, display errors, and show confirmation.
But we can generate a generic form using `django.forms.ModelForm`.
In `views.py`:

```python
from django import forms
from photo.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
```

Add `'form': CommentForm(),` to the values dictionary, and that's it!
We now have all we need to print a form in the template.
In `photo_detail.html` add the form as a table.

```html
<form method="POST">
  <h2>Like what you see? Why not add a comment!</h2>
  <table>
  {{form.as_table}}
  </table>
  <input type="submit" />
</form>
```

Making the form actually do something
--------

We need to add the data from the request object into the form.
We also should remove the photo and approved fields because those are not set by the user.
If the data is clean, save and redirect with a success message.

```python
from django.http import HttpResponseRedirect

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('photo','approved')

def photo_detail(request,photo_id):
    photo = Photo.objects.get(id=photo_id)
    comments = photo.comment_set.all()
    comments = comments.filter(approved=True)
    values = {
        'photo': photo,
        'comments': comments,
        'success': 'success' in request.GET,
    }

    form = CommentForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        comment = form.save(commit=False)
        comment.photo = photo
        comment.save()
        return HttpResponseRedirect(request.path+"?success=true")

    values['form'] = form

    return TemplateResponse(request,'photo_detail.html',values)
```

We add a conditional, `{% if request.GET.success %}`, to display a success message.
Also we need to to hide the `photo`. In `photo_detail.html`:

```html
{% if request.GET.success %}
<p>
  Thank you for your comment! It has been submitted for approval.
</p>
{% else %}
<form method="POST">
  {% csrf_token %}
  <h2>Like what you see? Why not add a comment!</h2>
  <table>
  {{form.as_table}}
  </table>
  <input type="submit" />
</form>
{% endif %}
```

That should do it for the day. 

Night 3
========

Modfying a 3rd party app
--------

Previously we've been looking at writing django applications from scratch. But if you wrote everything from scratch you'd never launch a site. So now we're going to look at adding a new application and then tie our previous models into the application

We'll start by installing a third party app, say django-blog-zinnia. You can find new apps by looking through djangopackages.org or by googling and finding new apps on git hub. Here's the installation documentaiton for Zinnia:

http://django-blog-zinnia.readthedocs.org/en/latest/getting-started/install.html

The easiest way to install this is using pip:

`$ sudo pip install django-blog-zinnia`

It also says we need to install django-mptt, django-tagging, and BeautifulSoup, all of which are installed by pip when you execute the above command. Zinnia's documentation also says to add the following to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
    ...
    'django.contrib.comments',
    'tagging',
    'mptt',
    'zinnia',
    'photo',
    )
```

It is important that you put photo after zinnia because we want `admin.autodiscover()` to execute the admin files in that order.

And we need to add the following `TEMPLATE_CONTEST_PROCESSORS`:

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'zinnia.context_processors.version',) # Optional
```

This is all rather high level stuff that we don't need to worry about. Finally we add the Zinnia urls to `urls.py` in the `urlpatterns = patterns(...` variable. Zinnia offers a high level of customization of urls, but we're only worried about the blog.

```python
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
```

Now we only need to syncdb and migrate!

```python
$ python manage.py syncdb
$ python manage.py migrate
```

Navigate to `/admin/` and `/weblog/` in a web browser and you'll see what looks like a complete website with little code.

Brief Aside - Templates
--------

When modifying a 3rd party app, it is best to extend it rather than modify any existing code.
Let's look at this with the admin. At the command prompt run:

```python
$ python
>>> import zinnia
>>> zinnia.__path__
```

This will print the location of the files used to run django.
Normally you'd leave it here because you aren't going to modify the source code.
We're going to copy it for easy access. Be sure not to modify any files in zinnia, but rather copy them.
Exit python (ctrl + d) and type the following using the output from above:

```bash
$ cp -r <path-from-above> ~/projects/intro
```

In the code you copied from zinnia there is a folder called `zinnia/templates/zinnia`. Django will first look in your main templates directory, `intro/templates` before looking in `zinnia/templates`. It actually looks in all of your `INSTALLED_APPS` in the order that they appear in `intro/settings.py`. All zinnia templates say `{% extends "zinnia/base.html" %}` at the top and `zinnia/templates/zinnia/base.html` says to extend `zinnia/skeleton.html` at the top. 

We're going to copy all of zinnia's templates to the `intro/templates/` folder. This is actually bad practice since upgrading zinnia will be harder in the future if we forget which templates we changed. (you can copy these any way you want, I just used bash since it's semi-universal)

```bash
$ cp -r zinnia/templates/zinnia/ intro/templates/
```

Refresh your file browser (right click on the top) and you'll see that you now have copies of all of the zinnia templates locally stored. If you open `intro/templates/zinnia/skeleton.html` you can edit all of the copy (static text) to match your name. Next you can open `intro/templates/zinnia/base.html` and comment out any sidebar widgets you aren't going to use (for example if you only have one user you may want to remove the authors widget. I recommend using `{% comment %}` and `{% endcomment %}` so that you can put them back in if you want them later (let's say you stop being such a loner and get a friend who wants to write on your blog). You can always go back to the zinnia github page or the zinnia source documentation on github to see the originals.

Classes
--------

In order to modify the admin interface for zinnia, we need to modify the `zinnia/admin.py` classes that use `admin.ModelAdmin`. Don't change this file! After learning about class inheritance we'll be able to modify the pages at `/admin/zinnia/` without changing the source and without re-writing everything.

### Everything's an object!

Previously we've ignored the nature of a python class.
To manipulate the Django Admin interface, we'll need to know a little bit more.
In python "everything is an object".
This means every variable, piece of data, etc. has methods and properties.
To see a list of these, you need to simply use the `dir` function on any object.
From the terminal try the following:

```python
$ python manage.py shell
>>> x = 'monkey'
>>> dir(x)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
```

These are all the things you can do with a string. Event adding two strings together `'monkey'+lovin'` is actually just using the __add__ method on the string `'monkey'.__add__('lovin')`.

A class is a generic object that can be used to make objects. If we want to make a new type of object, we can "inherit" all of the behaviors of another type by creating a new class. By convention, classes are written in CamelCase.

I'm going to show you how to make a class and how to improve it. Don't worry too much about typing this one out. Instead just try to understand the more important concept of inheritance.

```python
>>> class BarrelOfMonkeys():
...     count=0
...     def add(self,number):
...         self.count = self.count + number
...     def add_one(self):
...         self.add(1)
>>> barrel = BarrelOfMonkeys()
>>> print barrel.count
0
>>> barrel.add(5)
>>> print barrel.count
5
```

Here `count` is a property, accessed like `some_object.some_property`, and `add` is a method. Methods need at least one argument, `self` which is used to refer to the object. `self` is simply the barrel created in `barrel = BarrelOfMonkeys()`. Here `barrel` is an instance of `BarrelOfMonkeys`, which is why python will yell that "the first argument of a method must be an instance of BarrelOfMonkeys" if you forget to put `self` in the above functions. Methods are functions and must be called like 'some_object.some_method(arg1,arg2...)`. Self is automatically passed in and should not be written in when the object is called.

Classes can inherit from other classes. The new class has all the methods and attributes of the old class.

```python
>>> class BetterBarrel(BarrelOfMonkeys):
...     max = 10
...     def remaining(self):
...         return self.max - self.count
...     def add(self,number):
...         if self.count == self.max:
...             print "Barrel is full, sorry."
...             return
...         if self.count + number > self.max:
...             print "There is only room for " + str(self.remaining()) + " more monkey(s)."
...             return
...         self.count = self.count + number
>>> barrel2 = BetterBarrel()
>>> barrel2.add(9)
>>> barrel2.add(5000)
There is only room for one more monkey(s).
```

Anytime a method/property has the same name as the old class it is overwritten.
Throughout the class we have been doing this with two classes `django.db.models.Model`
and `django.contrib.admin.ModelAdmin`.

Now we're going to overwrite a lot of methods on the `ModelAdmin` class.

Modifying the Admin
--------

`ModelAdmin` and all subclasses of it are used to display model in the admin interface (derp).
Visit 
https://docs.djangoproject.com/en/1.4/ref/contrib/admin/#modeladmin-options 
for a comprehensive list of ModelAdmin options.

The admin consists of:

Index (`/admin/`),

app index (`/admin/<app-name>/`),

list view (`/admin/<app-name>/<model-name>/`),

and change-list view (`/admin/<app-name>/<model-name>/<id>/`).

All of these urls were set up when you put `(r'^admin/',include(admin.urls)),` in `urls.py`.

Zinnia comes witha highly customized admin. It even has a single image displayed with each blog article. You could re-upload all the images you put in your photo app. Instead we're going to unregister the zinnia admin, modify it to use the Photo model, and re-register it.

First we need to connect the photo model with the Zinnia entry:

```python
#add this to photo/models.py

from zinnia.models import Entry

...

class EntryPhoto(models.Model):
    photo = models.ForeignKey(Photo)
    entry = models.ForeignKey(Entry)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ("order",)
```

Create a schemamigration and apply it:

```bash
$ python manage.py schemamigration --auto photo
$ python manage.py migrate photo
```

Now we have a table linking entries to photos. We could register this model to the admin the same way we did Photo, but this would be awkward to edit. Instead we're going to create an inline. In `photo/admin.py`:

```python
from zinnia.models import Entry
from zinnia.admin import EntryAdmin
from photo.models import Photo, Comment, EntryPhoto

admin.site.unregister(Entry)

class EntryPhotoInline(admin.TabularInline):
    model = EntryPhoto

class EntryAdmin(EntryAdmin):
    inlines = EntryAdmin.inlines + [EntryPhotoInline]

admin.site.register(Entry,EntryAdmin)
```

Now go to the '/admin/zinnia/entry/add/' and you'll notice that there is now a series of inlines for entry photos! This by itself does nothing. We can connect photos to entries in the database, but they are not being dispalyed in the templates.

At this point you'd search the code for any place that 'image' occurs and replace it with the photo image. Luckily I've done that for you. Go to 'intro/templates/zinnia/_entry_detail' and modify any that has 'object.image' with your EntryPhotos. Originally you see:

```html
{% if object.image %}
<div class="entry-image">
  <p>
    {% if continue_reading %}
    <a href="{{ object.get_absolute_url }}" title="{{ object.title }}" rel="bookmark">
      {% endif %}
      <img src="{{ object.image.url }}" alt="{{ object.title }}" class="left" />
      {% if continue_reading %}
    </a>
    {% endif %}
  </p>
</div>
{% endif %}
```

Change it to:

```html
{% if object.entryphoto_set.count %}
<div class="entry-image">
  <p>
    {% if continue_reading %}
    <a href="{{ object.get_absolute_url }}" title="{{ object.title }}" rel="bookmark">
      {% endif %}
      <img src="{{ MEDIA_URL }}{{ object.entryphoto_set.all.0.photo.src }}" alt="{{ object.title }}" class="left" />
      {% if continue_reading %}
    </a>
    {% endif %}
  </p>
</div>
{% endif %}
```

Now if you're like , you've uploaded a file WAY too big to be shown on this page. That's when we need sorl thumbnail. 

```html
{% load thumbnail %}
{% thumbnail object.entryphoto_set.all.0.photo.src "200x200" crop="center" as im %}
<div class="entry-image">
  <p>
    {% if continue_reading %}
    <a href="{{ object.get_absolute_url }}" title="{{ object.title }}" rel="bookmark">
      {% endif %}
      <img src="{{ im.url }}" alt="{{ object.title }}" class="left" widht="{{ im.width }}" height="{{ im.height }}"/>
      {% if continue_reading %}
    </a>
    {% endif %}
  </p>
</div>
{% endif %}
```
