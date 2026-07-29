from django.shortcuts import render, redirect
from .models import School, Classroom, Teacher, Student
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def home(request): 
    return render(request, 'school/home.html')


def about(request):
    return render(request, 'school/about.html')


def schools(request):
    schools = School.objects.all()
    return render(request, 'school/schools.html', {'schools': schools})
                                                                                                                                                                                                                                

def classrooms(request):
    classrooms = Classroom.objects.all()
    return render(request, 'school/classrooms.html', {'classrooms': classrooms})


def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'school/teachers.html', {'teachers': teachers})


def students(request):
    students = Student.objects.all()
    return render(request, 'school/students.html', {'students': students})

@login_required(login_url="login")
def dashboard(request):

    context = {
        "school_count": School.objects.count(),
        "classroom_count": Classroom.objects.count(),
        "teacher_count": Teacher.objects.count(),
        "student_count": Student.objects.count(),
    }

    return render(request, "school/dashboard.html", context)

@login_required(login_url="login")
def school_list(request):
    schools = School.objects.all()

    return render(
        request,
        "school/schools/list.html",
        {"schools": schools}
    )

@login_required(login_url="login")
def school_add(request):

    if request.method == "POST":

        name = request.POST.get("name")
        principal = request.POST.get("principal")
        address = request.POST.get("address")
        established_year = request.POST.get("established_year")

        errors = {}

        if not name.strip():
            errors["name"] = "School name is required."

        if not principal.strip():
            errors["principal"] = "Principal name is required."

        if not address.strip():
            errors["address"] = "Address is required."

        try:
            established_year = int(established_year)

            if established_year < 1800 or established_year > 2026:
                errors["year"] = "Enter a valid year."

        except:
            errors["year"] = "Year must be a number."

        if errors:
            return render(
                request,
                "school/schools/add.html",
                {
                    "errors": errors,
                    "old": request.POST
                }
            )

        School.objects.create(
            name=name,
            principal=principal,
            address=address,
            established_year=established_year
        )

        return redirect("school_list")

    return render(request, "school/schools/add.html")

@login_required(login_url="login")
def school_edit(request, id):

    school = get_object_or_404(School, id=id)

    if request.method == "POST":

        name = request.POST.get("name")
        principal = request.POST.get("principal")
        address = request.POST.get("address")
        established_year = request.POST.get("established_year")

        errors = {}

        if not name.strip():
            errors["name"] = "School name is required."

        if not principal.strip():
            errors["principal"] = "Principal name is required."

        if not address.strip():
            errors["address"] = "Address is required."

        try:
            established_year = int(established_year)

            if established_year < 1800 or established_year > 2026:
                errors["year"] = "Enter a valid year."

        except:
            errors["year"] = "Year must be a number."

        if errors:

            return render(
                request,
                "school/schools/edit.html",
                {
                    "school": school,
                    "errors": errors
                }
            )

        school.name = name
        school.principal = principal
        school.address = address
        school.established_year = established_year

        school.save()

        return redirect("school_list")

    return render(
        request,
        "school/schools/edit.html",
        {
            "school": school
        }
    )

@login_required(login_url="login")
def school_delete(request, id):

    school = get_object_or_404(School, id=id)

    if request.method == "POST":
        school.delete()
        return redirect("school_list")

    return render(
        request,
        "school/schools/delete.html",
        {"school": school}
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid Username or Password")

    return render(request, "school/login.html")

@login_required(login_url="login")
def classroom_list(request):
    classrooms = Classroom.objects.all()

    return render(
        request,
        "school/classrooms/list.html",
        {"classrooms": classrooms}
    )

@login_required(login_url="login")
def classroom_add(request):

    if request.method == "POST":

        school_id = request.POST.get("school")
        class_name = request.POST.get("class_name")
        room_number = request.POST.get("room_number")
        capacity = request.POST.get("capacity")

        errors = {}

        # School Validation
        if not school_id:
            errors["school"] = "Please select a school."

        # Class Name Validation
        if not class_name.strip():
            errors["class_name"] = "Class name is required."

        # Room Number Validation
        try:
            room_number = int(room_number)

            if room_number <= 0:
                errors["room_number"] = "Room number must be greater than 0."

        except:
            errors["room_number"] = "Enter a valid room number."

        # Capacity Validation
        try:
            capacity = int(capacity)

            if capacity <= 0:
                errors["capacity"] = "Capacity must be greater than 0."

        except:
            errors["capacity"] = "Enter a valid capacity."

        # School Exists?
        if school_id:
            try:
                school = School.objects.get(id=school_id)
            except School.DoesNotExist:
                errors["school"] = "Selected school does not exist."

        if errors:

            schools = School.objects.all()

            return render(
                request,
                "school/classrooms/add.html",
                {
                    "errors": errors,
                    "schools": schools,
                    "old": request.POST,
                }
            )

        Classroom.objects.create(
            school=school,
            class_name=class_name,
            room_number=room_number,
            capacity=capacity,
        )

        return redirect("classroom_list")

    schools = School.objects.all()

    return render(
        request,
        "school/classrooms/add.html",
        {
            "schools": schools
        }
    )

@login_required(login_url="login")
def classroom_edit(request, id):

    classroom = get_object_or_404(Classroom, id=id)

    if request.method == "POST":

        school_id = request.POST.get("school")
        class_name = request.POST.get("class_name")
        room_number = request.POST.get("room_number")
        capacity = request.POST.get("capacity")

        errors = {}

        if not school_id:
            errors["school"] = "Please select a school."

        if not class_name.strip():
            errors["class_name"] = "Class name is required."

        try:
            room_number = int(room_number)

            if room_number <= 0:
                errors["room_number"] = "Room number must be greater than 0."

        except:
            errors["room_number"] = "Enter a valid room number."

        try:
            capacity = int(capacity)

            if capacity <= 0:
                errors["capacity"] = "Capacity must be greater than 0."

        except:
            errors["capacity"] = "Enter a valid capacity."

        if school_id:
            try:
                school = School.objects.get(id=school_id)
            except School.DoesNotExist:
                errors["school"] = "Selected school does not exist."

        if errors:

            schools = School.objects.all()

            return render(
                request,
                "school/classrooms/edit.html",
                {
                    "classroom": classroom,
                    "schools": schools,
                    "errors": errors,
                }
            )

        classroom.school = school
        classroom.class_name = class_name
        classroom.room_number = room_number
        classroom.capacity = capacity

        classroom.save()

        return redirect("classroom_list")

    schools = School.objects.all()

    return render(
        request,
        "school/classrooms/edit.html",
        {
            "classroom": classroom,
            "schools": schools,
        }
    )

@login_required(login_url="login")
def classroom_delete(request, id):

    classroom = get_object_or_404(Classroom, id=id)

    if request.method == "POST":
        classroom.delete()
        return redirect("classroom_list")

    return render(
        request,
        "school/classrooms/delete.html",
        {"classroom": classroom}
    )

@login_required(login_url="login")
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(
        request,
        "school/teachers/list.html",
        {"teachers": teachers}
    )


@login_required(login_url="login")
def teacher_add(request):

    if request.method == "POST":

        classroom_id = request.POST.get("classroom")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        subject = request.POST.get("subject")
        email = request.POST.get("email")

        errors = {}

        if not classroom_id:
            errors["classroom"] = "Please select a classroom."

        if not first_name.strip():
            errors["first_name"] = "First name is required."

        if not last_name.strip():
            errors["last_name"] = "Last name is required."

        if not subject.strip():
            errors["subject"] = "Subject is required."

        if not email.strip():

         errors["email"] = "Email is required."

        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):

         errors["email"] = "Enter a valid email address."

        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
            except Classroom.DoesNotExist:
                errors["classroom"] = "Selected classroom does not exist."

        if errors:

            classrooms = Classroom.objects.all()

            return render(
                request,
                "school/teachers/add.html",
                {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                    "errors": errors,
                    "classrooms": classrooms,
                    "old": request.POST,
                }
            )

        Teacher.objects.create(
            classroom=classroom,
            first_name=first_name,
            last_name=last_name,
            subject=subject,
            email=email,
        )

        return redirect("teacher_list")

    classrooms = Classroom.objects.all()

    return render(
        request,
        "school/teachers/add.html",
        {
            "classrooms": classrooms
        }
    )

@login_required(login_url="login")
def teacher_edit(request, id):

    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":

        classroom_id = request.POST.get("classroom")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        subject = request.POST.get("subject")
        email = request.POST.get("email")

        errors = {}

        if not classroom_id:
            errors["classroom"] = "Please select a classroom."

        if not first_name.strip():
            errors["first_name"] = "First name is required."

        if not last_name.strip():
            errors["last_name"] = "Last name is required."

        if not subject.strip():
            errors["subject"] = "Subject is required."

        if not email.strip():
            errors["email"] = "Email is required."

        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            errors["email"] = "Enter a valid email address."

        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
            except Classroom.DoesNotExist:
                errors["classroom"] = "Selected classroom does not exist."

        if errors:

            classrooms = Classroom.objects.all()

            return render(
                request,
                "school/teachers/edit.html",
                {
                    "teacher": teacher,
                    "classrooms": classrooms,
                    "errors": errors,
                    "old": request.POST,
                }
            )

        teacher.classroom = classroom
        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.subject = subject
        teacher.email = email

        teacher.save()

        return redirect("teacher_list")

    classrooms = Classroom.objects.all()

    return render(
        request,
        "school/teachers/edit.html",
        {
            "teacher": teacher,
            "classrooms": classrooms,
        }
    )

@login_required(login_url="login")
def teacher_delete(request, id):

    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        teacher.delete()
        return redirect("teacher_list")

    return render(
        request,
        "school/teachers/delete.html",
        {"teacher": teacher}
    )

@login_required(login_url="login")
def student_list(request):
    students = Student.objects.all()

    return render(
        request,
        "school/students/list.html",
        {"students": students}
    )

@login_required(login_url="login")
def student_edit(request, id):

    student = get_object_or_404(Student, id=id)
    classrooms = Classroom.objects.all()

    if request.method == "POST":

        classroom_id = request.POST.get("classroom")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        roll_number = request.POST.get("roll_number")

        errors = {}

        if not classroom_id:
            errors["classroom"] = "Please select a classroom."

        if not first_name.strip():
            errors["first_name"] = "First name is required."

        if not last_name.strip():
            errors["last_name"] = "Last name is required."

        if not age:
            errors["age"] = "Age is required."
        else:
            try:
                age = int(age)

                if age < 3 or age > 100:
                    errors["age"] = "Enter a valid age."

            except:
                errors["age"] = "Age must be a number."

        if not roll_number:
            errors["roll_number"] = "Roll number is required."
        else:
            try:
                roll_number = int(roll_number)

                if Student.objects.filter(
                    roll_number=roll_number
                ).exclude(id=student.id).exists():

                    errors["roll_number"] = "Roll number already exists."

            except:
                errors["roll_number"] = "Roll number must be numeric."

        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
            except Classroom.DoesNotExist:
                errors["classroom"] = "Selected classroom does not exist."

        if errors:

            return render(
                request,
                "school/students/edit.html",
                {
                    "student": student,
                    "classrooms": classrooms,
                    "errors": errors,
                    "old": request.POST,
                }
            )

        student.classroom = classroom
        student.first_name = first_name
        student.last_name = last_name
        student.age = age
        student.roll_number = roll_number

        student.save()

        return redirect("student_list")

    return render(
        request,
        "school/students/edit.html",
        {
            "student": student,
            "classrooms": classrooms,
        }
    )

@login_required(login_url="login")
def student_add(request):

    classrooms = Classroom.objects.all()

    if request.method == "POST":

        classroom = request.POST.get("classroom")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        roll_number = request.POST.get("roll_number")

        errors = {}

        if classroom == "":
            errors["classroom"] = "Please select a classroom."

        if first_name.strip() == "":
            errors["first_name"] = "First name is required."

        if last_name.strip() == "":
            errors["last_name"] = "Last name is required."

        if age == "":
            errors["age"] = "Age is required."
        else:
            try:
                age = int(age)

                if age < 3 or age > 100:
                    errors["age"] = "Enter a valid age."

            except:
                errors["age"] = "Age must be a number."

        if roll_number == "":
            errors["roll_number"] = "Roll number is required."
        else:
            try:
                roll_number = int(roll_number)

                if Student.objects.filter(roll_number=roll_number).exists():
                    errors["roll_number"] = "Roll number already exists."

            except:
                errors["roll_number"] = "Roll number must be numeric."

        if errors:

            return render(
                request,
                "school/students/add.html",
                {
                    "errors": errors,
                    "old": request.POST,
                    "classrooms": classrooms
                }
            )

        Student.objects.create(
            classroom=Classroom.objects.get(id=classroom),
            first_name=first_name,
            last_name=last_name,
            age=age,
            roll_number=roll_number
        )

        return redirect("student_list")

    return render(
        request,
        "school/students/add.html",
        {
            "classrooms": classrooms
        }
    )

@login_required(login_url="login")
def student_delete(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "school/students/delete.html",
        {"student": student}
    )

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def student_photos(request, id):

    student = get_object_or_404(Student, id=id)

    folder_path = os.path.join(
        settings.MEDIA_ROOT,
        "Photos",
        str(student.id)
    )

    photos = []

    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            photos.append(f"/media/Photos/{student.id}/{file}")

    if request.method == "POST":

        if "photo" in request.FILES:

            photo = request.FILES["photo"]

            if photo.size > 5 * 1024 * 1024:

                return render(
        request,
        "school/students/photos.html",
        {
            "student": student,
            "photos": photos,
            "upload_error": "Image size must be less than 5 MB."
        }
    )

            allowed_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"
            ]

            extension = os.path.splitext(photo.name)[1].lower()

            if extension not in allowed_extensions:

                return render(
                    request,
                    "school/students/photos.html",
                    {
                        "student": student,
                        "photos": photos,
                        "upload_error": "Only image files are allowed."
                    }
                )

            os.makedirs(folder_path, exist_ok=True)

            storage = FileSystemStorage(location=folder_path)

            storage.save(photo.name, photo)

            return redirect("student_photos", id=student.id)

    return render(
        request,
        "school/students/photos.html",
        {
            "student": student,
            "photos": photos,
        }
    )

@login_required(login_url="login")
def delete_student_photo(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        photo = request.POST.get("photo")

        if photo:

            filename = os.path.basename(photo)

            file_path = os.path.join(
                settings.MEDIA_ROOT,
                "Photos",
                str(student.id),
                filename
            )

            if os.path.exists(file_path):

                os.remove(file_path)

    return redirect("student_photos", id=student.id)