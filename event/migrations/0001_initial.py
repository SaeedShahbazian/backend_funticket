# Generated by Django 5.1.2 on 2024-10-19 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
        ('funticket', '__first__'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('meta_title', models.CharField(blank=True, max_length=200, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('aparat_trailer', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('theater', 'Theater'), ('cinema', 'Cinema')], default='theater', max_length=10)),
                ('weight', models.FloatField(default=0.0)),
                ('event_rate', models.FloatField(default=0)),
                ('rate_sum_cache', models.FloatField(default=0)),
                ('rate_count_cache', models.BigIntegerField(default=0)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('users_rating', models.FloatField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_background', to='media.image')),
                ('images', models.ManyToManyField(blank=True, related_name='image_events', to='media.image')),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_poster', to='media.image')),
                ('rates', models.ManyToManyField(blank=True, related_name='reate_events', to='funticket.rate')),
                ('threads', models.ManyToManyField(blank=True, related_name='thread_events', to='comment.thread')),
                ('videos', models.ManyToManyField(blank=True, related_name='video_events', to='media.video')),
                ('genres', models.ManyToManyField(blank=True, related_name='genre_event', to='event.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('profile_photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='media.image')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EventsActors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1000)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_actors', to='event.event')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_event_actors', to='event.person')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='actors_event', through='event.EventsActors', to='event.person'),
        ),
        migrations.AddField(
            model_name='event',
            name='directors',
            field=models.ManyToManyField(blank=True, related_name='directors_event', to='event.person'),
        ),
        migrations.AddField(
            model_name='event',
            name='producers',
            field=models.ManyToManyField(blank=True, related_name='producers_event', to='event.person'),
        ),
        migrations.AddField(
            model_name='event',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='writers_event', to='event.person'),
        ),
        migrations.CreateModel(
            name='EventRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_roles', to='event.event')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_roles_event', to='event.person')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles_event', to='event.role')),
            ],
        ),
    ]