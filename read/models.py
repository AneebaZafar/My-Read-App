from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Genre(models.Model):
    Genre_id=models.AutoField
    Genre_name=models.CharField(max_length=50)

    def __str__(self):
        return self.Genre_name
    

class Book(models.Model):
    book_id=models.AutoField
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    book_name=models.CharField(max_length=50)
    book_author=models.CharField(max_length=50, default="", blank=True, null=True)
    book_genre=models.ForeignKey(Genre, on_delete=models.CASCADE, default="")
    description=models.CharField(max_length=5000, default="", blank=True, null=True)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="read/images", default="")

    def __str__(self):
        return self.book_name
  
class Chapter(models.Model):
    chapter_id=models.AutoField
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    book_id=models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    chapter_name=models.CharField(max_length=500, default="", blank=True, null=True)
    chapter_description=models.CharField(max_length=1000000, default="", blank=True, null=True)
    count=models.IntegerField(default=1)  

class library_book(models.Model):
    lib_id=models.AutoField
    userid=models.ForeignKey(User, on_delete=models.CASCADE, default="")
    lib_bookid=models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    
class Reading_list(models.Model):
    read_id=models.AutoField
    userid=models.ForeignKey(User, on_delete=models.CASCADE, default="")
    read_bookid=models.ForeignKey(Book, on_delete=models.CASCADE, default=1)

class Reading_Progress(models.Model):
    reading_prog_id=models.AutoField
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, default="")
    book_id=models.ForeignKey(Book, on_delete=models.CASCADE, default="")
    last_read_chapter=models.ForeignKey(Chapter, on_delete=models.CASCADE, default="")
