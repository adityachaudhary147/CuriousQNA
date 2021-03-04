from django.contrib import admin

# Register your models here.

from .models import Question1, Answers, QuestionGroups


class AnswerInline(admin.TabularInline):
    model = Answers


class Question1Admin(admin.ModelAdmin):

    inlines = [AnswerInline]
    class Meta:
        model = Question1

class QuestionGroupsAdmin(admin.ModelAdmin):

    class Meta:
        QuestionGroups


admin.site.register(Question1, Question1Admin)
admin.site.register(QuestionGroups, QuestionGroupsAdmin)
# admin.site.register(Answers,AnswerInline)