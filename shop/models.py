from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Nomi", max_length=60)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Medicine(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="medicines")
    name = models.CharField("Nomi", max_length=120)
    maker = models.CharField("Ishlab chiqaruvchi", max_length=80, blank=True)
    dosage = models.CharField("Dozasi / shakli", max_length=80, blank=True)
    description = models.TextField("Tavsif", blank=True)
    price = models.PositiveIntegerField("Narxi (so'm)")
    in_stock = models.PositiveIntegerField("Omborda", default=0)
    needs_prescription = models.BooleanField("Retsept bilan", default=False)
    image = models.ImageField(upload_to="meds/", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", args=[self.pk])


class Order(models.Model):
    STATUS = [("new", "Yangi"), ("confirmed", "Tasdiqlandi"),
              ("delivered", "Yetkazildi"), ("cancelled", "Bekor qilindi")]
    name = models.CharField("Ism", max_length=80)
    phone = models.CharField("Telefon", max_length=20)
    address = models.CharField("Manzil", max_length=200)
    comment = models.CharField("Izoh", max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="new")
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Buyurtma #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    qty = models.PositiveSmallIntegerField()
