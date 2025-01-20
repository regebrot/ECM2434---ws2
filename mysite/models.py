from django.db import models

class AmountType(models.Model):
  name = models.CharField(max_length=100)

class ItemType(models.Model):
  uniqueBarcode = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  amountType = models.ForeignKey(AmountType, on_delete=models.CASCADE)

class IndividualItems(models.Model):
  id = models.IntegerField()
  expirationDate = models.DateField()
  type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
  amount = models.IntegerField()

class ShoppingList(models.Model):
  itemType = models.ForeignKey(ItemType, on_delete=models.CASCADE)
  amount = models.IntegerField()