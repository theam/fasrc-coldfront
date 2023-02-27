import unittest

from django.db.models import Count
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from coldfront.core.test_helpers import utils
from coldfront.core.allocation.models import (Allocation,
                                AllocationAttribute,
                                AllocationChangeRequest)

FIXTURES = [
        "coldfront/core/test_helpers/test_data/test_fixtures/resources.json",
        "coldfront/core/test_helpers/test_data/test_fixtures/poisson_fixtures.json",
        "coldfront/core/test_helpers/test_data/test_fixtures/admin_fixtures.json",
        "coldfront/core/test_helpers/test_data/test_fixtures/all_res_choices.json",
        "coldfront/core/test_helpers/test_data/test_fixtures/field_of_science.json",
        "coldfront/core/test_helpers/test_data/test_fixtures/project_choices.json",
        ]


class AllocationQC(unittest.TestCase):
    def check_resource_quotas(self):
        zero_quotas = AllocationAttribute.objects.filter(
                            allocation_attribute_type__in=[1,5], value=0)
        self.assertEqual(zero_quotas.count(), 0)

    def check_resource_counts(self):
        over_one = Allocation.objects.annotate(resource_count=Count('resources')).filter(resource_count__gt=1)
        self.assertEqual(over_one.count(), 0)


class AllocationListViewTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.admin_user = get_user_model().objects.get(username="gvanrossum")
        self.project_admin_allocation_user = get_user_model().objects.get(username='sdpoisson')
        self.client = Client()

    def test_allocation_list_access(self):
        """Confirm that allocation-list renders correctly
        """
        # no login means redirect
        utils.test_logged_out_redirect_to_login(self, "/allocation/")


        # confirm that show_all_allocations=on enables admin to view all allocations
        self.client.force_login(self.admin_user,
                    backend="django.contrib.auth.backends.ModelBackend")
        response = self.client.get("/allocation/?show_all_allocations=on")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['allocation_list'], 1)

        # confirm that show_all_allocations=on is accessible to non-admin but
        # contains only the user's allocations
        self.client.force_login(self.project_admin_allocation_user, backend="django.contrib.auth.backends.ModelBackend")
        response = self.client.get("/allocation/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['allocation_list'], 1)




class AllocationChangeDetailViewTest(TestCase):

    fixtures = FIXTURES

    def setUp(self):
        """create an AllocationChangeRequest to test
        """
        self.test_user1 = get_user_model().objects.get(username='gvanrossum')
        self.test_user2 = get_user_model().objects.get(username='sdpoisson')
        self.client = Client()
        self.client.force_login(self.test_user1, backend="django.contrib.auth.backends.ModelBackend")
        AllocationChangeRequest.objects.create(pk=2, allocation_id=1, status_id=1,
                        justification="Test.").save()

    def test_allocationchangedetailview_access(self):
        response = self.client.get(reverse('allocation-change-detail', kwargs={'pk':2}))
        self.assertEqual(response.status_code, 200)

    def test_allocationchangedetailview_post_deny(self):
        param = {'choice': 'deny'}
        response = self.client.post(reverse('allocation-change-detail', kwargs={'pk':2}),
        param, follow=True)
        self.assertEqual(response.status_code, 200)
        alloc_change_req = AllocationChangeRequest.objects.get(pk=2)
        self.assertEqual(alloc_change_req.status_id, 3)

    def test_allocationchangedetailview_post_approve(self):
        # with nothing changed, should get error message of "You must make a change to the allocation."
        param = {'choice': 'approve'}
        response = self.client.post(reverse('allocation-change-detail', kwargs={'pk':2}),
        param, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]), "You must make a change to the allocation.")
        # alloc_change_req = AllocationChangeRequest.objects.get(pk=2)
        # self.assertEqual(alloc_change_req.status_id, 2)


class AllocationChangeViewTest(TestCase):

    fixtures = FIXTURES

    def setUp(self):
        self.admin_user = get_user_model().objects.get(username='gvanrossum')
        self.project_pi = get_user_model().objects.get(username='sdpoisson')
        self.client = Client()
        self.client.force_login(self.admin_user,
                backend="django.contrib.auth.backends.ModelBackend")

    def test_allocationchangeview_access(self):
        """
        """
        kwargs={'pk':1, }
        response = self.client.get('/allocation/1/change-request', kwargs=kwargs)
        # print(response.__dict__)
        self.assertEqual(response.status_code, 200)



class AllocationDetailViewTest(TestCase):

    fixtures = FIXTURES

    def setUp(self):
        self.admin_user = get_user_model().objects.get(username='gvanrossum')
        self.project_pi = get_user_model().objects.get(username='sdpoisson')
        self.project_user_non_allocation_user = get_user_model().objects.get(username='sdpoisson')
        self.allocation_user = get_user_model().objects.get(username='snewcomb')
        self.client = Client()

    def test_allocation_detail_access(self):
        # check that login is required
        utils.test_logged_out_redirect_to_login(self, "/allocation/1/")
        # check access for admin
        self.client.force_login(self.admin_user,
                backend="django.contrib.auth.backends.ModelBackend")
        response = self.client.get('/allocation/1/')
        self.assertEqual(response.status_code, 200)
        # check access for existing project pi
        self.client.force_login(self.project_pi,
                backend="django.contrib.auth.backends.ModelBackend")
        response = self.client.get('/allocation/1/')
        self.assertEqual(response.status_code, 200)
        # check access for project user who isn't allocation user
        # check access for allocation user with "Removed" status


    def test_allocation_detail_template_value_render(self):
        """Confirm that quota_tb and usage_tb are correctly rendered in the
        generated AllocationDetailView
        """
        self.client.force_login(self.admin_user,
                backend="django.contrib.auth.backends.ModelBackend")
        response = self.client.get('/allocation/1/')
        self.assertEqual(response.status_code, 200)
        # check that allocation_quota_tb has value
        self.assertEqual(response.context['allocation_quota_bytes'], 109951162777600)
        # check that allocation_usage_tb has value
        self.assertEqual(response.context['allocation_usage_bytes'], 10995116277760)
