import os
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Review, Comment, Category, Title, Genre
from users.models import User


class Command(BaseCommand):
    help = 'Импорт CSV-файлов в базу данных'

    def handle(self, *args, **options):
        csv_dir = os.path.join(settings.BASE_DIR, 'static/data')

        # Загрузка данных для Category
        category_file_path = os.path.join(csv_dir, 'category.csv')
        with open(category_file_path, 'r', encoding='utf-8') as category_file:
            csv_reader = csv.DictReader(category_file)
            for row in csv_reader:
                Category.objects.create(name=row['name'], slug=row['slug'])

        self.stdout.write(self.style.SUCCESS('Category успешно импортирован!'))

        # Загрузка данных для Genre
        genre_file_path = os.path.join(csv_dir, 'genre.csv')
        with open(genre_file_path, 'r', encoding='utf-8') as genre_file:
            csv_reader = csv.DictReader(genre_file)
            for row in csv_reader:
                Genre.objects.create(name=row['name'], slug=row['slug'])

        self.stdout.write(self.style.SUCCESS('Genre успешно импортирован!'))

        # Загрузка данных для Title
        title_file_path = os.path.join(csv_dir, 'titles.csv')
        with open(title_file_path, 'r', encoding='utf-8') as title_file:
            csv_reader = csv.DictReader(title_file)
            for row in csv_reader:
                category = Category.objects.get(id=row['category'])
                title = Title.objects.create(
                    name=row['name'],
                    year=row['year'],
                    category=category
                )

        self.stdout.write(self.style.SUCCESS('Title успешно импортирован!'))

        # Обработка связей между Genre и Title
        genre_title_file_path = os.path.join(csv_dir, 'genre_title.csv')
        with open(genre_title_file_path, 'r', encoding='utf-8') as genre_title_file:
            csv_reader = csv.DictReader(genre_title_file)
            for row in csv_reader:
                title_id = row['title_id']
                genre_id = row['genre_id']

                title = Title.objects.get(id=title_id)
                genre = Genre.objects.get(id=genre_id)

                title.genre.add(genre)

        self.stdout.write(self.style.SUCCESS(
            'GenreTitle успешно импортирован!'))

        # Загрузка данных для User
        user_file_path = os.path.join(csv_dir, 'users.csv')
        with open(user_file_path, 'r', encoding='utf-8') as user_file:
            csv_reader = csv.DictReader(user_file)
            for row in csv_reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

        self.stdout.write(self.style.SUCCESS('User успешно импортирован!'))

        # Загрузка данных для Review
        review_file_path = os.path.join(csv_dir, 'review.csv')
        with open(review_file_path, 'r', encoding='utf-8') as review_file:
            csv_reader = csv.DictReader(review_file)
            for row in csv_reader:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                Review.objects.create(
                    title=title,
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date']
                )

        self.stdout.write(self.style.SUCCESS('Review успешно импортирован!'))

        # Загрузка данных для Comment
        comment_file_path = os.path.join(csv_dir, 'comments.csv')
        with open(comment_file_path, 'r', encoding='utf-8') as comment_file:
            csv_reader = csv.DictReader(comment_file)
            for row in csv_reader:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                Comment.objects.create(
                    review=review,
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date']
                )

        self.stdout.write(self.style.SUCCESS('Comment успешно импортирован!'))
