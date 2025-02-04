from argparse import ArgumentParser
from typing import Any

from django.db import transaction

from zerver.lib.management import ZulipBaseCommand
from zilencer.models import RemoteZulipServer, RemoteZulipServerAuditLog


class Command(ZulipBaseCommand):
    help = """Add a remote Zulip server for push notifications."""

    def add_arguments(self, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("command-specific arguments")
        group.add_argument("uuid", help="the user's `zulip_org_id`")
        group.add_argument("key", help="the user's `zulip_org_key`")
        group.add_argument(
            "--hostname", "-n", required=True, help="the hostname, for human identification"
        )
        group.add_argument("--email", "-e", required=True, help="a contact email address")

    def handle(self, *args: Any, **options: Any) -> None:
        with transaction.atomic():
            remote_server = RemoteZulipServer.objects.create(
                uuid=options["uuid"],
                api_key=options["key"],
                hostname=options["hostname"],
                contact_email=options["email"],
            )
            RemoteZulipServerAuditLog.objects.create(
                event_type=RemoteZulipServerAuditLog.REMOTE_SERVER_CREATED,
                server=remote_server,
                event_time=remote_server.last_updated,
            )
