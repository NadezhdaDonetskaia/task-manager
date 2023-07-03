from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда для вывода приветствия в консоль'

    def handle(self, *args, **options):
        self.stdout.write('Приветствую, пользователь!')
