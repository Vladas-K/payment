from django.shortcuts import render
from .forms import MeterForm
from .models import MeterReading

TARIFF_COLD = 65.77
TARIFF_HOT = 322.5
TARIFF_SEWAGE = 51.62

def calculate(request):
    result = None
    last = MeterReading.objects.order_by('-created_at').first()

    if request.method == "POST":
        form = MeterForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            cold_used = obj.cold_curr - obj.cold_prev
            hot_used = obj.hot_curr - obj.hot_prev
            sewage_used = cold_used + hot_used

            obj.cold_cost = cold_used * TARIFF_COLD
            obj.hot_cost = hot_used * TARIFF_HOT
            obj.sewage_cost = sewage_used * TARIFF_SEWAGE
            obj.total = (
                obj.cold_cost +
                obj.hot_cost +
                obj.sewage_cost +
                obj.electricity +
                obj.internet
            )

            obj.save()

            result = {
                "cold_cost": round(obj.cold_cost, 2),
                "hot_cost": round(obj.hot_cost, 2),
                "sewage_cost": round(obj.sewage_cost, 2),
                "electricity": obj.electricity,
                "internet": obj.internet,
                "total": round(obj.total, 2),
            }
    else:
        if last:
            form = MeterForm(initial={
                "cold_prev": last.cold_curr,
                "hot_prev": last.hot_curr,
                "electricity": last.electricity,
                "internet": last.internet,
            })
        else:
            form = MeterForm()

    return render(request, "calc.html", {"form": form, "result": result})



def history(request):
    records = MeterReading.objects.order_by('-created_at')
    return render(request, "history.html", {"records": records})
