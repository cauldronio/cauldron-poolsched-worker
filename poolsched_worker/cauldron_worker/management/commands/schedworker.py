from django.core.management.base import BaseCommand
from django.apps import apps

from poolsched import schedworker


class Command(BaseCommand):
    help = 'Run the scheduler worker'

    INTENTION_ORDER = [
        'poolsched_github.IGHEnrich',
        'poolsched_gitlab.IGLEnrich',
        'poolsched_git.IGitEnrich',
        'poolsched_meetup.IMeetupEnrich',
        'poolsched_github.IGHRaw',
        'poolsched_gitlab.IGLRaw',
        'poolsched_git.IGitRaw',
        'poolsched_meetup.IMeetupRaw',
    ]

    def handle(self, *args, **options):
        # TODO: Define intention order in settings to be customizable for each worker
        intention_order = [apps.get_model(intention) for intention in self.INTENTION_ORDER]
        schedworker.SchedWorker(run=True, intention_order=intention_order)
