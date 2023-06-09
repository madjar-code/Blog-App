from enum import Enum
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.request import Request
from six import text_type

from users.models import User


class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> str:
        return text_type(user.id) + text_type(timestamp) + text_type(user.is_verified)


class DeleteAccountTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> str:
        return text_type(user.id) + text_type(timestamp) + text_type(user.is_active)


def send_email_verification(request: Request, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = EmailTokenGenerator().make_token(user)
    domain = get_current_site(request).domain
    link = f'http://{domain}/verify/{uid}/{token}'
    
    try:
        send_mail(subject='Basic App - Activate your account',
                  message=f"Hello {user.username}, please activate your\
                           account by clicking on the link below. \n\
                           {link}\n\n\nIf it's not you, please ignore\
                           this e-mail.",
                  from_email=None, recipient_list=[user.email],
                  fail_silently=False)
    except Exception as e:
        print(e)


def send_email_password_reset(request: Request, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    domain = get_current_site(request).domain
    link = f'http://{domain}/password/reset/{uid}/{token}/'
    
    try:
        send_mail(subject='Basic App - Reset your password',
                  message=f"Hello {user.username}, you can reset your password\
                           by clicking on the link below. \n{link}\n\n\n\
                           If it's not you, immediately change password, your\
                           account might be in thief's hands",
                           from_email=None, recipient_list=[user.email],
                           fail_silently=False)
    except Exception as e:
        print(e)


def send_email_delete_user(request: Request, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = DeleteAccountTokenGenerator().make_token(user)
    domain = get_current_site(request).domain
    link = f'http://{domain}/delete/{uid}/{token}'

    try:
        send_mail(subject='Basic App - Delete your account',
                  message=f"Hello {user.username}, click the link below\
                           to delete your account.\n{link}\n\n\n\
                           If it's not you, immediately change password, your\
                           account might be in thief's hands",
                           from_email=None, recipient_list=[user.email],
                           fail_silently=False)
    except Exception as e:
        print(e)
