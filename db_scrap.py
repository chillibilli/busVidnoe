from sql import *
import sqlite3


class DbScrapHelper:

    def __init__(self):
        self.db_file = 'mostrans.db'
        self.conn = sqlite3.connect(self.db_file)
        self.route_id = 0
        self.trip_id = 0
        self.busstop_id = 0
        self.major_stop_id = 0

    def exec(self, statement, params=()):
        c = self.conn.cursor()
        rows = []
        try:
            rows = c.execute(statement, params)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(statement)
            print(e)
        return rows

    def recreate(self):
        c = self.conn.cursor()
        statement = ''

        try:

            for statement in drop_all:
                c.execute(statement)
            self.conn.commit()

            for statement in create_all:
                c.execute(statement)
            self.conn.commit()

            for statement in weekdays_data:
                c.execute(statement)
            self.conn.commit()

            for row in c.execute('SELECT * FROM weekday ORDER BY weekday_id'):
                    print(row)

        except sqlite3.OperationalError as e:
            print(statement)
            print(e)

        self.conn.commit()

    def insert_route(self, c, route_number, route_name, order_num, url):
        statement = "INSERT INTO route (route_id, route_number, route_name, order_num, url) VALUES (?, ?, ?, ?, ?);"
        self.route_id += 1
        c.execute(statement, (self.route_id, route_number, route_name, order_num, url))
        return self.route_id

    def insert_trip(self, c, is_return, route_id):
        statement = "INSERT INTO trip (trip_id, is_return, route_id) VALUES (?, ?, ?);"
        self.trip_id += 1
        c.execute(statement, (self.trip_id, is_return, route_id))
        return self.trip_id

    def insert_busstop(self, c, busstop_name):
        statement = "INSERT INTO busstop (busstop_id, busstop_name) VALUES (?, ?);"
        self.busstop_id += 1
        c.execute(statement, (self.busstop_id, busstop_name))
        return self.busstop_id

    def insert_trip_day(self, c, trip_id, weekday_id):
        statement = "INSERT INTO trip_day (trip_id, weekday_id) VALUES (?, ?);"
        c.execute(statement, (trip_id, weekday_id))

    def insert_stoptime(self, c, trip_id, busstop_id, hh, mm):
        statement = "INSERT INTO stoptime (trip_id, busstop_id, hh, mm) VALUES (?, ?, ?, ?);"
        c.execute(statement, (trip_id, busstop_id, hh, mm))

    def find_busstop(self, c, busstop_name):
        statement = "SELECT busstop_id FROM busstop WHERE busstop_name = ?"
        row = c.execute(statement, (busstop_name,)).fetchone()
        return None if row is None else row[0]

    def insert_major_stop(self, busstop_name, route_id, directions_from_here, order_num):
        c = self.conn.cursor()
        busstop_id = self.find_busstop(c, busstop_name)
        if busstop_id is None:
            return False

        self.major_stop_id += 1
        c.execute("INSERT INTO major_stops (major_stop_id, route_id, busstop_id, order_num) VALUES (?, ?, ?, ?);",
            (self.major_stop_id, route_id, busstop_id, order_num))

        for direction_id in directions_from_here:
            c.execute("INSERT INTO direction_path (major_stop_id, direction_id) VALUES (?, ?);",
                    (self.major_stop_id, direction_id))

        self.conn.commit()
        return True

    def save(self, all_trips, route_number, route_name, order_num, url):
        c = self.conn.cursor()

        route_id = self.insert_route(c, route_number, route_name, order_num, url)

        for trip in all_trips:
            trip_id = self.insert_trip(c, trip['is_return'], route_id)
            for day in trip['days']:
                self.insert_trip_day(c, trip_id, day)
            for stop in trip['stops']:
                busstop_name = stop[0]
                hhmm = stop[1]
                hour = int(hhmm[:2])
                min = int(hhmm[3:])
                busstop_id = self.find_busstop(c, busstop_name)
                if busstop_id is None:
                    busstop_id = self.insert_busstop(c, busstop_name)
                self.insert_stoptime(c, trip_id, busstop_id, hour, min)
            self.conn.commit()

        return route_id
