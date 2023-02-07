import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()
from django.conf import settings
import uuid

class Instructor(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    AI_SCIENTIST = 'ai_scientist'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin'),
        (AI_SCIENTIST, 'AI Scientist')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
            self.occupation

class Exam (models.Model):
    id = models.BigAutoField(primary_key=True)

    exam_title = models.CharField(max_length=100)

class Choice(models.Model):
    id = models.BigAutoField(primary_key=True)

        #  <HINT> Create a Choice Model with:
        # Summary: Used to persist choice content for a question
        # One-To-Many (or Many-To-Many if you want to reuse choices) relationship with Question
        # Choice content
        # Indicate if this choice of the question is a correct one or not
        # Other fields and methods you would like to design

    exam = models.ForeignKey (Exam , on_delete=models.CASCADE)

    choice_content = models.CharField(max_length=100)
    #choice_boolean = models.BooleanField(default=False)

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)

    question_content = models.CharField(max_length=100)

    exam = models.ForeignKey (Exam , on_delete=models.CASCADE)
    choice = models.ForeignKey (Choice, on_delete=models.CASCADE)

    #question_grade = models.IntegerField(default=0)
    #question_grade_point = models.IntegerField(default=0)

    # <HINT> Create a Question Model with:
    # Summary: Used to persist question content for a course
    # Has a One-To-Many (or Many-To-Many if you want to reuse questions) relationship with course
    # Foreign key to lesson
    # Has a grade point for each question / # question grade/mark / # question_grade_point
    # Has question content / #question content
    # question text
    # Other fields and methods you would like to design

    # REVIEW THIS IF NEEDED !!!
    # <HINT> A sample model method to calculate if learner get the score of the question
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(
            is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    instructors = models.ManyToManyField(Instructor)
    #lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE) #lesson = models.ManyToOneRel(Lesson)


    name = models.CharField(null=False, max_length=100, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    # def __str__(self):
        #    return "Name: " + self.name + "," + \
        #           "Description: " + self.description

    def __str__(self):
        return self.name

class Lesson(models.Model):
    id = models.BigAutoField(primary_key=True)

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE) #exam = models.ManyToOneRel(Exam)
    course = models.ForeignKey (Course , on_delete=models.CASCADE)

    title = models.CharField(max_length=200, default="Course Title") 
    description = models.CharField( max_length=200, default="Course Description")
    lecture = models.TextField(max_length=1000, default="Course Lecture")

class Enrollment(models.Model):
    id = models.BigAutoField(primary_key=True)

        # Enrollment model
        # <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
        # And we could use the enrollment to track information such as exam submissions


    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Submission(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    # <HINT> The submission model
    # One enrollment could have multiple submission
    # One submission could have multiple choices
    # One choice could belong to multiple submissions

    enrollment = models.ManyToManyField(Enrollment)
    choice = models.ManyToManyField(Choice)

