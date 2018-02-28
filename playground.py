from db_bot import DbBotHelper
from db_scrap import DbScrapHelper

db = DbBotHelper()

print(db.get_all_routes())

route_id = 2

print(db.get_major_stops(route_id))

major_stop_id = 10
busstop_id = 26

# обратные рейсы привязать к направлению "на Расторгуево" или "на ул.Завидная"
#db1 = DbScrapHelper()
#route_id = 2
#busstop_id = db1.find_busstop(db1.conn.cursor(), 'ул.Завидная, д.24')
#print('ул.Завидная, д.24 busstop_id =', busstop_id)
#print(list(db1.exec("SELECT * FROM trip WHERE trip.route_id = ? and trip.is_return = 1 and trip.trip_id in "
#            "(select trip_id from stoptime where stoptime.trip_id = trip.trip_id and stoptime.busstop_id = ?);",
#        (route_id, busstop_id))))
#
#busstop_id = db1.find_busstop(db1.conn.cursor(), 'ст.Расторгуево')
#print('ст.Расторгуево busstop_id =', busstop_id)
#print(list(db1.exec("SELECT * FROM trip WHERE trip.route_id = ? and trip.is_return = 1 and trip.trip_id in "
#            "(select trip_id from stoptime where stoptime.trip_id = trip.trip_id and stoptime.busstop_id = ?);",
#        (route_id, busstop_id))))

print(db.get_directions(major_stop_id))

direction_id = 3
weekday_id = 7

print(db.get_day_schedule(busstop_id, weekday_id, direction_id))

print(db.get_hour_schedule(busstop_id, weekday_id, direction_id, 6 * 60 + 00, 7 * 60 + 00))