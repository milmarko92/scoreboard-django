# Generated by Django 3.1.3 on 2020-11-14 18:52

from django.db import migrations, models
from django.db.migrations import RunPython

from myproject.inputs.pc_nf_1 import pc_nf_1_semi_1


def create_entries(apps, schema_editor):
    Edition = apps.get_model("myproject", "Edition")
    Vote = apps.get_model("myproject", "Vote")
    edition, _ = Edition.objects.get_or_create(name="People's Choice: Robbed Semi 1", year=0)
    all_votes = Vote.objects.all()
    for vote in all_votes:
        vote.edition = edition
    Vote.objects.bulk_update(all_votes, ['edition'])


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0006_vote_edition'),
    ]

    operations = [RunPython(create_entries)]