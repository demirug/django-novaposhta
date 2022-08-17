import json

import requests

from .singleton import Singleton


def _getfirst_elem(response):
    if response is None:
        return response
    return response[0]


def _kwargs_to_prams(**kwargs):
    return {k: v for k, v in kwargs.items()}


class _Model:
    def __init__(self, client, model_name):
        self._client = client
        self.model_name = model_name

    def _call(self, api_method, props):
        response = self._client.send(self.model_name, api_method, props)
        if response['success'] is False:
            print(f"Novaposhta-API: Handled Un-success response at {self.model_name}: {api_method}")
            print(response)
            return None
        return response['data']


class _Address(_Model):

    def __init__(self, client):
        super().__init__(client, "Address")

    def get_warehouse_types(self):
        return self._call("getWarehouseTypes", {})

    def get_warehouse(self, city_ref, page=1, limit=20):
        return self._call("getWarehouses", _kwargs_to_prams(CityRef=city_ref, Page=page, Limit=limit))

    def get_warehouse_all(self):
        return self._call("getWarehouses", {})

    def get_areas(self):
        return self._call("getAreas", {})

    def get_city(self, ref, page=1, limit=20):
        props = _kwargs_to_prams(Ref=ref, Page=page, Limit=limit)
        return self._call("getCities", props)

    def get_all_cities(self):
        return self._call("getCities", {})


class _Common(_Model):
    def __init__(self, client):
        super(_Common, self).__init__(client, "Common")

    def get_cargo_types(self):
        return self._call("getCargoTypes", {})


class _Tacking(_Model):
    def __init__(self, client):
        super().__init__(client, "TrackingDocument")

    def track(self, track_number):
        return _getfirst_elem(self._call("getStatusDocuments", {"Documents": [{"DocumentNumber": track_number}]}))

    def track_detail(self, track_number, phone):
        return _getfirst_elem(self._call("getStatusDocuments", {"Documents": [{"DocumentNumber": track_number, "Phone": phone}]}))


class _Counterparty(_Model):
    def __init__(self, client):
        super(_Counterparty, self).__init__(client, "Counterparty")

    def getCounterparties(self, counterparty_property):
        return self._call("getCounterparties", _kwargs_to_prams(CounterpartyProperty=counterparty_property))

    def getCounterpartyContactPersons(self, ref):
        return self._call("getCounterpartyContactPersons", _kwargs_to_prams(Ref=ref))

    def create_Counterparty(self, counterparty_type, counterparty_property, firstname, middle_name, lastname, phone):
        return self._call("save", _kwargs_to_prams(CounterpartyType=counterparty_type,
                                                   CounterpartyProperty=counterparty_property,
                                                   FirstName=firstname, MiddleName=middle_name, LastName=lastname,
                                                   Phone=phone))


class _InternetDocument(_Model):
    def __init__(self, client):
        super(_InternetDocument, self).__init__(client, "InternetDocument")

    def create_document(self, **kwargs):
        return _getfirst_elem(self._call("save", _kwargs_to_prams(**kwargs)))

    def delete_document(self, ref):
        return _getfirst_elem(self._call("delete", _kwargs_to_prams(DocumentRefs=ref)))


class NP_Scrapping(Singleton):

    def __init__(self, api_key, api_endpoint="https://api.novaposhta.ua/v2.0/json/"):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def send(self, model_name, api_method, method_props):
        data = {
            'apiKey': self.api_key,
            'modelName': model_name,
            'calledMethod': api_method,
            "methodProperties": method_props
        }
        response = requests.post(self.api_endpoint, json=data,
                                 headers={'Content-Type': 'application/json'})
        return json.loads(response.content)

    @property
    def address(self):
        return _Address(self)

    @property
    def common(self):
        return _Common(self)

    @property
    def tracking(self):
        return _Tacking(self)

    @property
    def document(self):
        return _InternetDocument(self)

    @property
    def counterparty(self):
        return _Counterparty(self)
