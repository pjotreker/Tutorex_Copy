from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class ConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))


account_invitation_token = ConfirmationTokenGenerator()
