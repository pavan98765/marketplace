from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignUpForm
# Create your views here.
from django.db.models import Q

def index(request):
    query = request.GET.get('query', '')
    item_queryset = Item.objects.filter(is_sold=False)

    if query:
        item_queryset = item_queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    items = item_queryset[:8]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'query': query,
    })


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')

    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })