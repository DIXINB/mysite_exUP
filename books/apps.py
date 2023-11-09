from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

class ProfileOfUserConfig(AppConfig):
    name = 'profile_of_user'