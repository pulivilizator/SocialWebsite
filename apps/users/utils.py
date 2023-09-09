
from .models import *

def create_profile(backend, user, *args, **kwargs):
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)