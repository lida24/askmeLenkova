<<<<<<< HEAD
from django.core.management.base import BaseCommand
from random import choice
from itertools import islice
from ...models import *
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # В скобках: (сокращённая запись комманды, полная запись комманды, тип принимаемого параметра)
        parser.add_argument('-u', '--users', type=int)
        parser.add_argument('-t', '--tags', type=int)
        parser.add_argument('-q', '--questions', type=int)
        parser.add_argument('-a', '--answers', type=int)
        parser.add_argument('-vfa', '--votes_for_answers', type=int)
        parser.add_argument('-vfq', '--votes_for_questions', type=int)
        parser.add_argument('-db', '--database', type=int)

    # Типа функция, связывающая команды с аргументами (или нет...)
    def handle(self, *args, **options):
        if options['users']:
            self.fill_users(options['users'])
        if options['tags']:
            self.fill_tags(options['tags'])
        if options['questions']:
            self.fill_questions(options['questions'])
        if options['answers']:
            self.fill_answers(options['answers'])
        if options['votes_for_answers']:
            self.fill_votes_for_answers(options['votes_for_answers'])
        if options['votes_for_questions']:
            self.fill_votes_for_questions(options['votes_for_questions'])
        if options['database']:
            self.fill_database(options['database'])

    def fill_tags(self, n):
        for i in range(n):
            Tag.objects.create(name=faker.word() + '_' + faker.word())

    def fill_users(self, n):
        logins = set()

        while len(logins) != n:
            logins.add(faker.word() + '_' + faker.word() + str(faker.random.randint(0, 10000)))

        for login in logins:
            user = User.objects.create(username=login, password=faker.password(), email=faker.email())
            profile = Profile.objects.create(user=user)

    def fill_questions(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('id', flat=True))

        for i in range(n):
            question = Question.objects.create(author_id=choice(users), title=faker.sentence(3) + '?',
                                               text=faker.text(), date=faker.date_between('-50d', 'today'))
            question.tags.add(choice(tags))
            if (i % 10000 == 0):
                print(i)

    def fill_answers(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        answers = []

        for i in range(n):
            answer = Answer(question_id=choice(questions), author_id=choice(users),
                            text=faker.sentence())
            answers.append(answer)
            if (i % 10000 == 0):
                print(i)

        batch_size = 100000
        for i in range(int(n / batch_size) + 1):
            batch = list(islice(answers, batch_size))
            if not batch:
                break
            if (i % 10000 == 0):
                print(i)
            Answer.objects.bulk_create(batch, batch_size)

    def fill_votes_for_questions(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        votes = []

        for i in range(n):
            temp_vote = VoteForQuestion(question_id=choice(questions),
                                        author_id=choice(users), vote=faker.random.randint(-1, 1))

            temp_vote.question.change_rating(temp_vote.vote)
            temp_vote.question.save()
            votes.append(temp_vote)
            if (i % 10000 == 0):
                print(i)

        batch_size = 100000
        for i in range(int(n / batch_size)):
            if (i % 10000 == 0):
                print(i)
            batch = list(islice(votes, batch_size))
            if not batch:
                break
            VoteForQuestion.objects.bulk_create(batch, batch_size)

    def fill_votes_for_answers(self, n: int):
        users = list(Profile.objects.values_list('id', flat=True))
        answers = list(Answer.objects.values_list('id', flat=True))
        votes = []

        for i in range(n):
            temp_vote = VoteForAnswer(author_id=choice(users), answer_id=choice(answers),
                                      vote=faker.random.randint(-1, 1))

            temp_vote.answer.change_rating(temp_vote.vote)
            temp_vote.answer.save()
            votes.append(temp_vote)
            if (i % 10000 == 0):
                print(i)

        batch_size = 100000
        for i in range(int(n / batch_size) + 1):
            if (i % 10000 == 0):
                print(i)
            batch = list(islice(votes, batch_size))
            if not batch:
                break
            VoteForAnswer.objects.bulk_create(batch, batch_size)

    def fill_database(self, n: int):
        self.fill_users(n)
        self.fill_tags(n)
        self.fill_questions(n * 10)
        self.fill_answers(n * 100)
        self.fill_votes_for_questions(n * 100)
        self.fill_votes_for_answers(n * 100)
=======
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from app.models import *

from random import choice, sample, randint
from faker import Faker
from datetime import datetime

fake = Faker(["ru_RU"])


class Command(BaseCommand):
    help = 'Генерация базы данных'

    def add_arguments(self, parser):
        parser.add_argument("--profiles", type=int, help="Количество профилей")
        parser.add_argument("--questions", type=int, help="Количество вопросов")
        parser.add_argument("--answers", type=int, help="Количество ответов к вопросу")
        parser.add_argument("--tags", type=int, help="Количество тегов")
        parser.add_argument("--votes", type=int, help="Количество оценок к вопросу")

    def handle(self, *args, **kwargs):
        try:
            profiles_count = kwargs["profiles"]
            questions_count = kwargs["questions"]
            answers_per_question_count = kwargs["answers"]
            tags_count = kwargs["tags"]
            votes_per_question_number = kwargs["votes"]
        except:
            raise CommandError("Some arguments were not provided")

        self.generate_profiles(profiles_count)
        self.generate_tags(tags_count)
        self.generate_questions(questions_count)
        self.generate_answers(answers_per_question_count)

    def generate_users(self, count):
        for i in range(10):
            User.objects.create_user(fake.unique.first_name()+"i", fake.email(),
                                     fake.password(length=fake.random_int(min=8, max=15)))

    def generate_profiles(self, count):
        self.generate_users(10)
        users_ids = list(User.objects.values_list("id", flat=True))
        profile_pics = ["img/profile-pic.jpeg", "img/hitomi3.jpeg"]

        for i in range(10):
            Profile.objects.create(user_id=users_ids[i], user_name=fake.last_name()+"i",
                                   profile_pic=choice(profile_pics))

    def generate_tags(self, count):
        for i in range(10):
            Tag.objects.create(tag_name=fake.word())

    def generate_questions(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))

        for i in range(10):
            question = Question.objects.create(
                author_id=choice(profiles),
                title=fake.sentence(nb_words=3),
                content=fake.text(),
                creation_date=fake.date_time_between(make_aware(datetime(year=2019, month=1, day=1),
                                                                timezone.get_current_timezone()),
                                                     timezone.now())
            )

            tags_count = Tag.objects.count()
            tags = list(set([Tag.objects.get(id=randint(1, tags_count)) for _ in range(randint(1, tags_count))]))
            question.tags.set(tags)

            question.votes.set(sample(profiles, randint(1, len(profiles))),
                               through_defaults={"mark": VoteManager.LIKE})
            question.update_rating()


    def generate_answers(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        for question_id in questions:
            for i in range(10):
                answer = Answer.objects.create(
                    author_id=choice(profiles),
                    related_question_id=question_id,
                    content=fake.text(),
                    creation_date=fake.date_time_between(make_aware(datetime(year=2020, month=10, day=1),
                                                                    timezone.get_current_timezone()),
                                                         timezone.now())
                )
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2
