# Импорты
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
import re

from .forms import RegisterForm, AvatarForm
from .models import Topic, Lesson, Test, Result, Profile


def index(request):
    return render(request, 'main/index.html')


def search(request):
    query = request.GET.get('q', '').strip()

    topic_results = []
    lesson_results = []

    if query:
        words = query.split()

        # ===== ТЕМЫ =====
        topic_q = Q()
        for word in words:
            topic_q |= Q(title__icontains=word) | Q(description__icontains=word)

        topic_results = Topic.objects.filter(topic_q)

        topic_results = sorted(
            topic_results,
            key=lambda t: (
                query.lower() not in t.title.lower(),
                len(t.title)
            )
        )

        # ===== УРОКИ =====
        lesson_q = Q()
        for word in words:
            lesson_q |= Q(title__icontains=word) | Q(content__icontains=word)

        lessons = Lesson.objects.filter(lesson_q)

        lesson_results = []

        for lesson in lessons:
            content = lesson.content

            for word in words:
                pattern = re.compile(f"({word})", re.IGNORECASE)
                content = pattern.sub(r'<mark>\1</mark>', content)

            lesson.highlighted_content = content
            lesson_results.append(lesson)

        lesson_results = sorted(
            lesson_results,
            key=lambda l: (
                query.lower() not in l.title.lower(),
                len(l.title)
            )
        )

    return render(request, 'main/search.html', {
        'query': query,
        'topic_results': topic_results,
        'lesson_results': lesson_results,
    })


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})


@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        avatar_form = AvatarForm(request.POST, request.FILES, instance=profile_obj)
        if avatar_form.is_valid():
            avatar_form.save()
            return redirect('profile')
    else:
        avatar_form = AvatarForm(instance=profile_obj)

    results = Result.objects.filter(user=request.user)

    tests_passed = results.values('test').distinct().count()
    lessons_passed = results.values('test__topic').distinct().count()

    avg_score = results.aggregate(avg=Avg('score'))['avg']
    avg_score = round(avg_score, 2) if avg_score else 0

    total_tests = Test.objects.count()

    if total_tests > 0:
        progress_percent = round((tests_passed / total_tests) * 100)
    else:
        progress_percent = 0

    if tests_passed >= 10:
        level = "Продвинутый"
    elif tests_passed >= 5:
        level = "Средний"
    elif tests_passed >= 1:
        level = "Начальный"
    else:
        level = "Новичок"

    return render(request, 'main/profile.html', {
        "tests_passed": tests_passed,
        "lessons_passed": lessons_passed,
        "avg_score": avg_score,
        "level": level,
        "avatar_form": avatar_form,
        "profile_obj": profile_obj,
        "total_tests": total_tests,
        "progress_percent": progress_percent,
    })


def tests(request):
    tests = Test.objects.all()

    user_tests = []
    if request.user.is_authenticated:
        user_tests = Result.objects.filter(user=request.user).values_list('test_id', flat=True)

    return render(request, "main/tests.html", {
        "tests": tests,
        "user_tests": user_tests
    })
def about(request):
    return render(request, "main/about.html")

def learning(request):
    topics = Topic.objects.all()
    return render(request, "main/learning.html", {"topics": topics})

def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    return render(request, "main/lesson.html", {"lesson": lesson})

def test_detail(request, id):
    test = get_object_or_404(Test, id=id)
    questions = list(test.questions.prefetch_related('answers').all())

    # Для гостей показываем только первый вопрос
    if not request.user.is_authenticated:
        questions = questions[:1]

    if request.method == 'POST':
        # Гость может отправить только первый вопрос и получает предложение зарегистрироваться
        if not request.user.is_authenticated:
            score = 0
            results_data = []

            for question in questions:
                selected_answer_id = request.POST.get(f'question_{question.id}')
                correct_answer = question.answers.filter(is_correct=True).first()

                is_correct = False

                if selected_answer_id and correct_answer:
                    if str(correct_answer.id) == selected_answer_id:
                        score += 1
                        is_correct = True

                results_data.append({
                    'question': question,
                    'selected': int(selected_answer_id) if selected_answer_id else None,
                    'correct': correct_answer.id if correct_answer else None,
                    'is_correct': is_correct
                })

            return render(request, 'main/test_result.html', {
                'test': test,
                'score': score,
                'total': 1,
                'results_data': results_data,
                'guest_mode': True
            })

        # Полный тест для авторизованных
        all_questions = test.questions.prefetch_related('answers').all()
        score = 0
        results_data = []

        for question in all_questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            correct_answer = question.answers.filter(is_correct=True).first()

            is_correct = False

            if selected_answer_id and correct_answer:
                if str(correct_answer.id) == selected_answer_id:
                    score += 1
                    is_correct = True

            results_data.append({
                'question': question,
                'selected': int(selected_answer_id) if selected_answer_id else None,
                'correct': correct_answer.id if correct_answer else None,
                'is_correct': is_correct
            })

        existing_results = Result.objects.filter(user=request.user, test=test).order_by('-score', '-created_at')
        result = existing_results.first()

        if result:
            if score > result.score:
                result.score = score
                result.save()
            existing_results.exclude(id=result.id).delete()
        else:
            Result.objects.create(
                user=request.user,
                test=test,
                score=score
            )

        return render(request, 'main/test_result.html', {
            'test': test,
            'score': score,
            'total': all_questions.count(),
            'results_data': results_data,
            'guest_mode': False
        })

    return render(request, 'main/test_detail.html', {
        'test': test,
        'questions': questions,
        'guest_mode': not request.user.is_authenticated,
    })