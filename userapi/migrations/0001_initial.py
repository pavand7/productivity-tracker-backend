# Generated by Django 3.2.14 on 2022-08-25 09:28

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import userapi.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('badgeID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('isNewUser', models.BooleanField(default=True)),
                ('userName', models.CharField(max_length=20, unique=True)),
                ('lastWeekProductivity', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=userapi.models.last_week_productivity_default, size=7)),
                ('badges', models.ManyToManyField(blank=True, related_name='users', to='userapi.Badge')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postID', models.AutoField(primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('timestamp', models.BigIntegerField()),
                ('numLikes', models.BigIntegerField(default=0)),
                ('numComments', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='userapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='userapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventID', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('start_time', models.BigIntegerField()),
                ('end_time', models.BigIntegerField()),
                ('date', models.CharField(max_length=10)),
                ('users', models.ManyToManyField(related_name='events', to='userapi.User')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentID', models.AutoField(primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('timestamp', models.BigIntegerField()),
                ('numLikes', models.BigIntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userapi.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='PostLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='userapi.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='userapi.user')),
            ],
            options={
                'unique_together': {('post', 'user')},
            },
        ),
        migrations.CreateModel(
            name='CommentLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='userapi.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='userapi.user')),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
    ]
