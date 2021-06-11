from django.contrib.gis.geos import Point
import csv
from main.models import Airport
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        Airport.objects.all().delete()
        with open('import_data/airports.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            #skip header
            next(reader)
            rows_cnt = 0
            for row in reader:
                pnt = Point(float(row[1]), float(row[2]))
                _airport = Airport(name=row[0], point=pnt)
                _airport.save()
                rows_cnt += 1
            print("ROWS FROM CSV: {0}".format(rows_cnt))

        with connection.cursor() as cursor:

            sql_init = """
            CREATE EXTENSION pgrouting;
            DROP TABLE IF EXISTS main_airport_routes;
            CREATE TABLE main_airport_routes(
                id SERIAL,
                source BIGINT,
                target BIGINT,
                distance BIGINT
            );
            """

            cursor.execute(sql_init)

            airports = Airport.objects.all()

            for a in airports.iterator():
                print(a.name)
                sql2 = """
                INSERT INTO main_airport_routes (distance, source, target)
                SELECT
                    ROUND(ST_DistanceSphere(ST_SetSRID(ST_MakePoint({0}, {1}),4326), X.point)) AS distance,
                    {2} AS source,
                    X.id AS target
                FROM main_airport X
                WHERE X.id <> {2}
                """.format(a.point.coords[0], a.point.coords[1], a.id)
                cursor.execute(sql2)
