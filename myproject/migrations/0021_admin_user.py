from django.db import migrations


def createsuperuser(apps, schema_editor):

   admin_password = "admin"

   from django.contrib.auth.models import User
   User.objects.create_superuser("admin", password=admin_password)


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0020_all_stars_2'),
    ]

    operations = [
        migrations.RunPython(createsuperuser)
    ]