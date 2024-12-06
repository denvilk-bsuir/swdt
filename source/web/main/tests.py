import pytest
from django.contrib.auth import get_user_model

from main.models import Profile

User = get_user_model()

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('user', 'user@mail.com', 'password')
    assert User.objects.count() == 1
    assert Profile.objects.count() == 1