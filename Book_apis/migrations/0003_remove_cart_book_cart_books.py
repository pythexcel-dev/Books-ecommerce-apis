# Generated by Django 4.2.2 on 2023-07-03 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book_apis', '0002_rename_publishdate_book_publish_date_cart_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='book',
        ),
        migrations.AddField(
            model_name='cart',
            name='books',
            field=models.ManyToManyField(to='Book_apis.book'),
        ),
    ]
