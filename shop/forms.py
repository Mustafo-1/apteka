from django import forms
from .models import Order

CLS = "field"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address", "comment"]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs["class"] = CLS
        self.fields["comment"].required = False
        self.fields["phone"].widget.attrs["placeholder"] = "+998 90 123 45 67"
