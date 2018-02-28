import sqlite3

class DbBotHelper:

    def __init__(self):
        self.__db_file = 'mostrans.db'

    def query(self, statement, params=()):
        rows = []
        conn = None
        try:
            conn = sqlite3.connect(self.__db_file)
            c = conn.cursor()
            q = c.execute(statement, params)
            rows = q.fetchall()
        except sqlite3.OperationalError as e:
            print(statement)
            print(e)
        finally:
            conn.close()
        return rows


    def get_all_routes(self):
        return self.query('SELECT route_id, route_number '
                          'FROM route '
                          'ORDER BY route_id;')

    def get_major_stops(self, route_id):
        return self.query('SELECT major_stop_id, route_id, major_stops.busstop_id, busstop_name, order_num '
                          'FROM major_stops, busstop '
                          'WHERE route_id = ? and major_stops.busstop_id = busstop.busstop_id '
                          'ORDER BY order_num;',
                          (route_id, ))

    def get_directions(self, major_stop_id):
        return self.query('SELECT direction.direction_id, direction_name, is_return, route_id, order_num '
                          'FROM direction_path, direction '
                          'WHERE major_stop_id = ? and direction_path.direction_id = direction.direction_id '
                          'ORDER BY order_num;',
                          (major_stop_id, ))

    def get_day_schedule(self, busstop_id, weekday_id, direction_id):
        return self.query('SELECT hh, mm '
                          'FROM trip, trip_day, stoptime '
                          'WHERE '
                          'stoptime.trip_id = trip.trip_id and '
                          'trip.trip_id = trip_day.trip_id and '
                          'stoptime.busstop_id = ? and '
                          'trip_day.weekday_id = ? and '
                          'trip.direction_id = ? '
                          'ORDER BY hh, mm',
                          (busstop_id, weekday_id, direction_id))

    def get_hour_schedule(self, busstop_id, weekday_id, direction_id, min_of_day_1, min_of_day_2):
        return self.query('SELECT hh, mm '
                          'FROM trip, trip_day, stoptime '
                          'WHERE '
                          'stoptime.trip_id = trip.trip_id and '
                          'trip.trip_id = trip_day.trip_id and '
                          'stoptime.busstop_id = ? and '
                          'trip_day.weekday_id = ? and '
                          'trip.direction_id = ? and '
                          'hh * 60 + mm between ? and ? '
                          'ORDER BY hh, mm',
                          (busstop_id, weekday_id, direction_id, min_of_day_1, min_of_day_2))

