from django.db import migrations



def createsuperuser(apps, schema_editor):
    # Create a new user using acquired password
    from django.contrib.auth.models import User
    User.objects.create_superuser("marko", password="admin")


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myproject', "0009_create_nf_injusticia_2_entries")
    ]

    operations = [
        migrations.RunPython(createsuperuser)
    ]