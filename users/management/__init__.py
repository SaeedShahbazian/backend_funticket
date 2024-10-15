from django.apps import apps as global_apps
from django.contrib.contenttypes.management import create_contenttypes
from django.db import DEFAULT_DB_ALIAS, router

"""
Admin : Technical
Chief : Office Chief
Support : support or callcenter of office
Content : Data entery in webSite
"""
GROUPS_LIST = ['admin', 'chief', 'support', 'content']
CHIEF_MODELS = [
    ("users", "user"),("geo", "city"),("media", "image"),("media", "video")
]
SUPPORT_MODELS = [
    ("users", "user"), ("geo", "city"),
    ("media", "video"), ("media", "image")
]
CONTENT_MODELS = []

def create_groups(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    if not app_config.models_module:
        return

    # Ensure that contenttypes are created for this app. Needed if
    # 'django.contrib.auth' is in INSTALLED_APPS before
    # 'django.contrib.contenttypes'.
    create_contenttypes(app_config, verbosity=verbosity, interactive=interactive, using=using, apps=apps, **kwargs)

    app_label = app_config.label
    try:
        app_config = apps.get_app_config(app_label)
        Group = apps.get_model('auth', 'Group')
        Permission = apps.get_model('auth', 'Permission')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Permission):
        return

    for group in GROUPS_LIST:
        _, created = Group.objects.using(using).get_or_create(name=group)
        if verbosity >= 2:
            if created:
                print('Adding groups {}'.format(group))
            else:
                print('Group {} already exists'.format(group))

    # Admin
    Group.objects.using(using).get(name='admin').permissions.add(
        *Permission.objects.all()
    )

    # Chief
    for dic in CHIEF_MODELS:
        Group.objects.using(using).get(name='chief').permissions.add(
            *Permission.objects.filter(content_type__app_label=dic[0], content_type__model=dic[1]).all()
        )
    # Support
    for dic in SUPPORT_MODELS:
        Group.objects.using(using).get(name='support').permissions.add(
            *Permission.objects.filter(content_type__app_label=dic[0], content_type__model=dic[1]).all()
        )

    # Content
    for model in CONTENT_MODELS:
        Group.objects.using(using).get(name='content').permissions.add(
            *Permission.objects.filter(content_type__app_label=model).all()
        )
