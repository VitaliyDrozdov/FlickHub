import csv
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = (
        'import csv to our database: use PATH and MODEL_NAME,'
        'request example: '
        'python3 manage.py import_csv -p static/data/category.csv -m category'
    )

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str,
                            help='path to file')
        parser.add_argument('-m', '--model_name', type=str,
                            help='name of our model')

    def handle(self, *args, **options):
        path = options['path']
        model = apps.get_model(app_label='reviews',
                               model_name=options['model_name'])
        with open(path, 'r', encoding='utf-8') as imported_csv:
            reader = csv.reader(imported_csv)
            header = next(reader)
            for row in reader:
                object_dict = {key: value for key, value in zip(header, row)}
                model.objects.create(**object_dict)
