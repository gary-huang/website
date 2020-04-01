from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

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
        message = Mail(
            from_email=("kyle@crossroadsajax.church", "Kyle Verhoog"),
            to_emails=[(user.email, f"{user.first_name} {user.last_name}")],
        )
        message.dynamic_template_data = dict(
            name=f"{user.first_name} {user.last_name}",
            stream_link=f"{stream_link}?mem={user.token}",
        )
        message.template_id = settings.EMAIL_TEMPLATE.BULLETIN
        sendgrid_client.send(message)
