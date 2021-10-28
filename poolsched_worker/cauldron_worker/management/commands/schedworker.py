import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now

from poolsched import schedworker
from cauldron_apps.poolsched_git.models import IGitAutoRefresh
from cauldron_apps.poolsched_github.models import IGHRepoAutoRefresh, IGHIssueAutoRefresh, IGH2IssueAutoRefresh
from cauldron_apps.poolsched_gitlab.models import IGLIssueAutoRefresh, IGLMergeAutoRefresh
from cauldron_apps.poolsched_meetup.models import IMeetupAutoRefresh
from cauldron_apps.poolsched_merge_identities.models import IMergeIdentities

User = get_user_model()


class Command(BaseCommand):
    help = 'Run the scheduler worker'

    AUTOREFRESH = [
        'poolsched_git.IGitAutoRefresh',
        'poolsched_github.IGHIssueAutoRefresh',
        'poolsched_github.IGHRepoAutoRefresh',
        'poolsched_github.IGH2IssueAutoRefresh',
        'poolsched_gitlab.IGLIssueAutoRefresh',
        'poolsched_gitlab.IGLMergeAutoRefresh',
        'poolsched_meetup.IMeetupAutoRefresh',
        'poolsched_merge_identities.IMergeIdentities',
    ]
    BASE_INTENTIONS = [
        'poolsched_twitter.ITwitterNotify',
        'poolsched_sbom.IParseSPDX',
        'cauldron.IAddGHOwner',
        'cauldron.IAddGLOwner',
        'cauldron_actions.IRefreshActions',
        'poolsched_export.IExportCSV',
        'poolsched_export.IReportKbn',
        'poolsched_export.ICommitsByMonth',
        'poolsched_github.IGHEnrich',
        'poolsched_gitlab.IGLEnrich',
        'poolsched_git.IGitEnrich',
        'poolsched_meetup.IMeetupEnrich',
        'poolsched_stackexchange.IStackExchangeEnrich',
        'poolsched_github.IGHRaw',
        'poolsched_gitlab.IGLRaw',
        'poolsched_git.IGitRaw',
        'poolsched_meetup.IMeetupRaw',
        'poolsched_stackexchange.IStackExchangeRaw',
    ]

    def _create_autorefresh_intentions(self):
        next_autorefresh = now() + datetime.timedelta(hours=1)
        models = [IGitAutoRefresh, IGHRepoAutoRefresh, IGHIssueAutoRefresh, IGH2IssueAutoRefresh,
                  IGLIssueAutoRefresh, IGLMergeAutoRefresh, IMeetupAutoRefresh, IMergeIdentities]
        u, created = User.objects.get_or_create(username='admin_poolsched', defaults={'first_name': 'admin_poolsched'})
        if created:
            u.set_unusable_password()
        for model in models:
            try:
                model.objects.get_or_create(defaults={'scheduled': next_autorefresh, 'user': u})
            except model.MultipleObjectsReturned:
                pass

    def handle(self, *args, **options):
        if settings.SORTINGHAT:
            intentions = self.AUTOREFRESH + self.BASE_INTENTIONS
            self._create_autorefresh_intentions()
        else:
            intentions = self.BASE_INTENTIONS
        intention_order = [apps.get_model(intention) for intention in intentions]
        schedworker.SchedWorker(run=True, intention_order=intention_order)
