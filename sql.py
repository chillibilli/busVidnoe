drop_all = [
    "DROP TABLE IF EXISTS chat;",
    "DROP TABLE IF EXISTS direction_path;",
    "DROP TABLE IF EXISTS major_stops;",
    "DROP TABLE IF EXISTS stoptime;",
    "DROP TABLE IF EXISTS trip_day;",
    "DROP INDEX IF EXISTS busstop_name;",
    "DROP TABLE IF EXISTS busstop;",
    "DROP TABLE IF EXISTS trip;",
    "DROP TABLE IF EXISTS direction;",
    "DROP TABLE IF EXISTS route;",
    "DROP TABLE IF EXISTS weekday;"
]

create_all = [
    """CREATE TABLE weekday (
        weekday_id integer PRIMARY KEY,
        weekday_name varchar,
        weekday_short_name varchar
    );
    """,

    """CREATE TABLE route (
        route_id integer PRIMARY KEY,
        route_number varchar UNIQUE,
        route_name varchar,
        order_num integer,
        url varchar UNIQUE
    );
    """,


    """CREATE TABLE direction (
        direction_id integer PRIMARY KEY,
        direction_name varchar,
        is_return integer,
        route_id integer REFERENCES route(route_id),
        order_num integer
    );
    """,

    """CREATE TABLE trip (
        trip_id integer PRIMARY KEY,
        is_return integer,
        route_id integer REFERENCES route(route_id),
        direction_id integer REFERENCES direction(direction_id)
    );
    """,

    """CREATE TABLE busstop (
        busstop_id integer PRIMARY KEY,
        busstop_name varchar UNIQUE
    );
    """,

    """CREATE UNIQUE INDEX busstop_name ON busstop(busstop_name);
    """,

    """CREATE TABLE trip_day (
        trip_id integer REFERENCES trip(trip_id),
        weekday_id integer REFERENCES weekday(weekday_id)
    );
    """,

    """CREATE TABLE stoptime (
        trip_id integer REFERENCES trip(trip_id),
        busstop_id integer REFERENCES busstop(busstop_id),
        hh integer,
        mm integer
    );
    """,

    """CREATE TABLE major_stops (
        major_stop_id integer PRIMARY KEY,
        route_id integer REFERENCES route(route_id),
        busstop_id integer REFERENCES busstop(busstop_id),
        order_num integer
    );
    """,

    """CREATE TABLE direction_path (
        major_stop_id integer REFERENCES major_stops(major_stop_id),
        direction_id integer REFERENCES direction(direction_id)
    );
    """,

]

weekdays_data = [
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (1,'Понедельник','Пн');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (2,'Вторник','Вт');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (3,'Среда','Ср');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (4,'Четверг','Чт');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (5,'Пятница','Пт');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (6,'Суббота','Сб');",
    "INSERT INTO weekday (weekday_id, weekday_name, weekday_short_name) VALUES (7,'Воскресенье','Вс');",
]
