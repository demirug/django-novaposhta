# Django-novaposhta API
Python server side client for Nova Poshta company's API

Stored novaposhta addresses in database for quick access 
___


## Installation
Client is based on `python 3.6`

__Required packages__
````
httpx
aenum 
djangorestframework
django-filter
````

Add `novaposhta_api` to `INSTALLED_APPS`

Run migrations `manage.py migrate`
___
## Configuration

1. Add `NOVAPOSHTA_KEY=YOUR_API_KEY` to Django config file
2. `manage.py novaposhta update` to upload all data to DB (require time)

If you need you can rebuild all data (erase old and upload new) `manage.py novaposhta rebuild`
___
## Usage

__Working with Area, City, Warehouse, WarehouseType__
```python
    # Getting all warehouses in Kyiv
    NP_City.objects.get(Description="Київ").warehouses.all()
    # Getting all Post machine in Odesa
    NP_City.objects.get(Description="Одеса").warehouses.filter(Description="Поштомат")
    # Get all cities in Zaporizhzhia oblast
    NP_Area.objects.get(Description="Запорізька").cities.all()
    # All warehouses types
    NP_WareHouseType.objects.all()

    # Getting all post machine in Kyiv with allowed max parcel weight greater or equal 15
    type = NP_WareHouseType.objects.get(Description="Поштомат")
    NP_City.objects.get(Description="Київ").warehouses.filter(Type=type, TotalMaxWeightAllowed__gte=15).all()

    # Getting all working warehouses
    NP_WareHouse.objects.filter(WarehouseStatus="Working").all()
```

__Tracking documents__
```python
    # Ways to track parsel
    track: NP_Track = Novaposhta.track("tracknumber")
    track: NP_Track = Novaposhta.track("tracknumber", "phoneNumber") # For detail track

    # Check track status
    
    if track.StatusCode == NP_TackStatus.RECEIVED:
        doSomeThing()

    # Track standart parsel data
    track: NP_Track = np.track("tracknumber", "phoneNumber")
    if track: # if track information correct
        print(NP_TrackStatus.RECEIVED)
        print(f"{track.WarehouseSender} -> {track.WarehouseRecipient} | {track.StatusCode}")
        if track.is_Detail(): # If track contains available detail information
            print(f"{track.SenderFullNameEW or track.SenderFullName}: {track.PhoneSender}")
            print(f"{track.RecipientFullNameEW or track.RecipientFullName}: {track.PhoneRecipient}")
```

__Create/Delete document__
```python
    # Creating new document
    target = Recipient("Андрій", "Ваяків", "Буковінський", "+3806666666")

    ref, track_number = np.create_document(
        NP_WareHouse.objects.first(),  # from WareHouse
        NP_WareHouse.objects.filter(City__Description="Сколе").first(),  # to WareHouse
        1.5,  # Parsel Weight
        1,  # Seats amount
        1500,  # Declared price
        "Test parsell entry",  # Description
        target,  # Recipient
        payer_type=PayerType.SENDER,  # PayerType (SENDER/RECIPIENT)
        cargo_type=CargoType.PARCEL,  # CargoType (PARCEL/DOCUMENTS)
        save=True  # Save to DB
    )

    # Ways to delete document
    np.delete_document_ref(ref)
    np.delete_document(NP_Document.objects.filter(IntDocNumber=track_number).first())
```

__Updating/Rebuilding data__
```python
    # Run rebuild all data
    Novaposhta().updater.rebuild_data()
    # Run updating data (adding new adresses to DB) 
    Novaposhta.updater.update_data()
```

___
## API

__Register API url__
```python

urlpatterns = [
    ''
    path('api-np/', include(('novaposhta_api.api.urls', 'api-np'))),
    ''
]
```

__Available urls__
````
  List of areas: /api-np/areas
  List of cities (filtering): /api-np/cities
  List of warehouse types: /api-np/warehouse-type/
  List of warehouses (filtering): /api-np/warehouse