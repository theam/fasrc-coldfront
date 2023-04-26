from django.test import TestCase
from django.contrib.auth import get_user_model

from coldfront.core.utils.fasrc import read_json
from coldfront.plugins.sftocf.utils import (push_cf,
                                            update_user_usage,
                                            match_allocations_with_usage_entries,
                                            split_num_string
                                            )
from coldfront.core.allocation.models import Allocation

FIXTURES = [
        'coldfront/core/test_helpers/test_data/test_fixtures/field_of_science.json',
        'coldfront/core/test_helpers/test_data/test_fixtures/all_res_choices.json',
        'coldfront/core/test_helpers/test_data/test_fixtures/poisson_fixtures.json',
        'coldfront/core/test_helpers/test_data/test_fixtures/project_choices.json',
        'coldfront/core/test_helpers/test_data/test_fixtures/resources.json',
        ]

class IntegrationTests(TestCase):
    fixtures = FIXTURES
    pref = './coldfront/plugins/sftocf/tests/testdata/'

    def test_push_cf(self):
        content = read_json(f'{self.pref}poisson_lab_holysfdb10.json')
        errors = push_cf(content)
        assert not errors

class UtilTests(TestCase):
    fixtures = FIXTURES
    pref = './coldfront/plugins/sftocf/tests/testdata/'
    dummy_user_usage = [
        {'size_sum': 1046274, 'lab_path': 'C/LABS/poisson_lab', 'vol_name': 'holylfs10', 'user_name': 'sdpoisson'},
        {'size_sum': 20498274, 'lab_path': 'C/LABS/poisson_lab', 'vol_name': 'holylfs10', 'user_name': 'ljbortkiewicz'},
        {'size_sum': 20498274, 'lab_path': 'C/LABS/gordon_lab', 'vol_name': 'holylfs10', 'user_name': 'aalice'}]
    dummy_allocation_usage = [
        {'vol_name': 'holylfs10', 'group_name': 'poisson_lab', 'user_name': 'sdpoisson', 'path': 'C/LABS/poisson_lab', 'total_size': 10749750250},
        {'vol_name': 'holylfs10', 'group_name': 'gordon_lab', 'user_name': 'aalice', 'path': 'C/LABS/gordon_lab', 'total_size': 10749750250}
    ]

    def test_update_user_usage(self):
        content = read_json(f'{self.pref}poisson_lab_holysfdb10.json')
        statdicts = content['contents']
        errors = False
        allocation = Allocation.objects.get(project_id=1)
        for statdict in statdicts:
            try:
                usage_bytes = statdict['size_sum']
                usage, unit = split_num_string(statdict['size_sum_hum'])
                user = get_user_model().objects.get(username=statdict['username'])
                update_user_usage(user, usage_bytes, usage, unit, allocation)
            except Exception as e:
                print('ERROR:', e)
                errors = True
        assert not errors

    def test_match_allocations_with_usage_entries(self):
        '''test match_allocations_with_usage_entries
        '''
        allocations = Allocation.objects.all()
        result = match_allocations_with_usage_entries(allocations, self.dummy_user_usage, self.dummy_allocation_usage)
        desired_dict = {
            'total_usage_entry': {
                'vol_name': 'holylfs10', 'group_name': 'poisson_lab', 'user_name': 'sdpoisson', 'path': 'C/LABS/poisson_lab', 'total_size': 10749750250},
            'allocation': allocations.get(pk=1),
            'volume': 'holylfs10',
            'path': 'C/LABS/poisson_lab',
            'user_usage_entries': [
                {'size_sum': 1046274, 'lab_path': 'C/LABS/poisson_lab', 'vol_name': 'holylfs10', 'user_name': 'sdpoisson'},
                {'size_sum': 20498274, 'lab_path': 'C/LABS/poisson_lab', 'vol_name': 'holylfs10', 'user_name': 'ljbortkiewicz'}]
            }
        self.assertEqual(result[0].__dict__, desired_dict)