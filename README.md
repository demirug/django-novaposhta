# Django-novaposhta API
Python server side client for Nova Poshta company's API

Stored novaposhta addresses in database for quick access 
___


## Installation
Client is based on `python 3.6`

Required `aenum` package `pip install aenum`

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

    # Run rebuild all data
    Novaposhta().updater.rebuild_data()
    # Run updating data (adding new adresses to DB) 
    Novaposhta.updater.update_data()
       
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