from django.contrib import admin

from app.models import Article, Author, Question, Answer, Tag, QuestionVote, AnswerVote, Profile

# Register your models here.
<<<<<<< HEAD

from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer
from app.models import VoteForQuestion

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(VoteForAnswer)
admin.site.register(VoteForQuestion)
=======
admin.site.register(Article)

admin.site.register(Author)

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)
admin.site.register(Profile)
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2
