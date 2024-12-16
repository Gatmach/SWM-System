from django.core.mail import send_mail
from twilio.rest import Client

def send_email_notification(bin_location, status):
    subject = f"Bin Status Alert: {bin_location}"
    message = f"The bin at {bin_location} is currently {status}. Please take action."
    from_email = 'your_email@example.com'
    recipient_list = ['recipient_email@example.com']
    send_mail(subject, message, from_email, recipient_list)

def send_sms_notification(bin_location, status):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"The bin at {bin_location} is currently {status}.",
        from_='+1234567890',  # Twilio phone number
        to='+0987654321'      # Recipient phone number
    )


