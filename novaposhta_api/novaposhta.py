from aenum import MultiValueEnum
from django.conf import settings

from .models import NP_Area, NP_City, NP_WareHouseType, NP_WareHouse
from .scraping import NP_Scrapping
from .singleton import Singleton


class NP_TrackStatus(MultiValueEnum):
    CREATED = 1,
    DELETED = 2,
    NOT_FOUND = 3,
    IN_CITY = 4, 41, 6,
    MOVING_ON = 5, 101,
    IN_WAREHOUSE = 7, 8,
    RECEIVED = 9, 10, 11,
    REFUSAL = 102, 103, 111, 105
    PARSEL_COMPLETING = 12
    REDIRECTING = 104,
    RECEIVED_RETURN_DELIVERY_INVOICE_CREATED = 106,
    RECEIVE_DATE_CHANGED = 112,


class NP_Track:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    warehouse_recipient: NP_WareHouse = None
    warehouse_sender: NP_WareHouse = None
    status: NP_TrackStatus = None
    status_date: str = None
    created_date: str = None
    scheduled_delivery_date: str = None
    document_weight: float = None
    seats_amount: int = None
    delivery_cost: float = None


class NP_TrackDetail(NP_Track):
    cargo_description: str = None
    cargo_price: float = None

    recipient_fullname: str = None
    recipient_phone: str = None
    sender_fullname: str = None
    sender_phone: str = None


class Novaposhta(Singleton):

    def __init__(self):
        self.api_key = settings.NOVAPOSHTA_KEY
        self.scrapping = NP_Scrapping(self.api_key)

    def rebuild_data(self):
        NP_WareHouse.objects.all().delete()
        NP_WareHouseType.objects.all().delete()
        NP_City.objects.all().delete()
        NP_Area.objects.all().delete()
        self.update_data()

    def update_data(self):
        self.register_warehouse_types()
        self.register_areas()
        self.register_cities()
        self.register_warehouses()

    def track(self, track_number):
        response = self.scrapping.tracking.track(track_number)
        if not response:
            return None
        try:
            return NP_Track(
                warehouse_sender=NP_WareHouse.objects.filter(ref=response['WarehouseSenderInternetAddressRef']).first(),
                warehouse_recipient=NP_WareHouse.objects.filter(
                    ref=response['WarehouseRecipientInternetAddressRef']).first(),
                status=NP_TrackStatus(int(response['StatusCode'])),
                status_date=response['TrackingUpdateDate'],
                created_date=response['DateCreated'],
                scheduled_delivery_date=response['ScheduledDeliveryDate'],
                document_weight=float(response['DocumentWeight']),
                seats_amount=int(response['SeatsAmount']),
                delivery_cost=float(response['DocumentCost']),
            )
        except Exception:
            return None

    def track_detail(self, track_number, phone):
        response = self.scrapping.tracking.track_detail(track_number, phone)
        if not response:
            return None
        try:
            track = NP_TrackDetail(
                warehouse_sender=NP_WareHouse.objects.filter(ref=response['WarehouseSenderInternetAddressRef']).first(),
                warehouse_recipient=NP_WareHouse.objects.filter(ref=response['WarehouseRecipientInternetAddressRef']).first(),
                status=NP_TrackStatus(int(response['StatusCode'])),
                status_date=response['TrackingUpdateDate'],
                created_date=response['DateCreated'],
                scheduled_delivery_date=response['ScheduledDeliveryDate'],
                document_weight=float(response['DocumentWeight']),
                seats_amount=int(response['SeatsAmount']),
                delivery_cost=float(response['DocumentCost']),

                cargo_description=response['CargoDescriptionString'],
                cargo_price=int(response['AnnouncedPrice']),

                recipient_fullname=response['RecipientFullNameEW'],
                recipient_phone=response['PhoneRecipient'],

                sender_fullname=response['SenderFullNameEW'],
                sender_phone=response['PhoneSender'],
            )
            if track.sender_phone == "":
                track.sender_phone = phone
            else:
                track.recipient_phone = phone
            return track
        except Exception:
            return None

    def register_warehouse_types(self):
        NP_WareHouseType.objects.bulk_create([NP_WareHouseType(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_warehouse_types()], ignore_conflicts=True)

    def register_warehouses(self):
        cities = NP_City.objects.all()
        warehouses_types = NP_WareHouseType.objects.all()

        NP_WareHouse.objects.bulk_create([NP_WareHouse(
            ref=elem['Ref'],
            city=cities.get(ref=elem['CityRef']),
            type=warehouses_types.get(ref=elem['TypeOfWarehouse']),
            status=elem['WarehouseStatus'],
            siteKey=int(elem['SiteKey']),
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            denyToSelect=bool(elem['DenyToSelect']),
            number=int(elem['Number']),
            maxDeclaredCost=int(elem['MaxDeclaredCost']),
            totalMaxWeightAllowed=int(elem['TotalMaxWeightAllowed']),
            placeMaxWeightAllowed=int(elem['PlaceMaxWeightAllowed']),
            dimensions_max_width=int(elem['SendingLimitationsOnDimensions']['Width']),
            dimensions_max_height=int(elem['SendingLimitationsOnDimensions']['Height']),
            dimensions_max_length=int(elem['SendingLimitationsOnDimensions']['Length'])
        ) for elem in self.scrapping.address.get_warehouse_all()], ignore_conflicts=True)

    def register_areas(self):
        NP_Area.objects.bulk_create([NP_Area(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            areas_center=elem['AreasCenter'],
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_areas()], ignore_conflicts=True)

    def register_cities(self):
        areas = NP_Area.objects.all()
        NP_City.objects.bulk_create([NP_City(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            ref=elem['Ref'],
            area=areas.get(ref=elem['Area']))
            for elem in self.scrapping.address.get_all_cities()], ignore_conflicts=True)
