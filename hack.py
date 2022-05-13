import random
from datacenter.models import (Lesson, Chastisement, Schoolkid,
                               Mark, Commendation, Subject)


PRISE_LIST = (
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!'
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!')


def get_schoolkid_by_name(schoolkid_name):
    return Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for current_mark in bad_marks:
        current_mark.points = 5
        current_mark.save()


def delete_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('-date').first()
    Commendation.objects.create(
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
        created=lesson.date,
        text=random.choice(PRISE_LIST)
    )


def hack_diary(child_name, subject_title):
    try:
        schoolkid = get_schoolkid_by_name(child_name)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с указанным именем.')
        return
    except Schoolkid.DoesNotExist:
        print('Не найден ученик с указанным именем.')
        return

    try:
        subject = Subject.objects.filter(
            title__contains=subject_title,
            year_of_study=schoolkid.year_of_study
        ).get()
    except Subject.MultipleObjectsReturned:
        print('Найдено несколько предметов с указанным названием.')
        return
    except Subject.DoesNotExist:
        print('Не найден предмет с указанным названием.')
        return

    fix_marks(schoolkid)
    delete_chastisements(schoolkid)
    create_commendation(schoolkid, subject)
