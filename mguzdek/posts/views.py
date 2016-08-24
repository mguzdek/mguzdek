from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from . import views
from .models import Post
from .forms import PostForm

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_list(request):
    queryset_list = Post.objects.all().order_by("-timestamp")

    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var = "abc"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "objects_list": queryset,
        "title": "My list List",
        "page_request_var" : page_request_var
    }
    return render(request, "post_list.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "title": "Detail",
        "instance": instance,
    }
    return render(request, "post_detail.html", context)

def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Item Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": "Detail",
        "instance": instance,
        "form":form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
