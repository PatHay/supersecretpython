from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from forms import Register, Login
# from forms import Register, Login, Add_Book, Add_Review
from models import User, Book, Review, Author
import bcrypt

def index(request):
    form = Register()
    login = Login()
    context = {
        'form': form,
        'form2': login,
    }
    return render(request, "belt_test/index.html", context)

def register(request):
    form = Register(request.POST)
    form2 = Login()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            create = User.objects.create(name = form.cleaned_data['name'], 
            alias = form.cleaned_data['alias'], email = form.cleaned_data['email'], 
            password = bcrypt.hashpw(form.cleaned_data['password'].encode('utf8'), bcrypt.gensalt()
            ))
            messages.add_message(request, messages.INFO, form.cleaned_data['name'], extra_tags="name")
            return redirect('/')
    context = {
        "form": form,
        "form2": form2,
    }
    return render(request, "belt_reviewer/index.html", context)

def login(request):
    try:
        request.session['login']
        request.session['alias']
    except KeyError:
        request.session['login'] = []
        request.session['alias'] = []
    form = Register()
    login = Login(request.POST)
    if request.method == 'POST':
        if login.is_valid():    
            print "valid"
            email = login.cleaned_data['email']
            request.session['login'] = User.objects.get(email=email).id
            request.session['alias'] = User.objects.get(email=email).alias
            print request.session['alias']
            return redirect('/books')
            
    # print "failed login form check"
    context = {
        "form": form,
        "form2": login,
    }
    return render(request, "belt_reviewer/index.html", context)

def success(request):
    context = {
        'login': request.session['alias'],
        'books': Book.objects.all(),
        "reviews": Review.objects.order_by("-created_at")[:3],
    }
    return render(request, "belt_reviewer/books.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

# def add_book(request):
#     form = Add_Book()
#     context = {
#         'form': form,
#     }
#     return render(request, "belt_reviewer/add.html", context)

# def add(request):
#     if request.method == 'POST':
#         form = Add_Book(request.POST)
#         form.fields['new_author'].required = False
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             author = Author.objects.get(id=form.cleaned_data['author'])
#             new_author = form.cleaned_data['new_author']
#             review = form.cleaned_data['review']
#             rating = form.cleaned_data['rating']
#             if len(new_author) > 0:
#                 a = Author.objects.create(name = new_author)
#                 a.save()
#                 b = Book.objects.create(title = form.cleaned_data['title'],
#                 author = a)
#                 b.save()
#                 r = Review.objects.create(written_review=review, rating = rating,
#                 reviewer=User.objects.get(id=request.session['login']), 
#                 reviewed_book = b)
#                 r.save()
#             if len(new_author) < 1:
#                 b = Book.objects.create(title = form.cleaned_data['title'],
#                 author = author)
#                 b.save()
#                 r = Review.objects.create(written_review=review, rating = rating,
#                 reviewer=User.objects.get(id=request.session['login']), 
#                 reviewed_book = b)
#                 r.save()
#         return redirect("/books/"+str(Book.objects.get(title=title).id))
#     context = {
#         "form": form,
#     }
#     return render(request, "belt_reviewer/index.html", context)

# def display(request, number):
#     form = Add_Review()
    
#     context = {
#         "book_title": Book.objects.get(id=number).title,
#         "author": Book.objects.get(id=number).author.name,
#         "reviews": Book.objects.get(id=number).book_reviews.all(),
#         "form": form,
#         "number": number,
#         "logged_in": request.session['login'],
#     }
#     return render(request,"belt_reviewer/book_display.html", context)

# def add_review(request, number):
#     if request.method == 'POST':
#         form = Add_Review(request.POST)
#         if form.is_valid():
#             review = form.cleaned_data['review']
#             rating = form.cleaned_data['rating']
#             r = Review.objects.create(written_review=review, rating = rating,
#             reviewer=User.objects.get(id=request.session['login']),
#             reviewed_book=Book.objects.get(id=number))
#             r.save()
#     return redirect("/books/"+str(number))

# def user_display(request, number):
#     context = {
#         "alias": User.objects.get(id=number).alias,
#         "name": User.objects.get(id=number).name,
#         "email": User.objects.get(id=number).email,
#         "total_reviews": User.objects.get(id=number).user_reviews.count(),
#         "reviews": User.objects.get(id=number).user_reviews.all(),
#     }
#     return render(request,"belt_reviewer/user_display.html", context)

# def delete(request, book_number, review_number):
#     Review.objects.filter(reviewer=request.session['login']).filter(id=review_number).delete()

#     if Book.objects.get(id=book_number).book_reviews.count() > 0:
#         return redirect('/books/' + book_number)

#     elif Book.objects.get(id=book_number).book_reviews.count() < 1:
#         Book.objects.get(id=book_number).delete()
#         return redirect('/books')