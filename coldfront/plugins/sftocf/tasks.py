from coldfront.plugins.sftocf import utils
from django.core import management

def pull_sf_push_cf():
    management.call_command('pull_sf_push_cf')


def pull_resource_data():
    utils.pull_resource_data()
