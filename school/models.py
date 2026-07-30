from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    principal = models.CharField(max_length=100)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name
    
class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    room_number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.class_name
    
class Student(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    roll_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Teacher(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Library(models.Model):

    book_name = models.CharField(max_length=200)

    author = models.CharField(max_length=100)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    category = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    rack_number = models.CharField(max_length=30)

    def __str__(self):
        return self.book_name
