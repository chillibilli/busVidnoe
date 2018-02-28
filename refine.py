

def refine_489(db, route_id):
    # добавить два направления
    db.exec("INSERT INTO direction (direction_id, direction_name, is_return, route_id, order_num) VALUES (1, 'на Москву', 0, ?, 1);", (route_id,))
    db.exec("INSERT INTO direction (direction_id, direction_name, is_return, route_id, order_num) VALUES (2, 'на Расторгуево', 1, ?, 2);", (route_id,))

    # все прямые рейсы привязать к направлению "на Москву",
    # а все обратные рейсы - к направлению "на Расторгуево"
    db.exec("UPDATE trip SET direction_id = 1 WHERE route_id = ? and is_return = 0;", (route_id,))
    db.exec("UPDATE trip SET direction_id = 2 WHERE route_id = ? and is_return = 1;", (route_id,))

    # перечислить главные остановки маршрута, привязать к направлениям
    db.insert_major_stop('ст.Расторгуево',    route_id, order_num=1, directions_from_here=[1], )
    db.insert_major_stop('Кинотеатр',         route_id, order_num=2, directions_from_here=[1, 2])
    db.insert_major_stop('ПЛК',               route_id, order_num=3, directions_from_here=[1, 2])
    db.insert_major_stop('Загорье',           route_id, order_num=4, directions_from_here=[1, 2])
    db.insert_major_stop('м. Кантемировская', route_id, order_num=5, directions_from_here=[2])


def refine_471(db, route_id):
    # добавить ТРИ направления
    db.exec("INSERT INTO direction (direction_id, direction_name, is_return, route_id, order_num) VALUES (3, 'на Москву', 0, ?, 1);", (route_id,))
    db.exec("INSERT INTO direction (direction_id, direction_name, is_return, route_id, order_num) VALUES (4, 'на ул.Завидная', 1, ?, 2);", (route_id,))
    db.exec("INSERT INTO direction (direction_id, direction_name, is_return, route_id, order_num) VALUES (5, 'на Расторгуево', 1, ?, 3);", (route_id,))

    # все прямые рейсы привязать к направлению "на Москву"
    db.exec("UPDATE trip SET direction_id = 3 WHERE route_id = ? and is_return = 0;", (route_id,))

    # обратные рейсы привязать к направлению "на Расторгуево" или "на ул.Завидная"
    busstop_id = db.find_busstop(db.conn.cursor(), 'ул.Завидная, д.24')
    db.exec("UPDATE trip SET direction_id = 4 WHERE trip.route_id = ? and trip.is_return = 1 and trip.trip_id in "
            "(select trip_id from stoptime where stoptime.trip_id = trip.trip_id and stoptime.busstop_id = ?);", (route_id, busstop_id))

    busstop_id = db.find_busstop(db.conn.cursor(), 'ст.Расторгуево')
    db.exec("UPDATE trip SET direction_id = 5 WHERE trip.route_id = ? and trip.is_return = 1 and trip.trip_id in "
            "(select trip_id from stoptime where stoptime.trip_id = trip.trip_id and stoptime.busstop_id = ?);", (route_id, busstop_id))

    # Переименовать "Каширское шоссе" в "Вегас"
    db.exec("UPDATE busstop SET busstop_name = 'Вегас' WHERE busstop_name = 'Каширское шоссе' ;")

    # перечислить главные остановки маршрута, привязать к направлениям
    db.insert_major_stop('ст.Расторгуево',    route_id, order_num=1, directions_from_here=[3], )
    db.insert_major_stop('Кинотеатр',         route_id, order_num=2, directions_from_here=[3, 5])
    db.insert_major_stop('ПЛК',               route_id, order_num=3, directions_from_here=[3, 4, 5])
    db.insert_major_stop('ул.Завидная, д.24', route_id, order_num=4, directions_from_here=[3, 4])
    db.insert_major_stop('Вегас',             route_id, order_num=5, directions_from_here=[3, 4, 5])
    db.insert_major_stop('м. Домодедовская',  route_id, order_num=6, directions_from_here=[4, 5])
