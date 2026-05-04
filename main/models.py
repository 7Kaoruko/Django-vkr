# Импорты
from django.db import models
from django.contrib.auth.models import User


# Модель темы (категория обучения)
class Topic(models.Model):
    # Название темы (например: "Криптография")
    title = models.CharField(max_length=200, verbose_name='Название темы')

    # Краткое описание темы
    description = models.TextField(verbose_name='Краткое описание')

    def __str__(self):
        # Как объект будет отображаться в админке
        return self.title


# Модель урока (теория)
class Lesson(models.Model):
    # Связь с темой (одна тема → много уроков)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Тема'
    )

    # Название урока
    title = models.CharField(max_length=200, verbose_name='Название урока')

    # Основной текст теории
    content = models.TextField(verbose_name='Теория')

    def __str__(self):
        return self.title


# Модель теста
class Test(models.Model):
    # Связь с темой (одна тема → один или несколько тестов)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Тема'
    )

    # Название теста
    title = models.CharField(max_length=200, verbose_name='Название теста')

    def __str__(self):
        return self.title



# Модель вопроса
class Question(models.Model):
    # Связь с тестом (один тест → много вопросов)
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест'
    )

    # Текст вопроса
    text = models.TextField(verbose_name='Текст вопроса')

    def __str__(self):
        # Ограничиваем вывод, чтобы не было слишком длинного текста
        return self.text[:50]



# Модель ответа
class Answer(models.Model):
    # Связь с вопросом (один вопрос → много ответов)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )

    # Текст варианта ответа
    text = models.CharField(max_length=255, verbose_name='Вариант ответа')

    # Является ли ответ правильным
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return self.text


# Модель результата теста
class Result(models.Model):
    # Пользователь, который прошёл тест
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Пользователь'
    )
    # Тест, который был пройден
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Тест'
    )
    # Количество набранных баллов
    score = models.IntegerField(verbose_name='Количество баллов')
    # Дата прохождения теста
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {self.score}'


# Модель профиля пользователя
class Profile(models.Model):
    # Связь один к одному с пользователем
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    # Аватар пользователя
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    def __str__(self):
        return f'Профиль: {self.user.username}'