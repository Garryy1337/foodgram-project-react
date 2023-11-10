import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузка данных из csv файла в модель Ingredient"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="Путь к файлу")

    def handle(self, *args, **options):
        print("Ожидайте, загрузка...")
        file_name = "ingredients.csv"
        file_path = os.path.join(options["path"], file_name)

        ingredients_to_create = []

        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                name_csv = 0
                measurement_unit_csv = 1

                try:
                    ingredient = Ingredient(
                        name=row[name_csv],
                        measurement_unit=row[measurement_unit_csv],
                    )
                    ingredients_to_create.append(ingredient)
                except Exception as err:
                    print(f"Ошибка в строке {row}: {err}")

        if ingredients_to_create:
            Ingredient.objects.bulk_create(
                ingredients_to_create, ignore_conflicts=True)

        print("Данные успешно загружены в модель.")
