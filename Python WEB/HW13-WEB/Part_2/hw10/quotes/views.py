from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import TagForm, AuthorForm, QuoteForm, Tag, Author, Quote


def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes/index.html', {'page_obj' : page_obj})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})

@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            choice_author = Author.objects.filter(fullname__in=request.POST.getlist('author'))
            for author in choice_author.iterator():
                new_quote.author.add(author)

            return redirect(to='main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, 'authors': authors, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, 'authors': authors, 'form': QuoteForm()})


def tag_page(request, tag_name):
    all_quotes = Quote.objects.filter(tags__name=tag_name)
    if not all_quotes:
        return render(request, 'quotes/no_quote.html', {'tag_name' : tag_name})
    elif len(all_quotes) == 1:
        first_quote = all_quotes[0]
        return render(request, 'quotes/tag_page.html', {'tag_name' : tag_name, 'first_quote' : first_quote})
    elif len(all_quotes) > 1:
        first_quote = all_quotes[0]
        quotes = all_quotes[1:]
        return render(request, 'quotes/tag_page.html', {'tag_name' : tag_name, 'first_quote' : first_quote, 'quotes' : quotes})
    

def author_page(request, fullname):
    author = Author.objects.filter(fullname=fullname)[0]
    print(author)
    return render(request, 'quotes/author_page.html', {'author' : author})

def top_tags(request):
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'quotes/top_tags.html', {'tags': tags})