from vaccination.models import Slot
from center.models import Storage


def reserve_vaccine(slot_id):
    slot = Slot.objects.get(id=slot_id)
    storage = Storage.objects.get(center=slot.campaign.center)
    if slot.max_capacity > slot.reserved:
        slot.reserved = slot.reserved + 1
        storage.booked_quantity = storage.booked_quantity + 1
        slot.save()
        storage.save()
        return True
    else:
        return False
