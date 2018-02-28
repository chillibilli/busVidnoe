from db_scrap import DbScrapHelper


def view(query):
    db = DbScrapHelper()
    rows = db.exec(query)
    for row in rows:
        print(row)


view('SELECT * FROM weekday ORDER BY weekday_id')

view('SELECT * FROM route ORDER BY route_id;')

view('SELECT count(*) FROM trip')

view('SELECT * FROM busstop ORDER BY busstop_id')

view('SELECT count(*) FROM trip_day')

view('SELECT count(*) FROM stoptime')

view('SELECT * FROM major_stops ORDER BY route_id, order_num')

view('SELECT * FROM direction_path')

view('SELECT * FROM busstop, stoptime WHERE busstop.busstop_id = stoptime.busstop_id and stoptime.busstop_id = 4 and hh = 7  ORDER BY hh, mm')

view('SELECT * FROM direction')
