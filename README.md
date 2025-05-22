# Django Tree Menu App
Django-приложение для построения древовидного меню, реализованное с использованием стандартных возможностей Django (template tag, ORM, admin). Предназначено для встраивания в любые Django-проекты.

## Возможности
- Меню хранится в базе данных и редактируется через Django admin
- Отрисовка меню осуществляется через template tag:
```bash
{% draw_menu 'main_menu' %}
```
- Поддержка нескольких меню на одной странице (по имени)
- Автоматическое определение активного пункта по request.path
- Развёртывание всех родительских узлов активного пункта + одного уровня вложенности после него
- Переходы по пунктам через явные URL (/about/) или named URL (reverse('about'))
- Отрисовка всего меню за один SQL-запрос
- Гарантирована защита от циклических связей в модели
- Чистый HTML без внешних JS/CSS библиотек

## Установка и запуск
1. Склонируйте репозиторий:

```bash
git clone https://github.com/yourusername/django-tree-menu.git
cd django-tree-menu
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Примените миграции:

```bash
python manage.py migrate
```
4. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```
5. Запустите сервер:

```bash
python manage.py runserver
```

6. Зайдите в админку:
http://localhost:8000/admin/
и создайте меню и пункты меню.

## Пример использования в шаблоне
```bash
{% load menu_tags %}
<!DOCTYPE html>
<html>
<head><title>Меню</title></head>
<body>
  {% draw_menu 'main_menu' %}
</body>
</html>
```
## Требования
Django 3.2+
Python 3.7+

## Структура
menu/ — Django app с моделями Menu и MenuItem

templatetags/menu_tags.py — реализация draw_menu

templates/menu/ — шаблоны отрисовки меню (рекурсивно)
