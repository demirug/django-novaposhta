from django.core.management import BaseCommand

from ...novaposhta import Novaposhta


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help="")

    def handle(self, *args, **options):

        actions = ['rebuild', 'update']
        if options['action'] not in actions:
            self.stdout.write(self.style.ERROR("Argument invalid. Available: " + ", ".join(actions)))
            return

        novaposhta: Novaposhta = Novaposhta()

        if options['action'] == 'rebuild':
            novaposhta.updater.rebuild_data()
            self.stdout.write(self.style.SUCCESS("Done"))

        if options['action'] == 'update':
            novaposhta.updater.update_data()
            self.stdout.write(self.style.SUCCESS("Done"))

