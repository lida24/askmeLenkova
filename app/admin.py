from django.contrib import admin

from app.models import Article, Author, Question, Answer, Tag, QuestionVote, AnswerVote, Profile

# Register your models here.
admin.site.register(Article)

admin.site.register(Author)

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)
admin.site.register(Profile)
