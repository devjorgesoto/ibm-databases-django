from django.contrib import admin
# <HINT> Import any new Models here
from .models import Instructor, Learner, Course, Lesson, Exam, Question, Choice


# <HINT> Register QuestionInline and ChoiceInline classes here

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Register your models here.

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_learners', 'full_time']
    list_filter =  ['full_time']

class LearnerAdmin(admin.ModelAdmin):
    list_display = ['user','occupation', 'social_link']
    list_filter = ['occupation']


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name','pub_date', 'total_enrollment')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']
    
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ChoiceInline]
    list_display = ['exam_title']
 
class QuestionAdmin(admin.ModelAdmin):
    inlines =[ChoiceInline]
    list_display = ['question_content', 'choice']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_content']


# Admin Site Register

admin.site.register(Instructor,InstructorAdmin)
admin.site.register(Learner,LearnerAdmin)

admin.site.register(Course, CourseAdmin)
#admin.site.register(Lesson, LessonAdmin)
admin.site.register(Exam, ExamAdmin)

#admin.site.register(Question,QuestionAdmin)
#admin.site.register(Choice, ChoiceAdmin)
