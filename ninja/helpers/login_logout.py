from ..models import User

def user_exists(username):
    return User.objects.filter(username=username).exists()
