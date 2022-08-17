import json

from aenum import MultiValueEnum
from django.conf import settings

from .mixins import NP_DirectJSONDataMixin
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


class NP_Track(NP_DirectJSONDataMixin):
    """
    Most popular attrs:
           TrackingUpdateDate, DateCreated, ScheduledDeliveryDate, DocumentWeight,
           SeatsAmount, DocumentCost, CargoDescriptionString, AnnouncedPrice,
           RecipientFullNameEW, PhoneRecipient, SenderFullNameEW, PhoneSender
    See more at: https://developers.novaposhta.ua/view/model/a99d2f28-8512-11ec-8ced-005056b2dbe1/method/a9ae7bc9-8512-11ec-8ced-005056b2dbe1
    """
    WarehouseSender: NP_WareHouse = None
    WarehouseRecipient: NP_WareHouse = None
    StatusCode: NP_TrackStatus = None

    def handle_WarehouseSenderInternetAddressRef(self, obj):
        self.WarehouseSender = NP_WareHouse.objects.filter(Ref=obj).first()

    def handle_WarehouseRecipientInternetAddressRef(self, obj):
        self.WarehouseRecipient = NP_WareHouse.objects.filter(Ref=obj).first()

    def handle_StatusCode(self, obj):
        self.StatusCode = NP_TrackStatus(int(obj))

    def is_Detail(self):
        return self.PhoneSender != "" and self.PhoneRecipient != ""


class Novaposhta(Singleton):

    def __init__(self):
        self.api_key = settings.NOVAPOSHTA_KEY
        self.scrapping = NP_Scrapping(self.api_key)
        self.updater = Updater(self.scrapping)

    def track(self, track_number, phone=None):

        if phone:
            response = self.scrapping.tracking.track_detail(track_number, phone)
        else:
            response = self.scrapping.tracking.track(track_number)

        if response is None:
            return None
        track = NP_Track(api_json=response)
        if phone:
            if track.PhoneSender == "":
                track.PhoneSender = phone
            else:
                track.PhoneRecipient = phone
        return track


class Updater:

    def __init__(self, scrapping: NP_Scrapping):
        self.scrapping = scrapping

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

    def register_warehouse_types(self):
        for elem in self.scrapping.address.get_warehouse_types():
            NP_WareHouseType(json=json.dumps(elem))

    def register_warehouses(self):
        for elem in self.scrapping.address.get_warehouse_all():
            NP_WareHouse(json=json.dumps(elem))

    def register_areas(self):
        for elem in self.scrapping.address.get_areas():
            NP_Area(json=json.dumps(elem))

    def register_cities(self):
        for elem in self.scrapping.address.get_all_cities():
            NP_City(json=json.dumps(elem))
