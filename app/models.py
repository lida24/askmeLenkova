from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD


############################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="../static/img/pic.png")

    def __str__(self):
        return self.user.username


class QuestionsManager(models.Manager):
    def new_questions(self):
        return self.order_by('date')

    def hot_questions(self):
        return self.order_by('-rating')

    def tag_questions(self, tag_name):
        tag = Tag.objects.filter(name=tag_name)
        return self.filter(tags__in=tag)

    def single_question(self, pk):
        # Важно, чтобы возвращался объект, а не множество объектов.
        return self.filter(id=pk).first()


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)
    date = models.DateField()

    objects = QuestionsManager()
=======
from django_resized import ResizedImageField
from django.utils import timezone


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, verbose_name='Имя пользователя')
    profile_pic = ResizedImageField(size=[60, 60], upload_to='avatars', verbose_name='Аватар')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True, verbose_name='Название тега')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-creation_date")

    def hot_questions(self):
        return self.order_by("-rating")

    def questions_for_tag(self, tag):
        return self.filter(tags__tag_name=tag)


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Заголовок вопроса')
    content = models.TextField(verbose_name='Текст вопроса')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    creation_date = models.DateTimeField(verbose_name='Дата создания вопроса')
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions', related_query_name='question')
    # users who voted for the question
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Оценки вопроса", through='QuestionVote',
                                   related_name="voted_questions", related_query_name="voted_questions")

    objects = QuestionManager()
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2

    def __str__(self):
        return self.title

<<<<<<< HEAD
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def change_rating(self, rate):
        if rate:
            self.rating += 1
        else:
            self.rating -= 1


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return 'Answer on '+self.question.title
=======
    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    def get_answers_count(self):
        return self.answers.count()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers",
                                         related_query_name="answer")
    content = models.TextField(verbose_name='Текст ответа')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')
    creation_date = models.DateTimeField(verbose_name='Дата создания ответа')
    is_marked_correct = models.BooleanField(default=False, verbose_name='Отмечен ли как верный')
    # users who voted for the answer
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Оценки вопроса", through='AnswerVote',
                                   related_name="voted_answer", related_query_name="voted_answer")
    objects = AnswerManager()

    def __str__(self):
        return self.content

    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

<<<<<<< HEAD
    def change_rating(self, rate):
        if rate:
            self.rating += 1
        else:
            self.rating -= 1


class VoteForAnswer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    UNVOTED = 0
    vote_types = [(LIKE, 'Like'), (DISLIKE, 'Dislike'), (UNVOTED, 'Unvoted')]

    vote = models.SmallIntegerField(choices=vote_types, default=UNVOTED)

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + ' --> answer#'+str(self.answer.id)

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответа'


class VoteForQuestion(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    UNVOTED = 0
    vote_types = [(LIKE, 'Like'), (DISLIKE, 'Dislike'), (UNVOTED, 'Unvoted')]

    vote = models.SmallIntegerField(choices=vote_types, default=UNVOTED)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + ' --> question#'+str(self.question.id)

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'
=======

class VoteManager(models.Manager):
    LIKE = 1
    DISLIKE = -1

    def get_likes(self, pk):
        return self.filter(id=pk, mark=VoteManager.LIKE).count()

    def get_dislikes(self, pk):
        return self.filter(id=pk, mark=VoteManager.DISLIKE).count()

    def get_rating(self, pk):
        return self.get_likes(pk) - self.get_dislikes(pk)


class QuestionVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=0,
                               verbose_name='Поставленная оценка')

    objects = VoteManager()

    related_question = models.ForeignKey('Question', verbose_name='Оцениваемый вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка вопроса: {self.mark}'

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'


class AnswerVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=0,
                               verbose_name='Поставленная оценка')

    objects = VoteManager()

    related_answer = models.ForeignKey('Answer', verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка ответа: {self.mark}'

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'


class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class ArticleManager(models.Manager):
    def only_from_marina(self):
        return self.filter(author_id=1)


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    verbose_name = 'Article'
    verbose_name_plural = 'Articles'
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2
