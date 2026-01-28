import pytest
from django.urls import reverse
from meters.models import MeterReading
from meters.forms import MeterForm
from meters.views import TARIFF_COLD, TARIFF_HOT, TARIFF_SEWAGE


@pytest.mark.django_db
def test_calculate_valid_post_creates_record(client):
    url = reverse("meters:calculate")

    data = {
        "cold_prev": 10,
        "cold_curr": 20,
        "hot_prev": 5,
        "hot_curr": 10,
        "electricity": 100,
        "internet": 500,
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert MeterReading.objects.count() == 1

    obj = MeterReading.objects.first()

    assert obj.cold_cost == (20 - 10) * TARIFF_COLD
    assert obj.hot_cost == (10 - 5) * TARIFF_HOT
    assert obj.sewage_cost == ((20 - 10) + (10 - 5)) * TARIFF_SEWAGE
    assert obj.total == (
        obj.cold_cost +
        obj.hot_cost +
        obj.sewage_cost +
        obj.electricity +
        obj.internet
    )


@pytest.mark.django_db
def test_calculate_invalid_post_returns_errors(client):
    url = reverse("meters:calculate")

    response = client.post(url, {})  # пустые данные

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
    assert MeterReading.objects.count() == 0


@pytest.mark.django_db
def test_calculate_get_initial_values(client):
    # Создаём предыдущую запись
    last = MeterReading.objects.create(
        cold_prev=0, cold_curr=10,
        hot_prev=0, hot_curr=5,
        electricity=100,
        internet=500,
        cold_cost=0, hot_cost=0, sewage_cost=0, total=0
    )

    url = reverse("meters:calculate")
    response = client.get(url)

    form = response.context["form"]

    assert form.initial["cold_prev"] == last.cold_curr
    assert form.initial["hot_prev"] == last.hot_curr
    assert form.initial["electricity"] == last.electricity
    assert form.initial["internet"] == last.internet


@pytest.mark.django_db
def test_calculate_get_without_previous_records(client):
    url = reverse("meters:calculate")
    response = client.get(url)

    form = response.context["form"]

    assert form.initial["cold_prev"] == ""
    assert form.initial["hot_prev"] == ""
    assert form.initial["electricity"] == ""
    assert form.initial["internet"] == ""


@pytest.mark.django_db
def test_calculate_result_displayed_after_redirect(client):
    obj = MeterReading.objects.create(
        cold_prev=0, cold_curr=10,
        hot_prev=0, hot_curr=5,
        electricity=100,
        internet=500,
        cold_cost=100,
        hot_cost=200,
        sewage_cost=50,
        total=450,
    )

    # Кладём ID в сессию
    session = client.session
    session["last_result_id"] = obj.id
    session.save()

    url = reverse("meters:calculate")
    response = client.get(url)

    assert response.status_code == 200
    assert "result" in response.context
    assert response.context["result"]["total"] == 450
