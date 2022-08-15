from django.db import models


class NP_WareHouseType(models.Model):
    ref = models.CharField(max_length=36, unique=True)

    description = models.CharField(max_length=50)
    description_ru = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class NP_Area(models.Model):
    ref = models.CharField(max_length=36, unique=True)

    description = models.CharField(max_length=50)
    description_ru = models.CharField(max_length=50)

    areas_center = models.CharField(max_length=36)

    def __str__(self):
        return self.description


class NP_City(models.Model):
    ref = models.CharField(max_length=36, unique=True)
    area = models.ForeignKey(NP_Area, on_delete=models.CASCADE, related_name='cities')

    description = models.CharField(max_length=50)
    description_ru = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class NP_WareHouse(models.Model):
    ref = models.CharField(max_length=36, unique=True)
    city = models.ForeignKey(NP_City, on_delete=models.CASCADE, related_name='warehouses')
    type = models.ForeignKey(NP_WareHouseType, on_delete=models.CASCADE, related_name='warehouses')

    siteKey = models.PositiveIntegerField()

    description = models.CharField(max_length=99)
    description_ru = models.CharField(max_length=99)

    denyToSelect = models.BooleanField()
    number = models.PositiveIntegerField()

    maxDeclaredCost = models.PositiveIntegerField()
    totalMaxWeightAllowed = models.PositiveIntegerField()
    placeMaxWeightAllowed = models.PositiveIntegerField()

    dimensions_max_width = models.PositiveIntegerField()
    dimensions_max_height = models.PositiveIntegerField()
    dimensions_max_length = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.type.description} #{self.number}: {self.city.description}"
