from django.shortcuts import render, redirect

# Create your views here.
from .forms import WeatherConditionsForm
from .models import WeatherConditions


def home_view(request):
    return render(request, "weatherApp/home.html")


def weather_conditions_create_view(request):
    form = WeatherConditionsForm()
    if request.method == "POST":
        form = WeatherConditionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weatherApp:weather_conditions_list")
    return render(request, "weatherApp/weather_conditions_create.html", {"form": form})


def weather_conditions_list_view(request):
    quantity_raw = request.GET.get("quantity")
    if quantity_raw != "" and quantity_raw is not None:
        quantity = int(quantity_raw)
    else:
        quantity = 5
    weather_conditions = (
        WeatherConditions.objects.all().order_by("time").reverse()[:quantity]
    )
    return render(
        request,
        "weatherApp/weather_conditions_list.html",
        {"weather_conditions": weather_conditions},
    )


def weather_conditions_update_view(request, id):
    product = WeatherConditions.objects.get(condition_id=id)
    form = WeatherConditionsForm()
    if request.method == "POST":
        form = WeatherConditionsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("weatherApp:weather_conditions_list")
    return render(request, "weatherApp/weather_conditions_create.html", {"form": form})


def weather_conditions_delete_view(request, id):
    weather_condition = WeatherConditions.objects.get(condition_id=id)
    if request.method == "POST":
        weather_condition.delete()
        return redirect("weatherApp:weather_conditions_list")
    return render(
        request,
        "weatherApp/weather_conditions_delete.html",
        {"weather_condition": weather_condition},
    )
