from django.db import models

from myproject.choices import COUNTRY_LIST


class Edition(models.Model):
    name = models.CharField(max_length=128, null=False)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year} {self.name}"


class Entry(models.Model):
    artist = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=False, choices=COUNTRY_LIST)
    # edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=False)
    # code = models.CharField(max_length=256, null=False)
    year = models.IntegerField()
    code = models.CharField(max_length=256, default="xxxx")

    def __str__(self):
        return f"{self.code} {self.artist} - {self.title}"


class Vote(models.Model):
    voter = models.CharField(max_length=64, null=False)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, null=False)
    score = models.IntegerField(null=False)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.voter} {self.entry}: {self.score}"
