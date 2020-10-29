import base64
import mimetypes
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from postmark.core import PMMail
from sendgrid import SendGridAPIClient
from sendgrid.helpers import mail

from church.models import ServicePage, User


# sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)


def send_bulletin(users):
    guest_next_service_link = User.get_guest_next_service_link()

    for user in users:
        # Skip sending to users without emails
        if not user.email:
            continue
        message = mail.Mail(
            to_emails=[(user.email, f"{user.first_name} {user.last_name}")],
        )
        message.from_email = mail.From("lynn@crossroadsajax.church", "Lynn Jackson")
        message.dynamic_template_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            stream_link=user.get_next_service_link(),
            guest_stream_link=guest_next_service_link,
            services_link=user.get_services_link(),
            offering_link=f"https://crossroadsajax.church/offering?mem={user.token}",
        )
        message.template_id = settings.EMAIL_TEMPLATE.BULLETIN
        sendgrid_client.send(message)


def _find_attachments(date: str):
    # Find attachments for the given date
    # They should be placed in the directory static/attachments/<YYYY><MM><DD>
    path = finders.find(f"attachments/{date}")

    if not path:
        return []

    files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]
    return files


def send_service(users):
    service_page = ServicePage.current_service_page()
    guest_next_service_link = User.get_guest_next_service_link()

    attachments = []
    for f in service_page.email_attachments:
        with f.file as file:
            data = file.read()

        encoded_file = base64.b64encode(data).decode()
        attachments.append(encoded_file)

    for user in users:
        # Skip sending to users without emails
        if not user.email:
            continue

        m = PMMail(
            to=f"{user.first_name} {user.last_name} <{user.email}>",
            sender="Lynn Jackson lynn@crossroadsajax.church",
            template_id="19602506",
            template_model=dict(
                company_name="Crossroads Church",
                company_address="520 Westney Rd S, Ajax, ON L1S 6W6",
                first_name=user.first_name,
                last_name=user.last_name,
                date=service_page.date.strftime("%A %B %d, %Y"),
                stream_link=user.get_next_service_link(),
                guest_stream_link=guest_next_service_link,
                services_link=user.get_services_link(),
                foreword=service_page.description,  # Note that this is HTML
            ),
        )
        # TODO: add attachments again
        # message.add_attachment(a)
        m.send()


def send_service_sendgrid(users):
    service_page = ServicePage.current_service_page()
    guest_next_service_link = User.get_guest_next_service_link()

    attachments = []
    for f in service_page.email_attachments:
        with f.file as file:
            data = file.read()

        encoded_file = base64.b64encode(data).decode()
        attachments.append(
            mail.Attachment(
                mail.FileContent(encoded_file),
                mail.FileName(os.path.basename(f.name)),
                mail.FileType(mimetypes.guess_type(f.name)[0]),
                mail.Disposition("attachment"),
            )
        )

    for user in users:
        # Skip sending to users without emails
        if not user.email:
            continue
        message = mail.Mail(
            to_emails=[(user.email, f"{user.first_name} {user.last_name}")],
        )
        message.from_email = mail.From("lynn@crossroadsajax.church", "Lynn Jackson")
        message.dynamic_template_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            date=service_page.date.strftime("%A %B %d, %Y"),
            stream_link=user.get_next_service_link(),
            guest_stream_link=guest_next_service_link,
            services_link=user.get_services_link(),
            foreword=service_page.description,  # Note that this is HTML
        )
        message.template_id = settings.EMAIL_TEMPLATE.SERVICE
        for a in attachments:
            message.add_attachment(a)
        sendgrid_client.send(message)
