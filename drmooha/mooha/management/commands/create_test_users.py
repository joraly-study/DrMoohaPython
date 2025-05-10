from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from mooha.models import Product, Category, Tag

class Command(BaseCommand):
    help = 'данная команда создает тестовых пользователей и группы с правами доступа'

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Администратор')
        seller_group, _ = Group.objects.get_or_create(name='Продавец')
        buyer_group, _ = Group.objects.get_or_create(name='Покупатель')

        product_permissions = Permission.objects.filter(
            content_type__model='product'
        )
        category_permissions = Permission.objects.filter(
            content_type__model='category'
        )
        tag_permissions = Permission.objects.filter(
            content_type__model='tag'
        )

        #назначаем права группам
        admin_group.permissions.set(
            product_permissions | category_permissions | tag_permissions
        )

        seller_group.permissions.set(
            Permission.objects.filter(
                content_type__model='product',
                codename__in=['add_product', 'change_product', 'view_product']
            )
        )

        buyer_group.permissions.set(
            Permission.objects.filter(
                content_type__model__in=['product', 'category', 'tag'],
                codename__startswith='view_'
            )
        )

        if not User.objects.filter(username='admin').exists():
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(f'Создан суперпользователь: {superuser.username}'))
        else:
            self.stdout.write(self.style.WARNING('Суперпользователь уже существует'))

        for i in range(2):
            username = f'admin{i+1}'
            if not User.objects.filter(username=username).exists():
                admin = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='admin123'
                )
                admin.groups.add(admin_group)
                self.stdout.write(self.style.SUCCESS(f'Создан администратор: {admin.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Администратор {username} уже существует'))

        for i in range(3):
            username = f'seller{i+1}'
            if not User.objects.filter(username=username).exists():
                seller = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='seller123'
                )
                seller.groups.add(seller_group)
                self.stdout.write(self.style.SUCCESS(f'Создан продавец: {seller.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продавец {username} уже существует'))

        for i in range(4):
            username = f'buyer{i+1}'
            if not User.objects.filter(username=username).exists():
                buyer = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='buyer123'
                )
                buyer.groups.add(buyer_group)
                self.stdout.write(self.style.SUCCESS(f'Создан покупатель: {buyer.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Покупатель {username} уже существует'))

        self.stdout.write(self.style.SUCCESS('Все пользователи и группы созданы успешно')) 