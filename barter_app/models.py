from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Модель категорий для объявлений."""

    name = models.CharField(
        _("Название"),
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Ad(models.Model):
    """Модель объявления для обмена товарами."""

    class Condition(models.TextChoices):
        NEW = "new", _("Новый")
        EXCELLENT = "excellent", _("Отличное")
        GOOD = "good", _("Хорошее")
        ACCEPTABLE = "acceptable", _("Приемлемое")
        POOR = "poor", _("Плохое")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name=_("Пользователь"),
    )
    title = models.CharField(
        _("Название"),
        max_length=200,
    )
    description = models.TextField(_("Описание"))
    image = models.ImageField(
        _("URL изображения"),
        blank=True,
        upload_to="photos/%Y/%m/%d/",
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="ads",
        verbose_name=_("Категория"),
    )
    condition = models.CharField(
        _("Состояние"),
        max_length=50,
        choices=Condition.choices,
        default=Condition.GOOD,
    )
    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    exchanged = models.BooleanField(
        _("Обмен произведен"),
        default=False,
    )

    class Meta:
        verbose_name = _("Объявление")
        verbose_name_plural = _("Объявления")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class ExchangeProposal(models.Model):
    """Модель предложения обмена между объявлениями."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Ожидает")
        ACCEPTED = "accepted", _("Принята")
        REJECTED = "rejected", _("Отклонена")

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="sent_proposals",
        verbose_name=_("Ваше объявление"),
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="received_proposals",
        verbose_name=_("Интересующее объявление"),
    )
    comment = models.TextField(
        _("Комментарий"),
        blank=True,
    )
    status = models.CharField(
        _("Статус"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Предложение обмена")
        verbose_name_plural = _("Предложения обмена")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.ad_sender} -> {self.ad_receiver}"
