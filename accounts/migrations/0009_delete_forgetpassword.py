# Generated by Django 3.2.12 on 2022-02-19 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_user_forgetpassword_account'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ForgetPassword',
        ),
    ]
