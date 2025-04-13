from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from math import ceil
from django.contrib.auth.models import User 
from .models import Book,Genre,library_book,Chapter,Reading_list,Reading_Progress
from django.contrib.auth import update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomPasswordChangeForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
#azka:cupcake123#
##esbah:esbah123


@login_required
def index(request):
    allbooks = []
    genbook = Book.objects.values('book_genre', 'id')
    gens = {item['book_genre'] for item in genbook}
    print(f"gens,{gens}")
    for gen in gens:
        books = Book.objects.filter(book_genre=gen)
        n = len(books)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allbooks.append([books, (1, nSlides), nSlides])
        print(allbooks)
    readbook = {'allbooks':allbooks}
    return render(request, 'read/index.html', readbook)


@login_required
def bookview(request,bookid):
    writer=False
    user_id=0
    books = Book.objects.values()
    book_chp=True
    chap=Chapter.objects.filter(book_id_id=bookid)
    n = len(chap)
    library=False
    reading_list=False
    book_writer=None
    if n==0:
        book_chp=False
    for book in books:
        if book['id']==bookid:
            book_writer=book['user_id_id']
            break
        print(book)
    if request.user.is_authenticated:
        user_id=request.user.id
    if book_writer==user_id:
        writer=True
    lib_chp=library_book.objects.values()
    for lib in lib_chp:
        if lib['userid_id']==user_id and lib['lib_bookid_id']==bookid:
            library=True
    reading_list_book=Reading_list.objects.values()
    for read in reading_list_book:
        if read['userid_id']==user_id and read['read_bookid_id']==bookid:
            reading_list=True
    print(book_chp)
    return render(request,'read/bookview.html',{'book':book,'writer':writer,'book_chp':book_chp,'library':library,'reading_list':reading_list})



@login_required
def genre(request):
    genre_name=Genre.objects.values('Genre_name')
    genre_name=[gen['Genre_name'] for gen in genre_name]
    
    genre={'genre_name':genre_name}
    print(genre)
    return render(request, 'read/genre.html', genre)


def genre_id(genre):
    all_genre=Genre.objects.values('id','Genre_name')
    for i in all_genre:
        if i['Genre_name']==genre:
            genre_id=(i['id'])
    return genre_id

@login_required
def genre_books(request,genre):
    allbooks=[]
    genreid=genre_id(genre)
    books=Book.objects.filter(book_genre=genreid)
    n = len(books)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allbooks.append([books, range(1, nSlides), nSlides])
    readbook = {'allbooks':allbooks}
    print(books)
    if n==0:
        return render(request,'read/genre_books.html',{'true':'true'})
    return render(request,'read/genre_books.html',readbook)


def safe_lower(attribute):
    try:
        return str(attribute).lower()
    except Exception as e:
        print(f"Error converting attribute to string: {e}")
        return ""

def searchMatch(query,item):
    if (query in safe_lower(item.description) or
        query in safe_lower(item.book_name) or
        query in safe_lower(item.book_author) or
        query in safe_lower(item.book_genre)):
        return True
    else:
        return False

@login_required
def search(request):
    query = request.GET.get('search')
    print('query',query)
    allbooks = []
    allusers=[]
    all_users=[]
    books = Book.objects.values('book_genre', 'id')
    gens = {item['book_genre'] for item in books}
    for gen in gens:
        booktemp = Book.objects.filter(book_genre=gen)
        print(booktemp)
        book = [item for item in booktemp if searchMatch(query, item)]
        n = len(book)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(book) != 0:
            allbooks.append([book, range(1, nSlides), nSlides])
    users = User.objects.values()
    for username in users:
        if username['username']==query or username['email']==query:
            all_users.append(username)
    nusers=len(allusers)
    nslides=nusers//4+ceil((nusers/4)-(nusers//4))
    if len(users)!=0:
        allusers.append([all_users,range(1,nslides),nslides])

    # Prepare context for rendering both books and users
    context = {'allbooks': allbooks, 'allusers': allusers, 'msg': ""}
    
    # If no matches are found, display a message
    if len(allbooks) == 0 and len(users) == 0 or len(query) < 4:
        context['msg'] = "Please make sure to enter a relevant search query"
    
    return render(request, 'read/index.html', context)


@login_required
def library(request,bookid):
    if request.user.is_authenticated:
        user_id=request.user.id
    libbook = library_book.objects.filter(userid_id=user_id,lib_bookid_id=bookid)
    if len(libbook)!=0:
        return HttpResponse('book is already in library')
    print('libbok',libbook)
    library=library_book(lib_bookid_id=bookid,userid_id=user_id)
    library.save()
    allbooks = []
    genbook = Book.objects.values('book_genre', 'id')
    gens = {item['book_genre'] for item in genbook}
    for gen in gens:
        books = Book.objects.filter(book_genre=gen)
        n = len(books)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allbooks.append([books, range(1, nSlides), nSlides])
        print(allbooks)
    readbook = {'allbooks':allbooks}
    return render(request, 'read/index.html', readbook)

@login_required
def library_display(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        user_id=int(user_id)
    allbook=[]
    allbooks=[]
    libbooks=[]
    no_book=False
    books=Book.objects.values()
    print(books)
    libbook=library_book.objects.values()
    for libb in libbook:
        print('true')
        if libb['userid_id']==user_id:
            libbooks.append(libb)
    if len(libbooks)==0:
        no_book=True
    for book in books:
        for lib in libbooks:
            if book['id']==lib['lib_bookid_id']:
                allbook.append(book)

    n=len(allbook)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    if len(allbook) != 0:
            allbooks.append([allbook, range(1, nSlides), nSlides])
    readbook={'library':allbooks,'no_book':no_book}
    print(library)
    return render(request, 'read/library.html', readbook)


@login_required
def profile(request):
    user_id=None
    if request.user.is_authenticated:
        user_id=request.user.id
        user_id=int(user_id)
        print(user_id)
    no_book=False
    allbook=[]
    allbooks=[]
    books = Book.objects.values()
    for book in books:
        print('true')
        if book['user_id_id']==user_id:
            allbook.append(book)
    print(allbook)
    if len(allbook)==0:
        no_book=True
    n=len(allbook)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    if len(allbook) != 0:
            allbooks.append([allbook, range(1, nSlides), nSlides])
    readbook={'library':allbooks,'no_book':no_book}
    print(library)
    return render(request, 'read/profile.html', readbook)



@login_required
def addbook(request):
 
    if request.method=="POST":
        book_genre=0
        if request.user.is_authenticated:
            user_id=request.user.id
            user_id=int(user_id)
        book_name = request.POST.get('book_name', '')
        book_author = request.POST.get('book_author', '')
        genre = request.POST.get('book_genre', '')
        description = request.POST.get('description', '')
        pub_date = request.POST.get('pub_date', '')
        image = request.FILES.get('image', '')
        print(False)
        genres = Genre.objects.values()
        for gen in genres:
            if gen['Genre_name']==genre:
                book_genre=gen['id']
                book_genre=int(book_genre)
                print(book_genre)
                addbooks = Book(user_id_id=user_id, book_name=book_name, book_author=book_author, book_genre_id=book_genre, description=description,pub_date=pub_date,image=image)
                addbooks.save()
    return render(request, 'read/addbook.html')


@login_required
def addchapter(request, bookid):
    if request.method == "POST":
        # Retrieve form data
        chapter_name = request.POST.get('chapter_name', '').strip()
        chapter_description = request.POST.get('chapter_description', '').strip()
        
        if chapter_name:  # Validate chapter name
            # Get the highest chapter count for the given book
            last_chapter = Chapter.objects.filter(book_id_id=bookid).order_by('-count').first()
            chp_count = last_chapter.count if last_chapter else 0  # Use 0 if no chapters exist
            
            # Create and save the new chapter
            addchapter = Chapter(
                user_id_id=request.user.id,
                book_id_id=bookid,
                chapter_name=chapter_name,
                chapter_description=chapter_description,
                count=chp_count + 1
            )
            addchapter.save()
          # Mark chapter creation as successful

    # Render the template
    return render(request, 'read/addchapter.html', {
        'book_id': bookid,
    })


@login_required
def chapters(request,bookid):
    empty=False
    allchapters=[]
    chapters=Chapter.objects.values()
    for chapter in chapters:
        if chapter['book_id_id']==bookid:
            allchapters.append(chapter)    
    n=len(allchapters)    
    if n==0:
        empty=True
    allchaps={'allchapters':allchapters,'true':empty}
    return render(request, 'read/chapters.html', allchaps)

# @login_required
def chapterdisplay(request,chapterid):
    target=[]
    user_id=None
    chapters=Chapter.objects.values()
    if request.user.is_authenticated:
        user_id = request.user.id
    for chapter in chapters:
        if chapter['id']==chapterid:
            print(chapter)
            target.append(chapter)
            chaps={'target':target}
            try:
                read_progs=Reading_Progress.objects.get(user_id_id=user_id,book_id_id=chapter['book_id_id'])
            except:
                read_progs=None
            if read_progs!=None:
                read_progs.last_read_chapter_id=chapterid
                read_progs.save()
            else:   
                read_progress=Reading_Progress(user_id_id=user_id,book_id_id=chapter['book_id_id'],last_read_chapter_id=chapter['id'])
                read_progress.save()
    return render(request, 'read/chapterdisplay.html', chaps)

@login_required
def continue_next(request,chapterid):
    target=[]
    no_chp=False
    chapters=Chapter.objects.values()
    for chapter in chapters:
        if chapter['id']==chapterid:
            count=chapter['count']
            print(f'count,{count}')
            count=count+1
            bookid=chapter['book_id_id']
            break
    print(f'count2{count}')
    for chap in chapters:    
        if chap['book_id_id']==bookid and chap['count']==count:
            target.append(chap)
            break
    
    if len(target)==0:
        no_chp=True
    
    chaps={'target':target,'no_chp':no_chp}
    print(target)
    return render(request, 'read/chapterdisplay.html', chaps)


@login_required
def reading_progress(request,bookid):
    user_id=None
    target=[]
    chaps={}
    no_chp=False
    if request.user.is_authenticated:
        user_id = request.user.id
    reading_progress=Reading_Progress.objects.values()
    for read in reading_progress:
        if read['user_id_id']==user_id and read['book_id_id']==bookid:
            chapterid=read['last_read_chapter_id']
            chapters=Chapter.objects.values()
            for chapter in chapters:
                if chapter['id']==chapterid:
                    print(chapter)
                    target.append(chapter)
                    break
    if len(target)==0:
            no_chp=True
    chaps={'target':target,'no_chp':no_chp}
    return render(request, 'read/chapterdisplay.html', chaps)

@login_required
def edit(request,bookid):
    empty=False
    allchapters=[]
    chapters=Chapter.objects.values()
    for chapter in chapters:
        if chapter['book_id_id']==bookid:
            allchapters.append(chapter)    
    n=len(allchapters)    
    if n==0:
        empty=True
    allchaps={'chapters':allchapters,'editclass':empty}
    return render(request, 'read/chapters.html', allchaps)       

@login_required
def editchapter(request,chapterid):
    user_id=None
    bookid=None
    name=None
    description=None
    chp=False
    if request.user.is_authenticated:
        user_id=request.user.id
        user_id=int(user_id)
    chapters=Chapter.objects.values()
    for chapter in chapters:
       if chapter['id']==chapterid and user_id==chapter['user_id_id']:
           chp=True
           bookid=chapter['book_id_id']
           name=chapter['chapter_name']
           description=chapter['chapter_description']
    edit={'bookid':bookid,'name':name,'description':description, 'chpid':chapterid, 'chp':chp}
    return render(request, 'read/chapterdisplay.html', edit)

@login_required
def save_edit_chp(request,chpid):
    if request.method=="POST":
        chapter_name = request.POST.get('chp_name', '')
        chapter_description = request.POST.get('chp_dsc', '')
    chapter=Chapter.objects.get(id=chpid)
    chapter.chapter_name=chapter_name
    chapter.chapter_description=chapter_description
    chapter.save()
    print(chapter.chapter_name)
    allbooks = []
    genbook = Book.objects.values('book_genre', 'id')
    gens = {item['book_genre'] for item in genbook}
    for gen in gens:
        books = Book.objects.filter(book_genre=gen)
        n = len(books)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allbooks.append([books, range(1, nSlides), nSlides])
        print(allbooks)
    readbook = {'allbooks':allbooks}
    return render(request, 'read/index.html', readbook)


@login_required
def update_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session to prevent logout
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('Edit_Profile')
        else:
            return HttpResponse ('There was an error updating your password.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'read/update_password.html', {'form': form})

@login_required
def edit_profile(request):
    user_id=None
    username=None
    email=None
    if request.user.is_authenticated:
        user_id=request.user.id
        user_id=int(user_id)
    user=User.objects.get(id=user_id)
    uname=user.username
    u_email=user.email
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        user.username=username
        user.email=email
        user.save()
        update_session_auth_hash(request, user)
        return render (request, 'read/edit_profile.html', {'True':True})
    return render (request, 'read/edit_profile.html', {'username':uname,'email':u_email})

@login_required
def handlelogout(request):
    logout(request)
    return redirect(reverse('login'))



@login_required
def del_chp(request,chpid):
    chapter=Chapter.objects.filter(id=chpid)
    if request.user.is_authenticated:
        chapter.delete()
    return redirect('ReadHome')

@login_required
def del_book(request,bookid):
    book=Book.objects.filter(id=bookid)
    if request.user.is_authenticated:
        book.delete()
    return redirect('ReadHome')


@login_required
def reading_list(request,bookid):
    if request.user.is_authenticated:
        user_id=request.user.id
    Readlistbook =Reading_list.objects.filter(userid_id=user_id,read_bookid_id=bookid)
    if len(Readlistbook)!=0:
        return HttpResponse('book is already in readinglist')
    readlist=Reading_list(read_bookid_id=bookid,userid_id=user_id)
    readlist.save()
    
    return redirect('ReadHome')

@login_required
def Reading_display(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        user_id=int(user_id)
    allbook=[]
    allbooks=[]
    libbooks=[]
    no_book=False
    books=Book.objects.values()
    print(books)
    Readbook=Reading_list.objects.values()
    for libb in Readbook:
        print('true')
        if libb['userid_id']==user_id:
            libbooks.append(libb)
    if len(libbooks)==0:
        no_book=True
    for book in books:
        for lib in libbooks:
            if book['id']==lib['read_bookid_id']:
                allbook.append(book)

    n=len(allbook)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    if len(allbook) != 0:
            allbooks.append([allbook, range(1, nSlides), nSlides])
    readbook={'reading':allbooks,'no_book':no_book}
    return render(request, 'read/reading_list.html', readbook)


@login_required
def remove_library(request, bookid):
    if request.user.is_authenticated:
        user_id = request.user.id
        
        # Filter the library books for the authenticated user and the given book ID
        library_books = library_book.objects.filter(lib_bookid_id=bookid, userid_id=user_id)
        
        # Delete the filtered records
        library_books.delete()

    return redirect('ReadHome')

@login_required
def remove_readinglist(request, bookid):
    if request.user.is_authenticated:
        user_id = request.user.id
        
        # Filter the library books for the authenticated user and the given book ID
        reading_books = Reading_list.objects.filter(read_bookid_id=bookid, userid_id=user_id)
        
        # Delete the filtered records
        reading_books.delete()

    return redirect('ReadHome')

@login_required
def view_profile(request, userid):
    no_books=False
    user_books_data = []
    user_reads_data = []
    print('userid',userid)
    # Get the user's books
    user=User.objects.get(id=userid)
    user_books = Book.objects.filter(user_id=userid)
    print('user_books',user_books)
    n_books = len(user_books)
    n_book_slides = n_books // 4 + ceil((n_books / 4) - (n_books // 4))
    if user_books:
        user_books_data.append([user_books, range(1, n_book_slides), n_book_slides])
    else:
        no_books=True
    read_book=[]
    user_reading_list = Reading_list.objects.values()
    user_reads = []
    all_user=[]
    for ur in user_reading_list:
        if ur['userid_id']==userid:
            all_user.append(ur)
    for entry in all_user:
        book_id=entry['read_bookid_id']
        print('book',book_id)
        read = Book.objects.values()
        for read_book in read:
            if read_book['id']==book_id:
                user_reads.append(read_book)
    n_reads = len(user_reads)
    if len(user_reads)==0:
        no_book=True
    n_read_slides = n_reads // 4 + ceil((n_reads / 4) - (n_reads // 4))
    if user_reads:
        user_reads_data.append([user_reads, range(1, n_read_slides), n_read_slides])

    print(f'User Books Data: {user_books_data}')
    print(f'User Reads Data: {user_reads_data}')

    context = {
        'user': user,
        'userbooks': user_books_data,
        'userreads': user_reads_data,
        'no_books': no_books
    }
    
    return render(request, 'read/view_profile.html', context)


def help(request):
    return render(request, 'read/help.html')



