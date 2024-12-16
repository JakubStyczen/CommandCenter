from django.shortcuts import render, redirect
from django.urls import reverse

from .models import PigeonInterrupt

# Create your views here.
def home_view(request):
    return render(request, 'pigeonInterrupts/home.html')

def pigeon_interrupt_list_view(request):
    if quantity := request.GET.get('quantity') != "":
        quantity = int(quantity)
    else:
        quantity = 5
    pigeons_interrupts = PigeonInterrupt.objects.all().order_by("Time").reverse()[:quantity]
    
    return render(request, 'pigeonInterrupts/pigeon_interrupt_list.html', {'pigeons_interrupts':pigeons_interrupts})

def pigeon_interrupt_delete_view(request, id):
    pigeon_interrupt = PigeonInterrupt.objects.get(id=id)
    if request.method == 'POST':
        pigeon_interrupt.delete()
        return redirect('pigeonInterrupts/pigeon_interrupt_list.html')
    return render(request, 'pigeonInterrupts/pigeon_interrupt_delete.html', {'pigeon_interrupt':pigeon_interrupt})