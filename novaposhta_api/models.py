from django.db import models


class NP_WareHouseType(models.Model):
    description = models.CharField(max_length=50)
    ref = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return self.description


class NP_Area(models.Model):
    description = models.CharField(max_length=50)
    ref = models.CharField(max_length=36, unique=True)
    areas_center = models.CharField(max_length=36)

    def __str__(self):
        return self.description


class NP_City(models.Model):
    area = models.ForeignKey(NP_Area, on_delete=models.CASCADE, related_name='cities')
    description = models.CharField(max_length=50)
    ref = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return self.description


class NP_WareHouse(models.Model):
    city = models.ForeignKey(NP_City, on_delete=models.CASCADE, related_name='warehouses')
    type = models.ForeignKey(NP_WareHouseType, on_delete=models.CASCADE, related_name='warehouses')
    description = models.CharField(max_length=99)
    number = models.CharField(max_length=36)
    ref = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return f"{self.description} {self.number}"
