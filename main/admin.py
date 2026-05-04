from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Topic, Lesson, Test, Question, Answer, Result


admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)