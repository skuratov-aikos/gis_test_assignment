Demo reels:

https://youtu.be/zRDiP30vzZo
https://youtu.be/LNFVq_CniWo

Test assignment, created by Skuratov Alexander

1) Clone repository
2) Run docker-compose up
3) Run docker-compose exec web python manage.py migrate
4) Run docker-compose exec web python manage.py gis_init (takes about 5-10 min. to run on average PC, about 6 mil. rows of complete graph generation)
5) Open localhost:8000 in browser

Used stack:
pgsql, postgis, pgrouting, django, DRF, react, docker, python3

Enchancement proposals:
- Path finding optimization
- Indexes to improve pgr_dejkstra(...) perfomance
- Redundant reverse edges insertions?