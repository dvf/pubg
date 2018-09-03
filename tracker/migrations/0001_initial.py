# Generated by Django 2.1.1 on 2018-09-03 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('remote_id', models.UUIDField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('remote_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('matches', models.ManyToManyField(to='tracker.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Shard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='player',
            name='shards',
            field=models.ManyToManyField(to='tracker.Shard'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['name', 'remote_id'], name='tracker_pla_name_49bc17_idx'),
        ),
    ]
