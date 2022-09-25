from django.db import models


class CardsInfo:
    rasdel = models.CharField(max_length=50)
    code = models.IntegerField()
    name = models.CharField(max_length=50)
    sales_id = models.IntegerField()
    sales_name = models.CharField(max_length=50)
    sales_credentials = models.CharField(max_length=1000)

    def __str__(self):
        return self.code


class MainModel(models.Model):
    rasdel = models.CharField(max_length=500)
    code = models.ForeignKey(CardsInfo.code, on_delete=models.CASCADE)
    review = models.IntegerField()
    price = models.IntegerField()
    rat = models.FloatField()
    date = models.DateTimeField()

