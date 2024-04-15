from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Appointment
from django.utils import timezone
from datetime import datetime, timedelta, time, date


# Прототип базы данных мастеров
master_data = {
    'nogotok': {'id': 1, 'title_name': 'Андрей Иванович', 'title_prof': 'Мастер по ноготочкам', 'photo': 'Link/images/1.jpg', 'password': '123', 'login':'nogotok'},
    'mmm': {'id': 2, 'title_name': 'Анастасия Кулич', 'title_prof': 'Мастер по массажу', 'photo': 'Link/images/2.jpg', 'password': '123', 'login':'mmm'},
    'fit': {'id': 3, 'title_name': 'Мила Йолович', 'title_prof': 'Мастер по фитнесу', 'photo': 'Link/images/3.jpg', 'password': '123', 'login':'fit'},
}

# Прототип базы данных услуг мастеров
master_data_pro = {
    'nogotok': {'usl_1': 'Наращивание ногтей', 'cen_1': '2000', 'time_1': '2', 'usl_2': 'Коррекция формы', 'cen_2': '500', 'time_2': '1', 'usl_3': 'Гель-лак', 'cen_3': '1500', 'time_3': '1'},
    'mmm': {'usl_1': 'Классический массаж', 'cen_1': '2000', 'time_1': '1', 'usl_2': 'Релакс массаж', 'cen_2': '2500', 'time_2': '1', 'usl_3': 'Оздоровительный массаж', 'cen_3': '3000', 'time_3': '1'},
    'fit': {'usl_1': 'Функциональная тренировка', 'cen_1': '1000', 'time_1': '1','usl_2': 'Кардио тренировка', 'cen_2': '1000', 'time_2': '1', 'usl_3': 'Растяжка', 'cen_3': '1500', 'time_3': '1'},
}


# Визуализация страницы списка мастеров
def master_list(request):
    return render(request, 'Link/master_list.html', {'masters': master_data.values()})



# Визуализация страницы с услугами выбранного мастера
def link (request, user_id): #Страница с услугами
    data_people = master_data.get(user_id)
    data_pro = master_data_pro.get(user_id)
    today_date = date.today().strftime('%Y-%m-%d')

    data_1 = {
            'data': data_people,
            'data_pro': data_pro,
            'user_id': user_id,
            'today_date': today_date,
            }  # title - это ключ (передаваемый параметр) : Значение параметра
    return render(request, 'Link/link.html', context=data_1)


def book (request):
    appointments = Appointment.objects.all()
    return render(request, 'Link/book.html', {'appointments': appointments})


def book_appointment(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        full_time = int(request.POST['full_time'])
        date = request.POST['date']
        start_time = request.POST['start_time']

        # Преобразование выбранного времени начала в объект времени
        selected_time = datetime.strptime(start_time, '%H:%M')

        # Вычисление времени окончания
        end_time = (selected_time + timedelta(hours=full_time)).strftime('%H:%M')

        # Проверка доступности времени
        if not is_time_available(date, start_time, end_time):
            return render(request, 'Link/error.html',
                          {'message': 'Этот временной интервал недоступен. Пожалуйста, выберите другое время.'})

        # Создание записи о приеме и сохранение в базе данных
        appointment = Appointment(user_id=user_id, full_time=full_time, date=date, start_time=start_time,
                                  end_time=end_time)
        appointment.save()

        # Перенаправление на главную страницу или другую страницу
        return redirect('book')
    else:
        return render(request, 'Link/calendar.html')


@csrf_protect
def calendar(request):
    today_date = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # Получаем значения выбранных чекбоксов из POST-запроса и сохраняем их в переменные
        selected_service_1 = request.POST.get('selected_services_1', None)
        time_value_1 = int(request.POST.get('time_value_1', 0))

        selected_service_2 = request.POST.get('selected_services_2', None)
        time_value_2 = int(request.POST.get('time_value_2', 0))

        selected_service_3 = request.POST.get('selected_services_3', None)
        time_value_3 = int(request.POST.get('time_value_3', 0))

        full_time = int(request.POST.get('full_time', 0)) or (time_value_1 + time_value_2 + time_value_3)

        # Загружаем записи о приемах с учетом фильтрации по user_id и выбранной дате
        selected_date = request.POST['date']
        appointments = Appointment.objects.filter(user_id=request.POST.get('user_id'), date=selected_date)

        available_times = get_available_times(selected_date, appointments)
        user_id = request.POST.get('user_id')

        print("user_id:", user_id)
        print("full_time:", full_time)
        print('Пост запрос 2ур')
        return render(request, 'Link/calendar.html',
                      {'selected_date': selected_date, 'appointments': appointments, 'available_times': available_times, 'user_id': user_id, 'full_time': full_time})
    else:
        selected_date = today_date
        user_id = 'Test'
        full_time = 1

        print("user_id:", user_id)
        print("full_time:", full_time)
        print('Без пост Запроса')
        return render(request, 'Link/calendar.html',
                      {'selected_date': selected_date, 'user_id': user_id, 'full_time': full_time})


def is_time_available(date, start_time, end_time):
    # Здесь возможно расширение логики для будущих задач
    return True  # Заглушка, всегда возвращает True для пример



def load_appointments(date):
    # Загружаем все записи о приемах для выбранной даты
    appointments = Appointment.objects.filter(date=date)
    return appointments


def get_available_times(date, appointments):
    # Создаем список всех возможных временных интервалов
    all_times = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']

    # Получаем занятые временные интервалы
    occupied_intervals = [(appointment.start_time, appointment.end_time) for appointment in appointments]

    # Исключаем из всех временных интервалов занятые интервалы
    available_times = []

    for time_slot in all_times:
        # Парсим время из строки
        hour, minute = map(int, time_slot.split(':'))
        start_time = time(hour, minute)

        # Проверяем, пересекается ли интервал с занятыми интервалами
        is_available = True
        for occupied_interval in occupied_intervals:
            occupied_start_time = occupied_interval[0]
            occupied_end_time = occupied_interval[1]

            if start_time >= occupied_start_time and start_time < occupied_end_time:
                is_available = False
                break

        if is_available:
            available_times.append(time_slot)

    return available_times


def get_available_intervals(appointments):
    # Получаем все занятые временные интервалы
    occupied_intervals = [(appointment.start_time, appointment.end_time) for appointment in appointments]

    # Создаем список доступных временных интервалов
    available_intervals = []

    # Проверяем доступные интервалы между занятыми интервалами
    for i in range(len(occupied_intervals) - 1):
        end_time_current = occupied_intervals[i][1]
        start_time_next = occupied_intervals[i + 1][0]
        available_intervals.append((end_time_current, start_time_next))

    return available_intervals



def get_booked_times(date):
    # Получаем все записи о приемах для выбранной даты
    appointments = Appointment.objects.filter(date=date)
    booked_times = []

    # Проходимся по каждой записи о приеме и добавляем временные слоты в список
    for appointment in appointments:
        booked_times.append(appointment.start_time)

    return booked_times




def page_not_found (request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')





# В перспективе
def add_page (request):
    return HttpResponse("<h1>Добавление статьи или страницы</h1>")

def contact (request):
    return HttpResponse("<h1>Контакты, обратная связь</h1>")

def login (request):
    return HttpResponse("<h1>Вход в учетную запись</h1>")


# Прототипирование
# def start (request):
#     data = {'title' : 'Главная страница',
#             'menu' : menu,
#             'posts' : data_bd,
#
#             } #title - это ключ (передаваемый параметр) : Значение параметра
#     with open('data_1.json', 'w', encoding='utf-8') as f:
#         # Записываем список в JSON файл
#         json.dump(data_bd, f, ensure_ascii=False)
#
#     return render(request, 'Link/start.html', context=data)