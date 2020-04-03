from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, ReplyTo

from church.models import ServicePage


sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)


def send_bulletin(users):
    service_page = ServicePage.current_service_page()

    stream_link = f"https://crossroadsajax.church{service_page.url}"

    # to_emails = [
    #     To(
    #         email=user.email,
    #         name=f"{user.first_name} {user.last_name}",
    #         substitutions=dict(
    #             name=f"{user.first_name} {user.last_name}",
    #             stream_link=f"{stream_link}?mem={user.token}",
    #         ),
    #     )
    #     for user in users
    # ]

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
            stream_link=f"{stream_link}?mem={user.token}",
        )
        message.template_id = settings.EMAIL_TEMPLATE.BULLETIN
        sendgrid_client.send(message)
