# Django-novaposhta API
Python server side client for Nova Poshta company's API

Stored novaposhta addresses in database for quick access 
___


## Installation
Client is based on `python 3.6`

You can install package by using pip:
 
`pip install git+https://github.com/demirug/django-novaposhta`
___
## Configuration

1. Add `NOVAPOSHTA_KEY=YOUR_API_KEY` to Django config file

2. `manage.py migrate`
3. `manage.py novaposhta update` to upload all data to DB (require time)

If you need you can rebuild all data (erase old and upload new) `manage.py novaposhta rebuild`
___
## Usage

```python
    # Getting all warehouses in Kyiv
    NP_City.objects.get(description="Київ").warehouses.all()
    # Getting all Post machine in Odesa
    NP_City.objects.get(description="Одеса").warehouses.filter(description="Поштомат")
    # Get all cities in Zaporizhzhia oblast
    NP_Area.objects.get(description="Запорізька").cities.all()
    # All warehouses types
    NP_WareHouseType.objects.all()

    # Getting all post machine in Kyiv with allowed max parcel weight greater or equal 15
    type = NP_WareHouseType.objects.get(description="Поштомат")
    NP_City.objects.get(description="Київ").warehouses.filter(type=type, totalMaxWeightAllowed__gte=15).all()

    # Run rebuild all data
    Novaposhta().rebuild_data()
    # Run updating data (adding new adresses to DB) 
    Novaposhta.update_data()