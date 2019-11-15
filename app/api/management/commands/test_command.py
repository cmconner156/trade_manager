from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models import TGMessage as Message

class Command(BaseCommand):
    help = 'Just testing stuff'

    def add_arguments(self, parser):
        #Positional arg example
        parser.add_argument('nothing', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        print("settings:%s" % settings)
        print("settings.TELEGRAM: %s" % settings.TELEGRAM)
        tg_api_hash = settings.TELEGRAM['API_HASH']
        if tg_api_hash is not None:
            print("api_hash:%s" % tg_api_hash)
        else:
            print("something is broken")


#        for poll_id in options['poll_ids']:
#            try:
#                poll = Poll.objects.get(pk=poll_id)
#            except Poll.DoesNotExist:
#                raise CommandError('Poll "%s" does not exist' % poll_id)
#
#            poll.opened = False
#            poll.save()
#
#            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))