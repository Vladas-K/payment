from django.db import models

class MeterReading(models.Model):
    cold_prev = models.FloatField(
        verbose_name="Холодная вода (предыдущее)"
    )
    cold_curr = models.FloatField(
        verbose_name="Холодная вода (текущее)"
    )
    hot_prev = models.FloatField(
        verbose_name="Горячая вода (предыдущее)"
    )
    hot_curr = models.FloatField(
        verbose_name="Горячая вода (текущее)"
    )
    electricity = models.FloatField(
        verbose_name="Электричество",
        default=0
    )
    internet = models.FloatField(
        verbose_name="Интернет",
        default=0
    )

    cold_cost = models.FloatField(
        verbose_name="Стоимость холодной воды"
    )
    hot_cost = models.FloatField(
        verbose_name="Стоимость горячей воды"
    )
    sewage_cost = models.FloatField(
        verbose_name="Стоимость водоотведения"
    )
    total = models.FloatField(
        verbose_name="Итого"
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Платёж от {self.created_at.strftime('%Y-%m-%d %H:%M')}"
