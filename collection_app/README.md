# mtg-django-collection-manager
Django to manage MTG Collection

 * A little bit of webscrapping with requests and beautiful soup
 * Usage of external API for form validation


# Troubleshooting

If the following error appears:

```commandline
django.db.utils.ProgrammingError: relation "collection_app_card" does not exist
LINE 1: SELECT COUNT(*) AS "__count" FROM "collection_app_card"
```

run the initial migration again

```commandline
./manage.py sqlmigrate collection_app 0001_initial
```
