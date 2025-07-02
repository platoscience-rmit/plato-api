from django.core.mail import send_mail
from apps.users.models.user_model import User

class EmailService:
    def verify_email(self, token):
        try:
            user = User.objects.get(verification_token=token)
            if user.is_verification_code_valid(token):
                user.is_verified = True
                user.verification_code_expires = None
                user.save()
                return True, "Email verified successfully"
            else:
                return False, "Invalid or expired verification token"
        except User.DoesNotExist:
            return False, "Invalid verification token"

    def send_verification_email(self, user):
        token = user.generate_verification_code()
        verification_url = f"/verify-email?token={token}"

        subject = "Verify your email address"
        message = f"""
        Hi {user.first_name or 'User'},
        
        Please click the link below to verify your email address:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        """

        send_mail(
            subject=subject,
            message=message,
            from_email='123',
            recipient_list=[user.email],
            fail_silently=False,
        )

    def resend_verification_email(self, user):
        if not user.is_verified:
            self.send_verification_email(user)
            return True, "Verification email resent successfully"
        return False, "User is already verified"
