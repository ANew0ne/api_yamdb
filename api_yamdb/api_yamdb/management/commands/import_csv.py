# import os
# import csv
# from django.core.management.base import BaseCommand
# from api.models import Category, Title, Genre
# from reviews.models import Review, Comment
# from users.models import User

# class Command(BaseCommand):
#     help = 'Импорт CSV-файлов в базу данных'

#     def handle(self, *args, **options):
#         csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/data')

#         # Загрузка данных для Category
#         category_file_path = os.path.join(csv_dir, 'category.csv')
#         with open(category_file_path, 'r') as category_file:
#             csv_reader = csv.DictReader(category_file)
#             for row in csv_reader:
#                 Category.objects.create(name=row['name'], slug=row['slug'])

#         self.stdout.write(self.style.SUCCESS('Category успешно импортирован!'))

#         # Загрузка данных для Genre
#         genre_file_path = os.path.join(csv_dir, 'genre.csv')
#         with open(genre_file_path, 'r') as genre_file:
#             csv_reader = csv.DictReader(genre_file)
#             for row in csv_reader:
#                 Genre.objects.create(name=row['name'], slug=row['slug'])

#         self.stdout.write(self.style.SUCCESS('Genre успешно импортирован!'))

#         # Загрузка данных для Title
#         title_file_path = os.path.join(csv_dir, 'titles.csv')
#         with open(title_file_path, 'r') as title_file:
#             csv_reader = csv.DictReader(title_file)
#             for row in csv_reader:
#                 category = Category.objects.get(name=row['category_name'])
#                 title = Title.objects.create(
#                     name=row['name'],
#                     year=row['year'],
#                     description=row['description'],
#                     category=category
#                 )
#                 genre_names = row['genre_name'].split(', ')
#                 for genre_name in genre_names:
#                     genre = Genre.objects.get(name=genre_name)
#                     title.genre.add(genre)

#         self.stdout.write(self.style.SUCCESS('Title успешно импортирован!'))

#         # Обработка связей между Genre и Title
#         genre_title_file_path = os.path.join(csv_dir, 'genre_title.csv')
#         with open(genre_title_file_path, 'r') as genre_title_file:
#             csv_reader = csv.DictReader(genre_title_file)
#             for row in csv_reader:
#                 title_name = row['title_name']
#                 genre_name = row['genre_name']

#                 title = Title.objects.get(name=title_name)
#                 genre = Genre.objects.get(name=genre_name)

#                 title.genre.add(genre)

#         self.stdout.write(self.style.SUCCESS('GenreTitle успешно импортирован'))

#         # Загрузка данных для Review
#         review_file_path = os.path.join(csv_dir, 'review.csv')
#         with open(review_file_path, 'r') as review_file:
#             csv_reader = csv.DictReader(review_file)
#             for row in csv_reader:
#                 title = Title.objects.get(name=row['title'])
#                 author = User.objects.get(username=row['author'])
#                 Review.objects.create(
#                     title=title,
#                     text=row['text'],
#                     author=author,
#                     score=row['score'],
#                     pub_date=row['pub_date']
#                 )

#         self.stdout.write(self.style.SUCCESS('Review успешно импортирован!'))

#         # Загрузка данных для Comment
#         comment_file_path = os.path.join(csv_dir, 'comments.csv')
#         with open(comment_file_path, 'r') as comment_file:
#             csv_reader = csv.DictReader(comment_file)
#             for row in csv_reader:
#                 review = Review.objects.get(text=row['review'])
#                 author = User.objects.get(username=row['author'])
#                 Comment.objects.create(
#                     review=review,
#                     text=row['text'],
#                     author=author,
#                     pub_date=row['pub_date']
#                 )

#         self.stdout.write(self.style.SUCCESS('Comment успешно импортирован!'))
