from django.core.management.base import BaseCommand
from shop.models import Category, Medicine

DATA = {
    "Og'riq va harorat": [("Paratsetamol", "500 mg, 20 tabletka", 6500, False), ("Ibuprofen", "200 mg, 20 tabletka", 11000, False)],
    "Shamollash": [("Askorbin kislotasi", "100 mg, 50 draje", 5000, False), ("Burun uchun sprey", "Dengiz suvi, 30 ml", 28000, False)],
    "Oshqozon-ichak": [("Faollashtirilgan ko'mir", "250 mg, 10 tabletka", 3000, False), ("Omeprazol", "20 mg, 30 kapsula", 24000, True)],
    "Allergiya": [("Loratadin", "10 mg, 10 tabletka", 9000, False)],
    "Vitaminlar": [("Magniy B6", "50 tabletka", 52000, False), ("D3 vitamini", "2000 IU, 60 kapsula", 68000, False)],
}

class Command(BaseCommand):
    help = "Namuna ma'lumotlar (narxlar taxminiy)"

    def handle(self, *a, **kw):
        from django.utils.text import slugify
        for cname, meds in DATA.items():
            cat, _ = Category.objects.get_or_create(name=cname, defaults={"slug": slugify(cname) or cname})
            for name, dosage, price, rx in meds:
                Medicine.objects.get_or_create(name=name, defaults=dict(
                    category=cat, dosage=dosage, price=price, needs_prescription=rx, in_stock=40))
        self.stdout.write("Tayyor.")
