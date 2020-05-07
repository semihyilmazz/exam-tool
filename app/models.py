from datetime import datetime, timedelta

import pypyodbc

class Student:

    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()


    def login(self,student_mail,student_password):

        self.cursor.execute('''select * from Student where StudentEmail = ? and StudentPasswordSalt = ?''',(student_mail,student_password))
        student = self.cursor.fetchone()
        return student

    def get_student_id(self,email):

        self.cursor.execute(''' select StudentID from Student where StudentEmail = ?''',(email))
        return self.cursor.fetchone()[0]

    def get_student_by_id(self,student_id):
        self.cursor.execute("select * from Student where StudentId = {StudentID}".format(StudentID=student_id))
        student = self.cursor.fetchone()
        return student

class Exam:

    def __init__(self,connection):
        self.connecton = connection
        self.cursor = self.connecton.cursor()

    def show_exams_by_studentid(self,student_id):

        self.cursor.execute('''select * from Takes where Takes.StudentID = {student_id} '''.format(student_id=student_id))
        return self.cursor.fetchall()

    def get_exam_details(self,student_id):

        self.cursor.execute('''select * from Takes where Takes.StudentID = {student_id} '''.format(student_id=student_id))
        takes = self.cursor.fetchall()
        # [('215311029', 2, False)]

        exam_ids = []
        for any in takes:
            exam_ids.append(any[1])

        test_details = []
        remanings = []
        for any in exam_ids:
            self.cursor.execute(''' select * from Exam where ExamID = {exam_id}'''.format(exam_id=any))
            test_details.append(self.cursor.fetchall()[0])

            self.cursor.execute(''' select ExamDate from Exam where ExamId = {exam_id}'''.format(exam_id=any))
            exam_date = self.cursor.fetchone()[0]
            print(exam_date)

            now = datetime.now()
            remainig_time = exam_date - now

            seconds = remainig_time.total_seconds()
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = seconds % 60
            remanings.append(hours * 60 + minutes)

        return test_details, remanings


    def single_exam_details(self,exam_id):

        self.cursor.execute(''' select * from Exam where ExamID = {exam_id}'''.format(exam_id=exam_id))
        test_detail = self.cursor.fetchone()
        return test_detail

    def is_exam_active(self,exam_id):

        self.cursor.execute(''' select ExamDate,ExamDuration from Exam where ExamID = ?''', (exam_id))

        exam_time = self.cursor.fetchone()
        return ((exam_time[0] + timedelta(minutes=exam_time[1]) > datetime.now()) and (datetime.now() > exam_time[0]))


    def get_exam_time_left(self,exam_id):

        self.cursor.execute(''' select ExamDate,ExamDuration from Exam where ExamID = ?''', (exam_id))

        exam_time = self.cursor.fetchone()

        duration = exam_time[0] - datetime.now()  # For build-in functions
        duration_in_s = duration.total_seconds()
        minutes = divmod(duration_in_s, 60)[0]+ exam_time[1]
        return minutes

class Question:

    def __init__(self,connection):

        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_question(self,exam_id,question_id):

        self.cursor.execute("select * from Question where ExamID ={exam_id}".format(exam_id=exam_id))
        exam_question = self.cursor.fetchall()

        #print(exam_question[0][0])
        question_amount = len(exam_question)
        #print(question_amount)
        kac_eklenmeli = exam_question[0][0] - 1

        self.cursor.execute("select * from Question where ExamID = {exam_id} and"
                       " QuestionID = {question_number}".format(exam_id=exam_id,
                                                                question_number=question_id + kac_eklenmeli))

        question = self.cursor.fetchone()
        return question, question_amount


