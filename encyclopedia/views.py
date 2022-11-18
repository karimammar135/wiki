from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
from . import models
from django import forms
from django.utils.safestring import mark_safe

''' creting new page form '''
class new_page_form(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Encyclopedia's Title"}), label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Content"}))

''' index '''
def index(request):
    # post method
    if request.method == "POST":
        form = request.POST
        entry_name = form['q']

        # checking for a substring
        substring_entries = []
        for entry in util.list_entries():
            if models.is_substring(entry, entry_name):
                substring_entries.append(entry)
        
        # if the given entry name by the user is a substring print a list of the entries that have it as a substring
        if len(substring_entries) > 0:
            return render(request, "encyclopedia/search_result.html", {
                "substring_entries": substring_entries
            })

        # else if the entry isn't a substring display it's content
        else:
            return entry_page(request, entry_name)
    
    # get method
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })  
    
''' entry page '''
current_title = ""
def entry_page(request, entry_name):
    # get the markdown content of the encyclopedia entry
    entry_content = util.get_entry(entry_name)
    # converting markdown content into html content
    if entry_content != None:
        entry_content = markdown2.markdown(entry_content)

    # returning entry html page
    current_title = entry_name
    return render(request, "encyclopedia/entry_page.html", {
        "title": entry_name,
        "entry_content": entry_content
    })

''' new page '''
def new_page(request):
    # post method
    if request.method == "POST":
        form = new_page_form(request.POST)

        # checking for form validation
        # if valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            for existing_title in util.list_entries():
                print(f"{existing_title}")
                # if there is an already existing encyclopedia with this name display an error message
                if title == existing_title:
                    return render(request, "encyclopedia/error.html", {
                        "h1": "This encyclopedia already exists!",
                        "h2": "Try changing the encyclopedia's name."
                    })
                
            # if no errors
            # save encyclopedia
            util.save_entry(title, content)
            # return the user to the page he just created
            return entry_page(request, title)

        # if invalid
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    # get method
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": new_page_form()
        })

# requesting a random page
def random(request):
    entries = util.list_entries()
    import random
    random_1 = random.randint(0,(len(entries) - 1))
    return entry_page(request, entries[random_1])

# editing a page
def edit(request, title):
    # getting the title of th entry page
    title = title

    # post method
    if request.method == "POST":
        # taking the information from the form
        form = request.POST

        # checking for validation
        # if not valid present an error
        if form['edit'] == "":
            return render(request, "encyclopedia/error.html", {
                "h1": "Error! Markdown content is empty."
            })
        # if valid save the content and redirect the user to that page
        else:
            # opening the file and replacing it's old content with the new one's
            with open(f"entries/{title}.md", "w") as f:
                f.write(form['edit'])
            
            return entry_page(request, title)
    
    # get method
    else:
        # get the markdown content of that entry
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
