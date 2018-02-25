from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup



def dayset(text):
    """Строит set из номеров дней из текста вида 'пвсчп__\n '
    """

    days = set()
    i = 0
    for c in text[:7]:
        i += 1
        if c != '_':
            days.add(i)

    return days


def getattr(tag, attr):
    try:
        return tag[attr][0]
    except (KeyError, TypeError):
        return ''


def scrap(url, is_return_func):

    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return

    if html is None:
        print("URL is not found")
        return

    s = html.read()
    print(s[:200])

    page = BeautifulSoup(s, "html.parser")

    # На веб-странице видим кучу табличек.
    # Сначала идут рейсы прямые, потом обратные.
    # Какую структуру мы хотим соорудить из всего набора табличек? Список рейсов.
    # Для каждого рейса хотим знать прямой он или обратный, в какие дни ходит, какие у него остановки в какое время:
    # [{'is_return': False|True, 'days': {1,2,3,4,5}, 'stops':[('Название остановки','ЧЧ:ММ'), ...]}, ...]
    # А для этого из каждой текущей таблички построим два списка:
    # days = [{1,2,3,4,5}, {6,7}, {}, ...] и
    # stops = [('Название остановки','ЧЧ:ММ'), ...], а еще
    # is_return = False|True
    # И после каждой таблички длина days и stops должна обязательно совпадать.
    # Будем ими зполнять общую структуру,
    # Но только если набор дней в данном рейсе пустой, то в финальную структуру его остановки не выводим.

    all_trips = []  # вот она, общая структура
    is_return = False

    days = []
    stops = []

    # а здесь t - это точно кусочек расписания
    for tr in page.findAll('tr'):

        if getattr(tr, 'class') == 'stops':
            if len(days) != 0:
                #print(len(days), len(stops))
                #[print(day) for day in days]
                #[print(stop) for stop in stops]
                #print('-------------------------------------------------------------------------')
                for i in range(len(days)):
                    if bool(days[i]):
                        route = []
                        for j in range(len(stops)):
                            stop = stops[j][i]
                            time = stop[1]
                            if time != '':
                                route.append(stop)
                        all_trips.append({
                            'is_return': is_return_func(stops[0][0][0]),
                            'days': days[i],
                            'stops': route,
                        })

            days = []
            stops = []

            # из этого будем строить days
            for d in tr.children:
                days.append(dayset(d.text))

        elif getattr(tr.td, 'class') == 'stops':
            stop = tr.td.text.strip()
            if stop[0] == '\ufeff':
                stop = stop[1:]
            last = []
            for td in tr.findAll('td', {'class', 'time'}):
                if getattr(td, 'class') == 'time':
                    last.append((stop, td.text.strip()))
            stops.append(last)

    #print(len(days), len(stops))
    #[print(day) for day in days]
    #[print(stop) for stop in stops]
    #print('-------------------------------------------------------------------------')
    for i in range(len(days)):
        if bool(days[i]):
            route = []
            for j in range(len(stops)):
                stop = stops[j][i]
                time = stop[1]
                if time != '':
                    route.append(stop)
            all_trips.append({
                'is_return': is_return_func(stops[0][0][0]),
                'days': days[i],
                'stops': route,
            })

    [print(trip) for trip in all_trips]
    return all_trips




