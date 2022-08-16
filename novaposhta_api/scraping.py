import json

import requests

from .singleton import Singleton


def _kwargs_to_prams(**kwargs):
    return {k: v for k, v in kwargs.items()}


class _Model:
    def __init__(self, client, model_name):
        self._client = client
        self.model_name = model_name

    def _call(self, api_method, props):
        data = self._client.send(self.model_name, api_method, props)['data']
        if len(data) == 0:
            return None
        return data


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


class _Tacking(_Model):
    def __init__(self, client):
        super().__init__(client, "TrackingDocument")

    def track(self, track_number):
        data = self._call("getStatusDocuments", {"Documents": [{"DocumentNumber": track_number}]})
        if data is not None:
            return data[0]
        return data

    def track_detail(self, track_number, phone):
        data = self._call("getStatusDocuments", {"Documents": [{"DocumentNumber": track_number, "Phone": phone}]})
        if data is not None:
            return data[0]
        return data


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
    def tracking(self):
        return _Tacking(self)
