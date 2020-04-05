from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, ReplyTo

from church.models import ServicePage, User


sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)


def send_bulletin(users):
    guest_next_service_link = User.get_guest_next_service_link()

    for user in users:
        # Skip sending to users without emails
        if not user.email:
            continue
        message = Mail(to_emails=[(user.email, f"{user.first_name} {user.last_name}")],)
        message.from_email = From("lynn@crossroadsajax.church", "Lynn Jackson")
        message.reply_to = ReplyTo("lynn@crossroadsinajax.org", "Lynn Jackson")
        message.dynamic_template_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            stream_link=user.get_next_service_link(),
            guest_stream_link=guest_next_service_link,
        )
        message.template_id = settings.EMAIL_TEMPLATE.BULLETIN
        sendgrid_client.send(message)


def send_service(users):
    guest_next_service_link = User.get_guest_next_service_link()

    for user in users:
        # Skip sending to users without emails
        if not user.email:
            continue
        message = Mail(to_emails=[(user.email, f"{user.first_name} {user.last_name}")],)
        message.from_email = From("kyle@crossroadsajax.church", "Kyle Verhoog")
        message.reply_to = ReplyTo("kyle.verhoog@crossroadsinajax.org", "Kyle Verhoog")
        message.dynamic_template_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            stream_link=user.get_next_service_link(),
            guest_stream_link=guest_next_service_link,
        )
        message.template_id = settings.EMAIL_TEMPLATE.SERVICE
        sendgrid_client.send(message)
