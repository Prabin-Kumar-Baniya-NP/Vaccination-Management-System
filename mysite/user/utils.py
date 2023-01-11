from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generates token for email verification
    """
    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email = user.email
        return f"VerifyEmail-{user.pk}{user.password}{login_timestamp}{timestamp}{email}{user.is_active}"

EmailVerificationTokenGenerator = TokenGenerator()