from db import *
from scrap import *
from refine import *

db = DB()

db.recreate()

# 489
url = "http://mostransavto.ru/passengers/routes/raspisaniya/?page=rasp&code=-7456630&ak=3&n=489&com="
all_trips = scrap(url, lambda x: x  != 'ст.Расторгуево')
route_id = db.save(all_trips, '489', 'Видное (ст. Расторгуево) – Москва (м. Кантемировская)', 1, url)
refine_489(db, route_id)


# 471
url = "http://mostransavto.ru/passengers/routes/raspisaniya/?page=rasp&code=-7456766&ak=3&n=471&com="
all_trips = scrap(url, lambda x: x  == 'м. Домодедовская')
route_id = db.save(all_trips, '471', 'Видное – Москва (м. Домодедовская)', 2, url)
refine_471(db, route_id)
