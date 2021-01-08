import flask
import os
import json
from flask import jsonify, render_template

class Student:
    def __init__(self,jsonIn):
        self.studentId = jsonIn['studentId']
        self.studentName = jsonIn['name']
        self.courses= jsonIn['courses']
        self.quizzes = jsonIn['quizzes']
    
    def addCourse(self,courseId):
        self.courses.append(courseId)
    
    def addQuiz(self,quizId,score):
        self.quizzes[quizId] = score

    def toJson(self):
        return {'studentId':self.studentId,'studentName':self.studentName,'courses':self.courses,'quizzes':self.quizzes}

class Course:
    def __init__(self,jsonIn):
        self.courseId = jsonIn['courseId']
        self.courseName = jsonIn['courseName']
        self.students = jsonIn['students']
        self.quizzes = jsonIn['quizzes']

    def addStudent(studentId):
        self.students.append(studentId)

    def toJson():
        return {'courseId':self.courseId, 'courseName':self.courseName, 'courses':self.students, 'quizzes':self.quizzes}

class Quiz:
    def __init__(self,jsonIn):
        self.quizName = jsonIn['quizName']
        self.courseId = jsonIn['courseId']
        self.questions = jsonIn['questions']
       self.quizId = jsonIn['quizId']
 
    def toJson(self):
        return {'quizId' : self.quizId, 'quizName' : self.quizName, 'courseId' : self.courseId,'questions' : self.questions}

class Helpers:
	def read_student_data(self):
	    with open(os.path.join('database', 'student.json'), 'r') as database:
	        return json.loads(database.read())

	def read_attempt_data(self,studentId,quizId):
	    fileName = 'attempt'+str(studentId)+str(quizId)+'.json'
	    with open(os.path.join('database', fileName), 'r') as database:
	        return json.loads(database.read())


	def read_quiz_data(self):
	    with open(os.path.join('database', 'quiz.json'), 'r') as database:
	        return json.loads(database.read())

	def read_user_data(self):
	    """
	    :return: Student data in the form of JSON object
	    """
	    with open(os.path.join('database', 'users.json'), 'r') as database:
	        return json.loads(database.read())


	def update_courses_data(self,movie_data):
	    """
	    Function to update Movies data
	    :param movie_data: New data of movies to override previous
	    :return: None
	    """
	    with open(os.path.join('database', 'courses.json'), 'w+') as database:
	        database.write(json.dumps(movie_data))

	def update_student_data(self,movie_data):
	    """
	    Function to update Movies data
	    :param movie_data: New data of movies to override previous
	    :return: None
	    """
	    with open(os.path.join('database', 'student.json'), 'w+') as database:
	        database.write(json.dumps(movie_data))

	def update_quiz_data(self,movie_data):
	    """
	    Function to update Movies data
	    :param movie_data: New data of movies to override previous
	    :return: None
	    """
	    with open(os.path.join('database', 'quiz.json'), 'w+') as database:
	        database.write(json.dumps(movie_data))


app = flask.Flask(__name__)
app.config["DEBUG"] = False 
app.run()

@app.route('/students/', methods=['GET'])
def getStudents():
    try:
        studentArr = []
        student_data = Helpers().read_student_data()
        for key in student_data:
            studentArr.append(Student(student_data[key]))
        return jsonify([s.toJson() for s in studentArr])
    except Exception as e:
        print(e)
        return {"exception" : str(e)}


@app.route('/enroll', methods=['POST'])
def enrollStudent():
    try:
        students = Helpers().read_student_data()
    except Exception as e:
        print(e)
        students = {}
    data = request.get_json()

    if (students[data['studentId']]):
        s = Student(students[data['studentId']])
        s.courses.append(data['courseId'])
        students[data['studentId']] = s.toJson()
        Helpers().update_student_data(students)

    try:
        courses = read_courses_data()
    except Exception as e:
        print(e)
        courses = {}

    if (courses[data['courseId']]):
        c = Course(courses[data['courseId']])
        c.students.append(data['studentId'])
        courses[data['courseId']] = c.toJson()
        Helpers().update_courses_data(courses)

    return {"success" : True}


@app.route('/students/<student_id>/results', methods=['GET'])
def displayScores(student_id):
    """
        Student able to see all quizzes with their respective attempts and scores
    """
    try:
        student_data = Helpers().read_student_data()
        if (student_data[student_id]):
            s = Student(student_data[student_id])
            return s.quizzes
        return {}
        # return invalid_request(success=False, quizzes = dict())
    except Exception as e:
        print(e)
        return {"exception" : str(e)}
        # return invalid_request(success=False,seats = dict())


@app.route('/students/attemptQuiz', methods=['POST'])
def attemptQuiz():
    """
        Student being able to take a quiz and see his score at the end of it.
    """
    student_data = read_student_data()
    quizData = read_quiz_data()
    data = request.get_json()
    attempt = read_student_attempt(data['studentId'],data['quizId'])
    return {"success" : True,"data":data}
    # temp  = Quiz(quizData[data['quizId']])
    # temp2 = Student(student_data[data['studentId']])
    # if (temp and temp2):
    #     score=0
    #     for q in attempt:
    #         if (temp.questions[q]['correctOption']==attempt[q]):
    #             score += 1
    #     temp2.quizzes[data['quizId']] = score
    #     student_data[data['studentId']] = temp2.toJson()
    #     update_student_data(student_data)
    #     return {"success" : True}#return the thing that needs to be changed
    #return {"success" : False}



@app.errorhandler(404)
def page_not_found(e):
    """
        Returns Response object with http status code 404 and renders the 404.html template
    """
    print(e)
    return render_template('404.html'), 404
