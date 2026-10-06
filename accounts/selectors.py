from .models import User


def get_user_by_id(*,pk):
    return User.objects.filter(id= pk).first()

def get_user_by_email(*,email):

    return User.objects.filter(email = email).first()


def get_user_all():
    return User.objects.all()

