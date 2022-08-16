import json

from django.db import IntegrityError


class NP_JSONDataMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
