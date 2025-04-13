from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path("", views.index, name="ReadHome"),
    path("bookview/<int:bookid>", views.bookview, name="BookView"),
    path("genre/",views.genre,name="Genre"),
    path("genre_books/<str:genre>", views.genre_books, name="GenreBooks"),
    path("search/", views.search, name="Search"),
    path("library/<int:bookid>", views.library, name="Library"),
    path("librarybooks/", views.library_display, name="LibraryDisplay"),
    path("reading_list/<int:bookid>", views.reading_list, name="readinglist"),
    path("readinglistbooks/", views.Reading_display, name="readinglistDisplay"),
    path("profile", views.profile, name="Profile"),
    path("addbook/", views.addbook, name="Addbook"),
    path("addchapter/<int:bookid>", views.addchapter, name="AddChapter"),
    path("chapters/<int:bookid>", views.chapters, name="Chapter"),
    path("edit/<int:bookid>", views.edit, name="Edit"),
    path("editchapter/<int:chapterid>", views.editchapter, name="EditChap"),
    path("chapterdisplay/<int:chapterid>", views.chapterdisplay, name="ChapterDisplay"),
    path('continue_next/<int:chapterid>', views.continue_next, name='NextChapter'),
    path("save_edit_chp/<int:chpid>", views.save_edit_chp, name="ChapterDave"),
    path('edit_profile', views.edit_profile, name='Edit_Profile'),
    path('update_password', views.update_password, name='UpdatePassword'),
    path('handlelogout', views.handlelogout, name='handlelogout'),
    path('del_chp/<int:chpid>', views.del_chp, name='del_chp'),
    path('del_book/<int:bookid>', views.del_book, name='del_book'),
    path("remove_library/<int:bookid>", views.remove_library, name="RemLibrary"),
    path("remove_readinglist/<int:bookid>", views.remove_readinglist, name="RemReadinglist"),
    path('view_profile/<int:userid>/', views.view_profile, name='view_profile'),
    path('help/', views.help, name='help'),
    path('reading_progress/<int:bookid>', views.reading_progress, name='progess'),
    
]
