from django.db import models

from .mixins import NP_JSONDataMixin


class NP_Document(NP_JSONDataMixin, models.Model):
    Ref = models.CharField(max_length=36, unique=True)
    IntDocNumber = models.CharField(max_length=36)

    json = models.TextField()

    class Meta:
        verbose_name = "NP Document"
        verbose_name_plural = "NP Documents"

    def __str__(self):
        return self.IntDocNumber


class NP_CargoType(NP_JSONDataMixin, models.Model):
    Ref = models.CharField(max_length=36, unique=True)
    Description = models.CharField(max_length=36)

    json = models.TextField()

    class Meta:
        verbose_name = "NP Cargo Type"
        verbose_name_plural = "NP Cargo Types"

    def __str__(self):
        return self.Description


class NP_WareHouseType(NP_JSONDataMixin, models.Model):
    Ref = models.CharField(max_length=36, unique=True)

    Description = models.CharField(max_length=50)
    DescriptionRu = models.CharField(max_length=50)

    json = models.TextField()

    class Meta:
        verbose_name = "NP WareHouse Type"
        verbose_name_plural = "NP WareHouse Types"

    def __str__(self):
        return self.Description


class NP_Area(NP_JSONDataMixin, models.Model):
    Ref = models.CharField(max_length=36, unique=True)

    Description = models.CharField(max_length=50)
    DescriptionRu = models.CharField(max_length=50)

    AreasCenter = models.CharField(max_length=36)

    json = models.TextField()

    class Meta:
        verbose_name = "NP Area"
        verbose_name_plural = "NP Areas"

    def __str__(self):
        return self.Description


class NP_City(NP_JSONDataMixin, models.Model):
    Ref = models.CharField(max_length=36, unique=True)
    Area = models.ForeignKey(NP_Area, on_delete=models.CASCADE, related_name='cities')

    Description = models.CharField(max_length=50)
    DescriptionRu = models.CharField(max_length=50)

    json = models.TextField()

    def handle_Area(self, obj):
        if self.Area_id is None:
            self.Area = NP_Area.objects.filter(Ref=obj).first()
            return True

    class Meta:
        verbose_name = "NP City"
        verbose_name_plural = "NP Cities"

    def __str__(self):
        return self.Description


class NP_WareHouse(NP_JSONDataMixin, models.Model):

    def __init__(self, *args, **kwargs):
        super(NP_WareHouse, self).__init__(*args, **kwargs)

    Ref = models.CharField(max_length=36, unique=True)

    City = models.ForeignKey(NP_City, on_delete=models.CASCADE, related_name='warehouses')
    Type = models.ForeignKey(NP_WareHouseType, on_delete=models.CASCADE, related_name='warehouses')
    WarehouseStatus = models.CharField(max_length=36)

    SiteKey = models.PositiveIntegerField()

    Description = models.CharField(max_length=99)
    DescriptionRu = models.CharField(max_length=99)

    DenyToSelect = models.BooleanField()
    Number = models.PositiveIntegerField()

    MaxDeclaredCost = models.PositiveIntegerField()
    TotalMaxWeightAllowed = models.PositiveIntegerField()
    PlaceMaxWeightAllowed = models.PositiveIntegerField()

    DimensionsMaxWidth = models.PositiveIntegerField()
    DimensionsMaxHeight = models.PositiveIntegerField()
    DimensionsMaxLength = models.PositiveIntegerField()

    json = models.TextField()

    def handle_CityRef(self, obj):
        if self.City_id is None:
            self.City = NP_City.objects.filter(Ref=obj).first()
            return True

    def handle_TypeOfWarehouse(self, obj):
        if self.Type_id is None:
            self.Type = NP_WareHouseType.objects.filter(Ref=obj).first()
            return True

    def handle_SendingLimitationsOnDimensions(self, obj):
        if self.DimensionsMaxWidth != obj['Width']:
            self.DimensionsMaxWidth = obj['Width']
            self.DimensionsMaxHeight = obj['Height']
            self.DimensionsMaxLength = obj['Length']
            return True

    class Meta:
        verbose_name = "NP Warehouses"
        verbose_name_plural = "NP Warehouse"

    def __str__(self):
        return f"{self.Type.Description} #{self.Number}: {self.City.Description}"
