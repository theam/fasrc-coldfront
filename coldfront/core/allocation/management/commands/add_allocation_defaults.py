from django.core.management.base import BaseCommand

from coldfront.core.allocation.models import (AttributeType,
                                              AllocationAttributeType,
                                              AllocationStatusChoice,
                                              AllocationChangeStatusChoice,
                                              AllocationUserStatusChoice)


class Command(BaseCommand):
    help = 'Add default allocation related choices'

    def handle(self, *args, **options):

        for attribute_type in ('Date', 'Float', 'Int', 'Text', 'Yes/No', 'No',
            'Attribute Expanded Text'):
            AttributeType.objects.get_or_create(name=attribute_type)

        for choice in ('Active', 'Denied', 'Expired',
                       'New', 'Paid', 'Payment Pending',
                       'Payment Requested', 'Payment Declined',
                       'Renewal Requested', 'Revoked', 'Unpaid',):
            AllocationStatusChoice.objects.get_or_create(name=choice)

        for choice in ('Pending', 'Approved', 'Denied',):
            AllocationChangeStatusChoice.objects.get_or_create(name=choice)

        for choice in ('Active', 'Error', 'Removed', ):
            AllocationUserStatusChoice.objects.get_or_create(name=choice)

        for name, attribute_type, has_usage, is_private in (
            # FASRC defaults
            ('Storage Quota (TB)', 'Float', True, False),
            ('Quota_In_Bytes', 'Float', True, False),
            ('UseStarFishZone', 'Yes/No', False, True),
            ('Offer Letter', 'Float', False, True),
            ('RequiresPayment', 'Yes/No', False, True),
            ('Offer Letter Code', 'Text', False, True),
            ('Subdirectory', 'Text', False, False),
            ('Heavy IO',  'Yes/No', False, False),
            ('Mounted',  'Yes/No', False, False),
            ('High Security', 'Yes/No', False, False),
            ('DUA', 'Yes/No', False, False),
            ('External Sharing', 'Yes/No', False, False),
            # UBCCR defaults
            # ('Cloud Account Name', 'Text', False, False),
            # ('CLOUD_USAGE_NOTIFICATION', 'Yes/No', False, True),
            # ('Core Usage (Hours)', 'Int', True, False),
            # ('Accelerator Usage (Hours)', 'Int', True, False),
            # ('EXPIRE NOTIFICATION', 'Yes/No', False, True),
            # ('freeipa_group', 'Text', False, False),
            # ('Is Course?', 'Yes/No', False, True),
            ('Paid', 'Float', False, False),
            # ('Paid Cloud Support (Hours)', 'Float', True, True),
            # ('Paid Network Support (Hours)', 'Float', True, True),
            # ('Paid Storage Support (Hours)', 'Float', True, True),
            # ('Purchase Order Number', 'Int', False, True),
            # ('send_expiry_email_on_date', 'Date', False, True),
            # ('slurm_account_name', 'Text', False, False),
            # ('slurm_specs', 'Attribute Expanded Text', False, True),
            # ('slurm_specs_attriblist', 'Text', False, True),
            # ('slurm_user_specs', 'Attribute Expanded Text', False, True),
            # ('slurm_user_specs_attriblist', 'Text', False, True),
            # ('Storage Quota (GB)', 'Int', False, False),
            # ('Storage_Group_Name', 'Text', False, False),
            # ('Tier 0 - $50/TB/yr', 'Text', False, False),
            # ('Tier 1 - $250/TB/yr', 'Text', False, False),
            # ('Tier 2 - $100/TB/yr', 'Text', False, False),
            # ('Tier 3 - $8/TB/yr', 'Text', False, False),
            # ('Tier 0', 'Text', False, False),
            # ('Tier 1', 'Text', False, False),
            # ('Tier 2', 'Text', False, False),
            # ('Tier 3', 'Text', False, False),

        ):
            AllocationAttributeType.objects.get_or_create(name=name, attribute_type=AttributeType.objects.get(
                name=attribute_type), has_usage=has_usage, is_private=is_private)
