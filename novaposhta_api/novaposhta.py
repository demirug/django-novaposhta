import json
from datetime import datetime
from enum import Enum

from aenum import MultiValueEnum
from django.conf import settings

from .mixins import NP_DirectJSONDataMixin
from .models import NP_WareHouse, NP_Document
from .scraping import NP_Scrapping
from .singleton import Singleton
from .updater import Updater


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


class PayerType(Enum):
    RECIPIENT = "Recipient"
    SENDER = "Sender"


class CargoType(Enum):
    PARCEL = "Parcel"
    DOCUMENTS = "Documents"


class Recipient:

    def __init__(self, first_name, middle_name, last_name, phone):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone


class OptionsSeat:
    def __init__(self, volumetricVolume, volumetricWidth, volumetricLength, volumetricHeight, weight):
        self.volumetricVolume = volumetricVolume
        self.volumetricWidth = volumetricWidth
        self.volumetricLength = volumetricLength
        self.volumetricHeight = volumetricHeight
        self.weight = weight


class Novaposhta(Singleton):

    def __init__(self):
        self.api_key = settings.NOVAPOSHTA_KEY
        self.scrapping = NP_Scrapping(self.api_key)
        self.updater = Updater(self.scrapping)

    def create_document(self, from_warehouse: NP_WareHouse, to_warehouse: NP_WareHouse,
                        weight: float, seats_amount: int, cost: int, description: str, recipient_data: Recipient,
                        option_seat: OptionsSeat = OptionsSeat(1, 30, 30, 30, 20),
                        payer_type: PayerType = PayerType.RECIPIENT, cargo_type: CargoType = CargoType.PARCEL,
                        save=True):

        sender = self.scrapping.counterparty.getCounterparties("Sender")[0]
        contact_sender = self.scrapping.counterparty.getCounterpartyContactPersons(sender['Ref'])[0]

        recipient = \
            self.scrapping.counterparty.create_Counterparty("PrivatePerson", "Recipient", recipient_data.first_name,
                                                            recipient_data.middle_name, recipient_data.last_name,
                                                            recipient_data.phone)[0]
        contact_recipient = recipient['ContactPerson']['data'][0]

        response = self.scrapping.document.create_document(
            PayerType=payer_type.value, PaymentMethod="Cash",
            DateTime=datetime.now().strftime("%d.%m.%Y"),
            CargoType=cargo_type.value,
            Weight=weight, SeatsAmount=seats_amount,
            Cost=cost, ServiceType="WarehouseWarehouse",
            Description=description,

            Sender=sender['Ref'],
            ContactSender=contact_sender['Ref'], SendersPhone=contact_sender['Phones'],
            CitySender=from_warehouse.City.Ref, SenderAddress=from_warehouse.Ref,
            Recipient=recipient['Ref'],
            ContactRecipient=contact_recipient['Ref'], RecipientsPhone=recipient_data.phone,
            CityRecipient=to_warehouse.City.Ref, RecipientAddress=to_warehouse.Ref,

            OptionsSeat=[{
                "volumetricVolume": option_seat.volumetricVolume,
                "volumetricLength": option_seat.volumetricLength,
                "volumetricWidth": option_seat.volumetricWidth,
                "volumetricHeight": option_seat.volumetricHeight,
                "weight": option_seat.weight
            }]
        )

        if response is None:
            return None

        if save:
            NP_Document(json=json.dumps(response))

        return response['Ref'], response['IntDocNumber']

    def delete_document(self, document: NP_Document):
        status = self.scrapping.document.delete_document(document.Ref)
        if status and status['Ref'] == document.Ref:
            document.delete()
            return True
        return False

    def delete_document_ref(self, document_ref: str):
        status = self.scrapping.document.delete_document(document_ref)
        NP_Document.objects.filter(Ref=document_ref).delete()
        return status and status['Ref'] == document_ref

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
