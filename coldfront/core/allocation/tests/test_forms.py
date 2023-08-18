import logging

from django.test import TestCase

from coldfront.core.resource.models import Resource
from coldfront.core.allocation.forms import (
    AllocationForm,
    AllocationUpdateForm,
)
from coldfront.core.test_helpers.factories import (
    setup_models,
    ResourceTypeFactory,
)


logging.disable(logging.CRITICAL)

UTIL_FIXTURES = [
    "coldfront/core/test_helpers/test_data/test_fixtures/ifx.json",
]

class AllocationFormBaseTest(TestCase):
    """Base class for allocation view tests."""

    fixtures = UTIL_FIXTURES

    @classmethod
    def setUpTestData(cls):
        """Test Data setup for all allocation view tests."""
        setup_models(cls)

    def return_cleaned_form(self, FormClass):
        form = FormClass(
            data=self.post_data, request_user=self.pi_user, project_pk=self.project.pk
        )
        form.is_valid()
        form_cleaned = form.clean()
        return form_cleaned


class AllocationFormTest(AllocationFormBaseTest):
    """Tests for the AllocationCreateView"""

    def setUp(self):
        tier_restype = ResourceTypeFactory(name='Storage Tier')
        self.post_data = {
            'justification': 'test justification',
            'quantity': '1',
            'offer_letter_code': '123-12312-3123-123123-123123-1231-23123',
            'resource': f'{self.proj_allocation.resources.first().pk}',
            'tier': Resource.objects.filter(resource_type=tier_restype).first()
        }

    def test_allocationform_offerlettercode_invalid(self):
        """ensure correct error messages for incorrect offer_letter_code value
        """
        self.post_data['offer_letter_code'] = '123456789'
        form = AllocationForm(data=self.post_data, request_user=self.pi_user, project_pk=self.project.pk)
        self.assertEqual(
            form.errors['offer_letter_code'], ['Input must contain exactly 33 digits.']
        )

    def test_allocationform_offerlettercode_valid(self):
        """Test POST to the AllocationCreateView
        - ensure 33-digit codes go through
        - ensure correctly entered codes get properly formatted
        """
        # correct # of digits with no dashes
        cleaned_form = self.return_cleaned_form(AllocationForm)
        self.assertEqual(
            cleaned_form['offer_letter_code'], '123-12312-3123-123123-123123-1231-23123'
        )

    def test_allocationform_offerlettercode_valid2(self):
        # check that offer code was correctly formatted
        # correct # of digits with many dashes
        self.post_data['offer_letter_code'] = '123-' * 11
        cleaned_form = self.return_cleaned_form(AllocationForm)

        self.assertEqual(
            cleaned_form['offer_letter_code'], '123-12312-3123-123123-123123-1231-23123'
        )

    def test_allocationform_offerlettercode_valid3(self):
        """Test POST to the AllocationCreateView
        - ensure xes count as digits
        """
        # correct # of digits with no dashes
        self.post_data['offer_letter_code'] = '1Xx-' * 11
        cleaned_form = self.return_cleaned_form(AllocationForm)
        print(cleaned_form)
        self.assertEqual(
            cleaned_form['offer_letter_code'], '1Xx-1Xx1X-x1Xx-1Xx1Xx-1Xx1Xx-1Xx1-Xx1Xx'
        )

    def test_allocationform_offerlettercode_multiplefield_invalid(self):
        """Test POST to AllocationCreateView in circumstance where hsph and seas values are also checked"""
        self.post_data['offer_letter_code'] = '123-' * 11
        self.post_data['hsph_code'] = True
        form = AllocationForm(
            data=self.post_data, request_user=self.pi_user, project_pk=self.project.pk
        )
        self.assertEqual(form.errors['offer_letter_code'], ["you must select exactly one from hsph, seas, or manual entry"])


class AllocationUpdateFormTest(AllocationFormBaseTest):
    """Tests for the AllocationNoteCreateView"""

    def setUp(self):
        self.post_data = {
            'resource': self.proj_allocation.resources.first(),
            'status': 'Active',
        }
