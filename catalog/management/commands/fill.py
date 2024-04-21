from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Предварительно очищаем БД
        Category.objects.all().delete()

        # Создаем список категорий, которые будут добавлены в БД
        category_list = [
            {'name': 'фрукты'},
            {'name': 'овощи'},
            {'name': 'молочка'}
        ]
        # Пакетное добавление данных
        category_for_create = []

        for category_item in category_list:
            category_for_create.append(Category(**category_item))

        Category.objects.bulk_create(category_for_create)

        # Список продуктов, которые будут добавлены в БД
        product_list = [
            {'name': 'ананас', 'category': Category.objects.get(name='фрукты'), 'price': 200},
            {'name': 'дыня', 'category': Category.objects.get(name='фрукты'), 'price': 150},
            {'name': 'яблоко', 'category': Category.objects.get(name='фрукты'), 'price': 50},
            {'name': 'груша', 'category': Category.objects.get(name='фрукты'), 'price': 100},
            {'name': 'свекла', 'category': Category.objects.get(name='овощи'), 'price': 50},
            {'name': 'морковь', 'category': Category.objects.get(name='овощи'), 'price': 30},
            {'name': 'капуста', 'category': Category.objects.get(name='овощи'), 'price': 50},
            {'name': 'лук', 'category': Category.objects.get(name='овощи'), 'price': 20},
            {'name': 'молоко', 'category': Category.objects.get(name='молочка'), 'price': 100},
            {'name': 'творог', 'category': Category.objects.get(name='молочка'), 'price': 150},
            {'name': 'сыр', 'category': Category.objects.get(name='молочка'), 'price': 500},
            {'name': 'сметана', 'category': Category.objects.get(name='молочка'), 'price': 50},

        ]
        # пакетное добавление данных
        products_for_create = []

        for product_item in product_list:
            products_for_create.append(Product(**product_item))

        Product.objects.bulk_create(products_for_create)