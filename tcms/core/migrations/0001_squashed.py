# Generated by Django 2.0.7 on 2018-07-25 14:28

from django.db import migrations


def forwards_add_initial_data(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name='Administrator'),
        Group(name='Tester'),
    ])

    Site = apps.get_model('sites', 'Site')
    Site.objects.create(name='localhost', domain='127.0.0.1:8000')


def reverse_remove_initial_data(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Administrator', 'Tester']).delete()

    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(name='localhost').delete()


def forwards_add_default_perms(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    admin = Group.objects.get(name='Administrator')
    all_perms = Permission.objects.all()
    admin.permissions.add(*all_perms)

    tester = Group.objects.get(name='Tester')
    # apply all permissions for test case & product management
    for app_name in ['django_comments', 'management', 'testcases', 'testplans', 'testruns']:
        app_perms = Permission.objects.filter(content_type__app_label__contains=app_name)
        tester.permissions.add(*app_perms)


def reverse_remove_default_perms(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    admin = Group.objects.get(name='Administrator')
    admin.permissions.clear()

    tester = Group.objects.get(name='Tester')
    tester.permissions.clear()


class Migration(migrations.Migration):

    replaces = [('core', '0001_django_comments__object_pk'),
                ('core', '0002_add_initial_data'),
                ('core', '0003_add_default_permissions_to_groups')]

    initial = True

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_add_initial_data,
            reverse_code=reverse_remove_initial_data,
        ),
        migrations.RunPython(
            code=forwards_add_default_perms,
            reverse_code=reverse_remove_default_perms,
        ),
    ]
