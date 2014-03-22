from django.db import models


class Scrip(models.Model):
    scrip_id = models.CharField(max_length=100, primary_key=True)
    exchange = models.CharField(max_length=10)
    scrip_name = models.CharField(max_length=200)
    mkt_value = models.FloatField(


class Transaction(models.Model):
    date = models.DateTimeField()
    scrip = models.ForeignKey(Scrip)
    transaction_type = models.CharField(max_length=4)
    rate = models.FloatField()
    qty = models.IntegerField()

