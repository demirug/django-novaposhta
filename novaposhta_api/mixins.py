import json

from django.db import IntegrityError


class NP_DirectJSONDataMixin:
    def __init__(self, api_json: dict, *args, **kwargs):
        super(NP_DirectJSONDataMixin, self).__init__(*args, **kwargs)
        if api_json is None:
            return

        for key, value in api_json.items():
            handled = False
            if hasattr(self, f"handle_{key}"):
                attr = getattr(self, f"handle_{key}")
                if callable(attr):
                    handled = True
                    attr(value)

            if not handled:
                setattr(self, key, value)


class NP_JSONDataMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.get_json() == "":
            return

        need_save = False
        for key, value in json.loads(self.get_json()).items():
            handled = False
            if hasattr(self, f"handle_{key}"):
                attr = getattr(self, f"handle_{key}")
                if callable(attr):
                    handled = True
                    if attr(value):
                        need_save = True

            if not handled and hasattr(self, key):
                if getattr(self, key) != value:
                    setattr(self, key, value)
                    need_save = True

        if need_save:
            try:
                super().save()
            except IntegrityError as e:
                pass

    def get_json(self):
        return getattr(self, 'json')

    class Meta:
        abstract = True
