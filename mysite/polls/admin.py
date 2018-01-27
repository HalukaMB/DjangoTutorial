from django.contrib import admin

from .models import Question

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):

    #OR admin.StackedInline
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    #this is for the individual question page

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    #this is for the question page
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #fields = ['pub_date', 'question_text']
    list_filter = ['pub_date']
    search_fields = ['question_text']




admin.site.register(Question, QuestionAdmin)
