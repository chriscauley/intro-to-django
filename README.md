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
    if request.method == "POST" and form.is_valid(): # The order is important here
        comment = form.save(commit=False)
        comment.photo = photo
        comment.save()
	return HttpResponseRedirect(request.path+"?success=true")

    values['form'] = form

    return TemplateResponse(request,'photo_detail.html',values)
```

The reason the order of `if request.method == "POST" and form.is_valid():` is important is that and "truncates" in python. If `request.method` is not `"POST"`, then the and statement will return `False` without checking `form.is_valid()`. When you validate a form by calling `form.is_valid()`, it applies the error messages (since the form is empty, there will be errors).

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

Classes
--------

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

That's super unreadable. To get a more readable list let's create a function, `print_dir`

```python
>>> def print_dir(obj):
...    for string in obj:
...        print string
...
>>> print_dir(x)
```

I supressed the output for brevity. 
A class is a generic object that can be used to make objects. 
By convention, classes are written in CamelCase.

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

Here `count` is a property, accessed like `some_object.some_property`,
`add` is a method. Methods need at least one argument, `self` which is used to refer to the object.
Methods are functions and must be called like 'some_object.some_method(arg1,arg2...)`
Self is automatically passed in and should not be written in when the object is called.

Classes can inherit from other classes. 
The new class has all the methods and attributes of the old class.

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

Modifying the Admin - List View
--------

`ModelAdmin` and all subclasses of it are used to display model in the admin interface (derp).
Visit 
https://docs.djangoproject.com/en/1.4/ref/contrib/admin/#modeladmin-options 
for a comprehensive list of ModelAdmin options.

The admin consists of the Index (`/admin/`),
app index (`/admin/<app-name>/`),
list view (`/admin/<app-name>/<model-name>/`),
and change-list view (`/admin/<app-name>/<model-name>/<id>/`).
All of these urls were set up when you put `(r'^admin/',include(admin.urls)),` in `urls.py`.

By default, the list view only shows `__unicode__` for every object.
This can be modified by changing the list_display option. 
In `photo/admin.py` create a `CommentAdmin` class and add it to the comment register function

```python
class CommentAdmin(admin.ModelAdmin):
    list_display = ('screenname','photo','text','approved')

admin.site.register(Comment,CommentAdmin)
```

Now if you look at the list view in the admin (`/admin/photo/comment`) you'll see more columns.
Additionally we can make models editable from the admin interface. 
`list_filter` can be set so that you can view only approved or unapproved comments.

```python
class CommentAdmin(admin.ModelAdmin):
    list_display = ('screenname','photo','text','approved')
    list_editable = ('approved',)
    list_filter = ('approved',)
```

Notice the trailing comma in list editable. A tuple with only one entry needs this.

Any method or property on the Comment model can be put into the list.
Additionally, methods on the 

```python
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','screenname','edit_photo','text','approved')
    list_editable = ('approved',)
    list_filter = ('approved',)
    def edit_photo(self,obj):
        return "<a href='/admin/photo/photo/"+str(obj.photo.id)+"'>"+obj.photo.name+"</a>"
    edit_photo.allow_tags = True
```

Now the photo can be edited by clicking the link!

Modifying the Admin - Change List View
--------

The above problem can also be solved by modifying the change view using `admin.TabularInline`.
This creates a mini change view at the bottom of a Model's page for modifying another model.
The following all of a given Photo's comments to be seen/modified from that Photo's change view.

```python
class CommentInline(admin.TabularInline):
    model = Comment

class PhotoAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Photo,PhotoAdmin)
```

Typically the admin is accessed by various users.
You are a superuser, which means you can do what you like.
However, you may want to prevent other users from modifying anything but the `approved` field.
This is done with `readonly_fields` options.

```python
class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('screenname','text')
```

Brief Aside - Templates
--------

When modifying a 3rd party app, it is best to extend it rather than modify any existing code.
Let's look at this with the admin. At the command prompt run:

```python
$ python
>>> import django
>>> django.__path__
```

This will print the location of the files used to run django.
Normally you'd leave it here, but we're going to copy it for easy access.
Exit python (ctrl + d) and type the following using the output from above:

```bash
$ cp -r <path-from-above> ~/projects/
```

Create a folder called `admin` in the `intro/templates` folder in your app.
Create an empty file called `login.html` in the new `intro/templates/login/` folder
Refresh the file browser and locate `django/contrib/admin/templates/admin`.
These are the admin templates.
Copy and paste the contents of `login.html` into the new file.
Modify anything and save!

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
