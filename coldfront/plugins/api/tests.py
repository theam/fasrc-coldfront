from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from coldfront.core.test_helpers.factories import setup_models, AllocationFactory
from coldfront.core.allocation.models import Allocation
from coldfront.core.project.models import Project


class ColdfrontAPI(APITestCase):
    """Tests for the Coldfront rest API"""

    fixtures = [
        "coldfront/core/test_helpers/test_data/test_fixtures/ifx.json",
    ]

    @classmethod
    def setUpTestData(cls):
        """Create some test data"""
        setup_models(cls)
        cls.additional_allocations = [
            AllocationFactory() for i in list(range(50))
        ]

    def test_requires_login(self):
        """Test that the API requires authentication"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allocation_api_permissions(self):
        """Test that accessing the allocation API view as an admin returns all
        allocations, and that accessing it as a user returns only the allocations
        for that user"""
        # login as admin
        self.client.force_login(self.admin_user)
        response = self.client.get('/api/allocations/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Allocation.objects.all().count())

        self.client.force_login(self.pi_user)
        response = self.client.get('/api/allocations/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_project_api_permissions(self):
        """Confirm permissions for project API:
        admin user should be able to access everything
        Projectusers should be able to access only their projects
        """
        # login as admin
        self.client.force_login(self.admin_user)
        response = self.client.get('/api/projects/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Allocation.objects.all().count())

        self.client.force_login(self.pi_user)
        response = self.client.get('/api/projects/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
