# Generated by Django 5.0.1 on 2024-02-14 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_games_pimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('quantity', models.IntegerField(default=1)),
                ('gid', models.ForeignKey(db_column='gid', on_delete=django.db.models.deletion.CASCADE, to='myapp.games')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
