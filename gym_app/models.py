from django.db import models
from django.utils import timezone
from django.db.models import Count

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(BaseModel):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def is_vip(self):
        return self.balance > 1000

    def __str__(self):
        return f"{self.name} {'(VIP)' if self.is_vip else ''}"
    

class Branch(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Trainer(BaseModel):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class GymClassQuerySet(models.QuerySet):
    def trending(self):
        return self.annotate(member_count=Count('members')).filter(member_count__gt=15)

class GymClassManager(models.Manager):
    def get_queryset(self):
        return GymClassQuerySet(self.model, using=self._db)

    def trending(self):
        return self.get_queryset().trending()

class GymClass(BaseModel):
    title = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateTimeField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='classes')
    members = models.ManyToManyField(Member, related_name='enrolled_classes', blank=True)

    objects = GymClassManager()

    def calculate_early_bird_discount(self):
        if self.start_date:
            days_until_start = (self.start_date - timezone.now()).days
            if days_until_start > 30:
                discounted_price = float(self.base_price) * 0.8
                return round(discounted_price, 2)
        return float(self.base_price)

    def __str__(self):
        return self.title
    
class Equipment(BaseModel):
    name = models.CharField(max_length=255)
    is_damaged = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='equipments')

    def __str__(self):
        return self.name

class DamagedEquipmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_damaged=True)

class DamagedEquipment(Equipment):
    objects = DamagedEquipmentManager()

    class Meta:
        proxy = True
        verbose_name = "Damaged Equipment"
        verbose_name_plural = "Maintenance Portal"