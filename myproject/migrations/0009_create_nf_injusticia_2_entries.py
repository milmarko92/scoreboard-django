# Generated by Django 3.1.3 on 2020-11-14 18:52

from django.db import migrations
from django.db.migrations import RunPython

from myproject.inputs.injusticia_2_sf1 import injusticia_2_entries_2, injusticia_2_entries_1


def create_entries_1(apps, schema_editor):
    entries = []
    Entry = apps.get_model("myproject", "Entry")
    Edition = apps.get_model("myproject", "Edition")
    edition, _ = Edition.objects.get_or_create(name="People's Choice: Robbed2 Semi 1", year=0)
    for entry in injusticia_2_entries_1:
        split = entry.split("\t")
        year = split[0]
        country = split[1]
        artist = split[2]
        song = split[3]
        code = split[4].lower()
        e = Entry(artist=artist, title=song, code=code, year=year,country=country)
        entries.append(e)
    Entry.objects.bulk_create(entries)

def create_entries_2(apps, schema_editor):
    entries = []
    Entry = apps.get_model("myproject", "Entry")
    Edition = apps.get_model("myproject", "Edition")
    edition, _ = Edition.objects.get_or_create(name="People's Choice: Robbed2 Semi 2", year=0)
    for entry in injusticia_2_entries_2:
        split = entry.split("\t")
        year = split[0]
        country = split[1]
        artist = split[2]
        song = split[3]
        code = split[4].lower()
        e = Entry(artist=artist, title=song, code=code, year=year,country=country)
        entries.append(e)
    Entry.objects.bulk_create(entries)


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0007_apply_first_edition'),
    ]

    operations = [RunPython(create_entries_1), RunPython(create_entries_2)]
