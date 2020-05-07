from django.shortcuts import render, HttpResponse, redirect
import requests
import pyodbc
import urllib3
from datetime import date, datetime, timedelta
from app.models import Student, Exam, Question
# Create your views here.

connection = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};"
                            "SERVER=DESKTOP-2U0OHNE;"
                            "DATABASE=semih;"
                            "Trusted_Connection=yes;")

cursor = connection.cursor()

print(connection)


def login(request):


    if request.method == "GET":
        print("login page")
        return render(request,"index.html")
    else:

        email = request.POST["email"]
        password = request.POST["pass"]
        student = Student(connection).login(email,'')

        student_id = Student(connection).get_student_id(email)
        return redirect("/{student_id}/tests".format(student_id = student_id))


def show_tests(request,user_id):

    exams = Exam(connection).get_exam_details(user_id)
    return render(request, "show_tests.html", {"test_details":exams[0], "time_remain":exams[1], "index":len(exams[0])})


def test_detail(request,student_id, exam_id):

    test_details = Exam(connection).single_exam_details(exam_id)
    print(test_details)
    student = Student(connection).get_student_by_id(student_id)
    #(3, 'Midterm 3', datetime.datetime(2020, 4, 7, 20, 0), 120, 'alicakmak@sehir.edu.tr', 'ENGR 101')

    return render(request, "test.html", {"test_detail": test_details, "student": student})


def show_question(request, student_id, exam_id , question_id):

    #if Exam(connection).is_exam_active(exam_id) != True:
    #   return redirect('/{student_id}/tests/{exam_id}'.format(student_id = student_id, exam_id = exam_id))


    if request.method =="POST":
        variable = request.POST['text_area']
        print(variable)
        return redirect("/{student_id}/tests/{exam_id}/{question_id}".format(student_id=student_id, exam_id=exam_id,question_id = question_id+1))

    else:
        time_left = Exam(connection).get_exam_time_left(7)
        question, question_amount = Question(connection).get_question(exam_id,question_id)
        return render(request, "question.html", {"question_amount": question_amount, "range": range(1,question_amount+1),
                                                 "student_id": student_id, "exam_id":exam_id, 'question': question, 'time':time_left})



def time(request):

    time = 'Jan 5, 2021 15:37:25'
    return render(request,'time.html', {'time':  time})
