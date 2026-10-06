from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Category, Medicine, Order, OrderItem


def cart_items(request):
    cart = request.session.get("cart", {})
    items, total = [], 0
    for m in Medicine.objects.filter(pk__in=cart.keys()):
        qty = min(cart[str(m.pk)], m.in_stock)
        if qty > 0:
            items.append({"med": m, "qty": qty, "sub": m.price * qty})
            total += m.price * qty
    return items, total


def catalog(request):
    g = request.GET
    qs = Medicine.objects.select_related("category")
    if g.get("q"):
        qs = qs.filter(Q(name__icontains=g["q"]) | Q(maker__icontains=g["q"]))
    if g.get("cat"):
        qs = qs.filter(category__slug=g["cat"])
    params = g.copy()
    params.pop("page", None)
    return render(request, "shop/catalog.html", {
        "page": Paginator(qs, 12).get_page(g.get("page")), "g": g,
        "categories": Category.objects.all(), "query": params.urlencode()})


def detail(request, pk):
    return render(request, "shop/detail.html", {"med": get_object_or_404(Medicine, pk=pk)})


@require_POST
def cart_set(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    cart = request.session.get("cart", {})
    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = 1
    if request.POST.get("add"):
        qty += cart.get(str(pk), 0)
    qty = min(qty, med.in_stock)
    if qty > 0:
        cart[str(pk)] = qty
    else:
        cart.pop(str(pk), None)
    request.session["cart"] = cart
    return redirect(request.POST.get("next") or "cart")


def cart(request):
    items, total = cart_items(request)
    return render(request, "shop/cart.html", {"items": items, "total": total})


def checkout(request):
    items, total = cart_items(request)
    if not items:
        return redirect("cart")
    form = OrderForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.total = total
            order.save()
            for it in items:
                OrderItem.objects.create(order=order, medicine=it["med"],
                                         price=it["med"].price, qty=it["qty"])
                Medicine.objects.filter(pk=it["med"].pk).update(in_stock=F("in_stock") - it["qty"])
        request.session["cart"] = {}
        return render(request, "shop/done.html", {"order": order})
    return render(request, "shop/checkout.html", {"form": form, "items": items, "total": total})
