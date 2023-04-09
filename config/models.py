from django.db import models


class Inventory(models.Model):
    class Meta:
        db_table = "inventory"

    total_inventory = models.IntegerField()
    total_cost = models.IntegerField()


class Product(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=8)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:  # 새로운 객체일 때만 실행
            inventory = Inventory.objects.create(total_inventory=0, total_cost=0)
            self.inventory = inventory
        super().save(*args, **kwargs)


# model
class Inbound(models.Model):

    product_code = models.CharField(max_length=8)
    inbound_quantity = models.IntegerField()
    inbound_date = models.DateField()
    inbound_cost = models.IntegerField()

class Outbound(models.Model):

    product_code = models.CharField(max_length=8)
    outbound_quantity = models.IntegerField()
    outbound_date = models.DateField()
    outbound_cost = models.IntegerField()
