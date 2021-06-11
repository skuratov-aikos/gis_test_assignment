from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from main.models import Airport
from rest_framework import viewsets
from main.serializers import AirportSerializer
from rest_framework.response import Response
from django.db import connection

def index(request):
    context = {'test': 'test_data'}
    return render(request, 'main/index.html', context)

#https://www.compose.com/articles/geofile-getting-started-with-pgrouting/


class AirportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Airport
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirportNearestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Airport
    queryset = Airport.objects.all()[:1]
    serializer_class = AirportSerializer

    def list(self, request):
        nearest_airport = self.request.query_params.get('nearest_airport', '')
        nearest_radius = self.request.query_params.get('nearest_radius', 0)
        sql = """
        SELECT id,name,point::bytea
        FROM "main_airport"
        WHERE ST_DistanceSphere(point, (SELECT point FROM "main_airport" WHERE name='{0}')) <= {1}
        """.format(nearest_airport, float(nearest_radius) * 1000)
        #first arg is
        self.queryset = self.model.objects.raw(sql)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class AirportPathViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Airport
    queryset = Airport.objects.all()[:1]
    serializer_class = AirportSerializer

    #!!!
    #https://www.compose.com/articles/geofile-getting-started-with-pgrouting/


    def list(self, request):
        start_airport = self.request.query_params.get('start_airport', '')
        end_airport = self.request.query_params.get('end_airport', '')
        max_distance = self.request.query_params.get('max_distance', 0)
        sql = """
        SELECT  
            c.id, c.name, c.point::bytea
        FROM  
            pgr_dijkstra(
                'SELECT id, source, target, distance AS cost FROM main_airport_routes WHERE distance < {2}'::text,
                (SELECT id FROM main_airport WHERE name = '{0}'), 
                (SELECT id FROM main_airport WHERE name = '{1}'), 
                FALSE
            ) AS p
            LEFT JOIN main_airport_routes AS r ON p.edge = r.id
            LEFT JOIN main_airport AS c ON p.node = c.id
        ORDER BY  
            p.seq;
        """.format(start_airport, end_airport, int(max_distance) * 1000)
        #first arg is
        self.queryset = self.model.objects.raw(sql)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)