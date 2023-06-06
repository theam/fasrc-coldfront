"""Department views"""

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, Q
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from coldfront.core.utils.views import ColdfrontListView, NoteCreateView, NoteUpdateView
from coldfront.core.allocation.models import Allocation, AllocationUser
from coldfront.core.department.forms import DepartmentSearchForm
from coldfront.core.department.models import (
    Department,
    DepartmentMember,
    DepartmentUserNote,
)

def return_department_roles(user, department):
    """Return list of a user's permissions for the specified department.
    possible roles are: manager, pi, or member.
    """
    member_conditions = (Q(active=1) & Q(user=user))
    if not department.useraffiliation_set.filter(member_conditions).exists():
        return ()

    permissions = ['user']
    for role in ['approver', 'pi', 'lab_manager']:
        if department.members.filter(member_conditions & Q(role=role)).exists():
            permissions.append(role)

    return permissions


class DepartmentListView(ColdfrontListView):
    model = Department
    template_name = 'department/department_list.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        order_by = self.return_order()

        department_search_form = DepartmentSearchForm(self.request.GET)
        departments = Department.objects.all()  # values()
        user_depts = DepartmentMember.objects.filter(user=self.request.user)
        if department_search_form.is_valid():
            data = department_search_form.cleaned_data
            if not data.get('show_all_departments') or not (
                self.request.user.is_superuser
                or self.request.user.has_perm('department.can_view_all_departments')
            ):
                departments = departments.filter(
                    id__in=user_depts.values_list('organization_id')
                )
            # Department and Rank filters name
            for search in ('name', 'rank'):
                if data.get(search):
                    departments = departments.filter(name__icontains=data.get(search))
        else:
            departments = departments.filter(
                id__in=user_depts.values_list('organization_id')
            )

        departments = departments.order_by(order_by).distinct()
        return departments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            SearchFormClass=DepartmentSearchForm, **kwargs
        )
        return context


# class DepartmentInvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
#
#     def get_context_data(self, **kwargs):
#         """Create all the variables for allocation_invoice_detail.html"""
#         pk = self.kwargs.get('pk')
#         self.department = get_object_or_404(FieldOfScience, pk=pk)
#
#
#         initial_data = {
#             'status': allocation_objs.first().status,
#         }
#         form = AllocationInvoiceUpdateForm(initial=initial_data)
#         context['form'] = form
#
#         # Can the user update the project?
#         context['is_allowed_to_update_project'] = set_proj_update_permissions(
#                                                     allocation_objs.first(), self.request.user)

#
#         context['ALLOCATION_ENABLE_ALLOCATION_RENEWAL'] = ALLOCATION_ENABLE_ALLOCATION_RENEWAL
#         return context


class DepartmentNoteCreateView(NoteCreateView):
    model = DepartmentUserNote
    fields = '__all__'
    form_obj = 'department'
    object_model = Department

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_page'] = 'department-detail'
        context['object_title'] = f'Department {context["object"].name}'
        return context

    def get_success_url(self):
        return reverse('department-detail', kwargs={'pk': self.kwargs.get('pk')})


class DepartmentNoteUpdateView(NoteUpdateView):
    model = DepartmentUserNote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_object'] = self.object.department
        context['object_detail_link'] = 'department-detail'
        return context

    def get_success_url(self):
        return reverse_lazy('department-detail', kwargs={'pk': self.object.department.pk})

class DepartmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Department Stats, Projects, Allocations, and invoice details."""

    # should a user need to be a member of the department to see this?
    model = Department
    template_name = 'department/department_detail.html'
    context_object_name = 'department'

    def test_func(self):
        """UserPassesTestMixin Tests.
        Allow access if a department member with billing permission.
        """
        if self.request.user.is_superuser:
            return True
        pk = self.kwargs.get('pk')
        department_obj = get_object_or_404(Department, pk=pk)
        if department_obj.members.filter(user=self.request.user).exists():
            return True

        messages.error(
            self.request, 'You do not have permission to view this department.'
        )
        return False

    def return_visible_notes(self, department_obj):
        noteset = department_obj.departmentusernote_set
        notes = (
            noteset.all()
            if self.request.user.is_superuser
            else noteset.filter(is_private=False)
        )
        return notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Can the user update the department?
        department_obj = self.object
        member_permissions = return_department_roles(self.request.user, department_obj)

        if self.request.user.is_superuser or 'approver' in member_permissions:
            context['manager'] = True
            projectview_filter = Q(status__name__in=['New', 'Active'])
        else:
            context['manager'] = False
            projectview_filter = Q(
                status__name__in=['New', 'Active'], projectuser__user=self.request.user
            )

        attribute_filter = (
            Q(
                allocation__allocationattribute__allocation_attribute_type_id=1
            ) & Q(allocation__status_id__in=[1, 2])
        )
        attribute_string = 'allocation__allocationattribute__value'
        project_objs = list(
            department_obj.projects.filter(projectview_filter).annotate(
                total_quota=Sum(attribute_string, filter=attribute_filter)
            )
        )
        child_depts = Department.objects.filter(parents=department_obj)
        if child_depts:
            for dept in child_depts:
                child_projs = list(
                    dept.projects.filter(projectview_filter).annotate(
                        total_quota=Sum(attribute_string, filter=attribute_filter)
                    )
                )
                project_objs.extend(child_projs)

        allocationuser_filter = (Q(status__name='Active') & ~Q(usage_bytes__isnull=True))

        for p in project_objs:
            p.allocs = p.allocation_set.filter(
                allocationattribute__allocation_attribute_type_id=1,
                status__name__in=['Active', 'New'],
            )
            p.total_price = sum(float(a.cost) for a in p.allocs.all())

        context['full_price'] = sum(p.total_price for p in project_objs)
        context['projects'] = project_objs
        context['department'] = department_obj

        allocation_objs = Allocation.objects.filter(
            project_id__in=[o.id for o in project_objs],
            status__name__in=['Active', 'New'],
        )

        context['allocations_count'] = allocation_objs.count()

        allocation_users = AllocationUser.objects.filter(
            Q(allocation_id__in=[o.id for o in allocation_objs]) & allocationuser_filter
        ).order_by('user__username')

        context['allocation_users'] = allocation_users
        context['notes'] = self.return_visible_notes(department_obj)
        context['note_update_link'] = 'department-note-update'

        try:
            context['ondemand_url'] = settings.ONDEMAND_URL
        except AttributeError:
            pass
        return context
