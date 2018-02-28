from db_bot import *


BACK_TO_START = '<< с начала'



def route_menu():
    return [
        ['471', '489']]


def depart_menu():
    return [
        ['ст.Расторгуево', 'Кинотеатр'],
        ['ПЛК', 'м. Кантемировская'],
        [BACK_TO_START]]


def direction_menu():
    return [
        ['на Москву', 'на Расторгуево'],
        [BACK_TO_START]]


def schedule_menu():
    return [
    ['Сейчас', '+1 час'],
    ['Сегодня', '+1 день'],
    [BACK_TO_START]]


regex_special_chars = r'.^$*+?{}[]\|()'

escape_dic = dict(zip(
    [ord(c) for c in regex_special_chars],
    ['\\' + c for c in regex_special_chars]))


def escape(string):
    return string.translate(escape_dic)


def flat(menu):
    for item in menu:
        if isinstance(item, list):
            yield from flat(item)
        else:
            yield item


def template_of(items):
    return '^(' + '|'.join([escape(item) for item in flat(items)]) + ')$'


def route_menu_re():
    return template_of(list(flat(route_menu())))


def depart_menu_re():
    return template_of(list(flat(depart_menu()))[:-1])


def direction_menu_re():
    return template_of(list(flat(direction_menu()))[:-1])


def schedule_menu_re():
    return template_of(list(flat(schedule_menu()))[:-1])

