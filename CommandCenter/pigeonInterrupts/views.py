from django.shortcuts import render, redirect
from django.urls import reverse

from .models import PigeonInterrupt


# Create your views here.
def home_view(request):
    return render(request, "pigeonInterrupts/home.html")


def pigeon_interrupt_list_view(request):
    quantity_raw = request.GET.get("quantity")
    if quantity_raw != "" and quantity_raw is not None:
        quantity = int(quantity_raw)
    else:
        quantity = 5
    pigeons_interrupts = (
        PigeonInterrupt.objects.all().order_by("Time").reverse()[:quantity]
    )
    return render(
        request,
        "pigeonInterrupts/pigeon_interrupt_list.html",
        {"pigeons_interrupts": pigeons_interrupts},
    )


def pigeon_interrupt_delete_view(request, id):
    pigeon_interrupt = PigeonInterrupt.objects.get(id=id)
    if request.method == "POST":
        pigeon_interrupt.delete()
        return redirect("pigeonInterrupts:pigeon_interrupt_list")
    return render(
        request,
        "pigeonInterrupts/pigeon_interrupt_delete.html",
        {"pigeon_interrupt": pigeon_interrupt},
    )
