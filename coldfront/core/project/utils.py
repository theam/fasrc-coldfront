from datetime import date

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from ifxbilling.models import BillingRecord

from coldfront.plugins.ifx.models import ProjectOrganization


def add_project_status_choices(apps, schema_editor):
    ProjectStatusChoice = apps.get_model('project', 'ProjectStatusChoice')

    for choice in ['New', 'Active', 'Archived', ]:
        ProjectStatusChoice.objects.get_or_create(name=choice)


def add_project_user_role_choices(apps, schema_editor):
    ProjectUserRoleChoice = apps.get_model('project', 'ProjectUserRoleChoice')

    for choice in ['User', 'Manager', ]:
        ProjectUserRoleChoice.objects.get_or_create(name=choice)


def add_project_user_status_choices(apps, schema_editor):
    ProjectUserStatusChoice = apps.get_model('project', 'ProjectUserStatusChoice')

    for choice in ['Active', 'Pending - Remove', 'Denied', 'Removed', ]:
        ProjectUserStatusChoice.objects.get_or_create(name=choice)

def generate_usage_history_graph(project):
    '''Create a billing record graph for a project.

    '''
    current_year = date.today().year
    previous_year = current_year - 1
    current_month = date.today().month

    # sort billing_records by year/month
    year_months = [(previous_year, month) for month in range(current_month, 13)] + [(current_year, month) for month in range(1, current_month+1)]
    allocations = project.allocation_set.all()
    columns = []
    for allocation in allocations:
        allocation_res = allocation.get_parent_resource.name
        allocation_billing_records = BillingRecord.objects.filter(
                (Q(year=current_year) | Q(year=previous_year, month__gte=current_month)),
                product_usage__product__product_name=allocation_res,
                account__organization=ProjectOrganization.objects.get(project=project).organization,
            )
        allocation_column = [allocation_res]
        projection = False
        for year_month in year_months:
            year = year_month[0]
            month = year_month[1]
            ym_records = allocation_billing_records.filter(year=year, month=month)
            if year == current_year and month == current_month and ym_records.count() == 0:
                projection = True
                ym_cost = allocation.cost
            else:
                ym_cost = float(sum(r.decimal_charge for r in ym_records))

            allocation_column.append(ym_cost)
        columns.append(allocation_column)

    if not projection:
        columns.append(['month'] + [f'{ym[1]}/{ym[0]}' for ym in year_months])
    else:
        columns.append(['month'] +
                [f'{ym[1]}/{ym[0]}' for ym in year_months[:-1]] +
                [f'{current_month}/{current_year} (PROJECTED)'])

    data = {
        "x": "month",
        "columns": columns,
        "type": "bar",
        "order": "null",
        "groups": [[ allocation.get_parent_resource.name for allocation in allocations
                ]],
    }

    return data
