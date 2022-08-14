from django.core.management import BaseCommand

from ...models import NP_WareHouse, NP_WareHouseType, NP_City, NP_Area
from ...novaposhta import Novaposhta


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help="")

    def handle(self, *args, **options):

        if options['action'] not in ['rebuild', 'update']:
            self.stdout.write(self.style.ERROR("Argument invalid. Available: rebuild, update"))
            return

        novaposhta: Novaposhta = Novaposhta()

        if options['action'] == 'rebuild':
            NP_WareHouse.objects.all().delete()
            self.stdout.write("Deleted WareHouses")
            NP_WareHouseType.objects.all().delete()
            self.stdout.write("Deleted WareHouse types")
            NP_City.objects.all().delete()
            self.stdout.write("Deleted Cities")
            NP_Area.objects.all().delete()
            self.stdout.write("Deleted Areas")

            novaposhta.register_areas()
            self.stdout.write("Registered Areas")
            novaposhta.register_cities()
            self.stdout.write("Registered Cities")
            novaposhta.register_warehouse_types()
            self.stdout.write("Registered Warehouse types")
            novaposhta.register_warehouses()
            self.stdout.write("Registered Warehouses")
            self.stdout.write(self.style.SUCCESS("Done"))

        else:
            novaposhta.register_areas()
            self.stdout.write("Added new Areas")
            novaposhta.register_cities()
            self.stdout.write("Added new Cities")
            novaposhta.register_warehouse_types()
            self.stdout.write("Added new Warehouse types")
            novaposhta.register_warehouses()
            self.stdout.write("Added new Warehouses")
            self.stdout.write(self.style.SUCCESS("Done"))

