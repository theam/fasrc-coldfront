import json
import logging
from functools import reduce
from datetime import datetime
import operator

import requests
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone

from coldfront.core.utils.common import import_from_settings
from coldfront.core.field_of_science.models import FieldOfScience
from coldfront.core.project.models import ( Project,
                                            ProjectUserRoleChoice,
                                            ProjectUserStatusChoice,
                                            ProjectStatusChoice,
                                            ProjectUser)
from coldfront.core.resource.models import Resource
from coldfront.core.allocation.models import   (Allocation,
                                                AllocationUser,
                                                AllocationAttribute,
                                                AllocationAttributeType)

today = datetime.today().strftime('%Y%m%d')

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler(f'logs/{today}.log', 'w')
logger.addHandler(filehandler)


def record_process(func):
    '''Wrapper function for logging'''
    def call(*args, **kwargs):
        funcdata = '{} {}'.format(func.__name__, func.__code__.co_firstlineno)
        logger.debug('\n%s START.', funcdata)
        result = func(*args, **kwargs)
        logger.debug('%s END. output:\n%s\n', funcdata, result)
        return result
    return call

class ErrorTracker:
    '''class for tracking errors that arise when processing groupuser data'''
    def __init__(self):
        self.no_members = []
        self.no_users = []
        self.no_managers = []

    def report(self):
        '''report errors'''
        logger.warning('AD groups with no members: %s', self.no_members)
        logger.warning('AD groups with no users: %s', self.no_users)
        logger.warning('AD groups with no managers: %s', self.no_managers)


class AllTheThingsConn:

    def __init__(self):
        self.url = 'https://allthethings.rc.fas.harvard.edu:7473/db/data/transaction/commit'
        self.token = import_from_settings('NEO4JP')
        self.headers = generate_headers(self.token)

    def post_query(self, query):
        resp = requests.post(self.url, headers=self.headers, data=json.dumps(query), verify=False)
        return json.loads(resp.text)

    def format_query_results(self, resp_json):
        result_dicts = list(resp_json['results'])
        return [dict(zip(rdict['columns'],entrydict['row'])) \
                for rdict in result_dicts for entrydict in rdict['data'] ]

    def collect_group_membership(self, groupname):
        '''
        Collect user, and relationship information for a given lab or labs from ATT.
        '''
        query = {'statements': [{
                    'statement': f'MATCH (u:User)-[r:MemberOf|ManagedBy]-(g:Group) \
                    WHERE (g.ADSamAccountName =~ \'{groupname}\') \
                    RETURN \
                    u.ADgivenName AS first_name, \
                    u.ADsurname AS last_name, \
                    u.ADSamAccountName AS user_name, \
                    u.ADenabled AS user_enabled, \
                    g.ADSamAccountName AS group_name,\
                    type(r) AS relationship,\
                    g.ADManaged_By AS group_manager, \
                    u.ADgidNumber AS user_gid_number, \
                    g.ADgidNumber AS group_gid_number'
                }]}
        resp_json = self.post_query(query)
        resp_json_formatted = self.format_query_results(resp_json)
        return resp_json_formatted

    def collect_pi_data(self, grouplist):
        '''collect information on pis for a given list of groups
        '''
        groupnamesearch = "|".join(grouplist)
        query = {'statements': [{
                    'statement': f'MATCH (g:Group)\
                    WITH g\
                    MATCH (u:User)\
                    WHERE (g.ADSamAccountName =~ \'({groupnamesearch})\') \
                    AND u.ADSamAccountName = g.ADManaged_By\
                    RETURN\
                    g.ADSamAccountName AS group_name,\
                    u.ADSamAccountName AS user_name, \
                    u.ADgivenName AS first_name, \
                    u.ADsurname AS last_name, \
                    u.ADmail AS email, \
                    u.ADDepartment AS department, \
                    u.ADTitle AS title, \
                    u.ADCompany AS company, \
                    u.ADParentCanonicalName AS path, \
                    u.DotsPTLUpdateDate, \
                    u.DotsADUpdateDate, \
                    u.ADenabled AS user_enabled, \
                    u.NANInNanites AS in_nanites, \
                    u.ADgidNumber AS user_gid_number'
                }]}
        resp_json = self.post_query(query)
        resp_json_formatted = self.format_query_results(resp_json)
        return resp_json_formatted

    def pull_quota_data(self, volumes=None):
        '''Produce JSON file of quota data for LFS and Isilon from AlltheThings.
        Parameters
        ----------
        volumes : List of volume names to collect. Optional, default None.
        '''
        result_file = 'coldfront/plugins/fasrc/data/allthethings_output.json'
        if volumes:
            volumes = '|'.join(volumes)
        else:
            volumes = '|'.join([r.name.split('/')[0] for r in Resource.objects.all()])
        logger.debug('volumes: %s', volumes)

        quota = {'match': '[:HasQuota]-(e:Quota)',
            'where':f'WHERE (e.filesystem =~ \'.*({volumes}).*\')',
            'storage_type':'\'Quota\'',
            'usedgb': 'usedGB',
            'sizebytes': 'limitBytes',
            'usedbytes': 'usedBytes',
            'fs_path':'filesystem',
            'server':'filesystem',
            'replace': '/n/',
            'unique':'datetime(e.DotsLFSUpdateDate) as begin_date'}

        isilon = {'match': '[:Owns]-(e:IsilonPath)',
            'where':f'WHERE (e.Isilon =~ \'.*({volumes}).*\')',
            'storage_type':'\'Isilon\'',
            'fs_path':'Path',
            'server':'Isilon',
            'usedgb': 'UsedGB',
            'sizebytes': 'SizeBytes',
            'usedbytes': 'UsedBytes',
            'replace': '01.rc.fas.harvard.edu',
            'unique':'datetime(e.DotsUpdateDate) as begin_date'}

        # volume = {'match': '[:Owns]-(e:Volume)',
        #     'where': '',
        #     'storage_type':'\'Volume\'',
        #     'fs_path':'LogicalVolume',
        #     'server':'Hostname',
        #     'unique':'datetime(e.DotsLVSUpdateDate) as update_date, \
        #             datetime(e.DotsLVDisplayUpdateDate) as display_date'}

        queries = {'statements': []}

        for d in [quota, isilon]:
            statement = {'statement': f"MATCH p=(g:Group)-{d['match']} \
                    {d['where']} RETURN\
                    {d['unique']}, \
                    g.ADSamAccountName as lab,\
                    (e.SizeGB / 1024.0) as tb_allocation, \
                    e.{d['sizebytes']} as byte_allocation,\
                    e.{d['usedbytes']} as byte_usage,\
                    (e.{d['usedgb']} / 1024.0) as tb_usage,\
                    e.{d['fs_path']} as fs_path,\
                    {d['storage_type']} as storage_type, \
                    replace(e.{d['server']}, '{d['replace']}', '') as server"}
            queries['statements'].append(statement)
        resp_json = self.post_query(queries)
        # logger.debug(resp_json)
        resp_json_formatted = self.format_query_results(resp_json)
        resp_json_by_lab = {entry['lab']:[] for entry in resp_json_formatted}
        for entry in resp_json_formatted:
            if (entry['storage_type'] == 'Quota' and (
                entry['tb_usage'] == None) or (
                    entry['byte_usage'] == 0 and entry['tb_allocation'] == 1)
            ) or\
            (entry['storage_type'] == 'Isilon' and entry['tb_allocation'] in [0, None]):
                logger.debug('removed: %s', entry)
                continue
            resp_json_by_lab[entry['lab']].append(entry)
        # logger.debug(resp_json_by_lab)
        resp_json_by_lab_cleaned = {k:v for k, v in resp_json_by_lab.items() if v}
        with open(result_file, 'w') as file:
            file.write(json.dumps(resp_json_by_lab_cleaned, indent=2))
        return result_file


    def push_quota_data(self, result_file):
        '''Use JSON of collected ATT data to update group quota & usage values in Coldfront.
        '''
        errored_allocations = {}
        result_json = read_json(result_file)
        counts = {'proj_err': 0, 'res_err':0, 'all_err':0, 'complete':0}
        # produce list of present labs
        lablist = list(set(k for k in result_json))
        proj_models = Project.objects.filter(title__in=lablist)
        proj_titles = [p.title for p in proj_models]
        # log labs w/o projects, remove them from result_json
        missing_projs = log_missing('project', proj_titles,lablist)
        counts['proj_err'] = len(missing_projs)
        [result_json.pop(key) for key in missing_projs]

        # produce set of server values for which to locate matching resources
        resource_set = {a['server'] for l in result_json.values() for a in l}
        logger.debug("coldfront resource_set: %s", resource_set)
        # get resource model
        res_models = Resource.objects.filter(reduce(operator.or_,
                                    (Q(name__contains=x) for x in resource_set)))
        res_names = [str(r.name).split('/')[0] for r in res_models]
        missing_res = log_missing('resource', res_names, resource_set)
        counts['proj_err'] = len(missing_res)

        for k, v in result_json.items():
            result_json[k] = [a for a in v if a['server'] not in missing_res]

        for lab, allocations in result_json.items():
            logger.debug('PROJECT: %s ====================================', lab)
            # Find the correct allocation_allocationattributes to update by:
            # 1. finding the project with a name that matches lab.lab
            proj_query = proj_models.get(title=lab)
            for allocation in allocations:
                try:
                    # 2. find the resource that matches/approximates the server value
                    r_str = allocation['server'].replace("01.rc.fas.harvard.edu", "")\
                                .replace("/n/", "")
                    resource = res_models.get(name__contains=r_str)

                    # 3. find the allocation with a matching project and resource_type
                    a = Allocation.objects.filter(  project=proj_query,
                                                    resources__id=resource.id,
                                                    status__name='Active'   )
                    if a.count() == 1:
                        a = a.first()
                    elif a.count() < 1:
                        logger.warning("ERROR: No Allocation for project %s, resource %s",
                                                    proj_query.title, resource.name)
                        log_missing("allocation", [], [resource.name],
                                                group=proj_query.title,
                                                pattern="G,I,D")
                        counts['all_err'] += 1
                        continue
                    elif a.count() > 1:
                        logger.info("WARNING: multiple allocations returned. If LFS, will "
                            "choose the FASSE option; if not, will choose otherwise.")
                        just_str = "FASSE" if allocation['storage_type'] == "Isilon" else "Information for"
                        a = Allocation.objects.get( project=proj_query,
                                                    justification__contains=just_str,
                                                    resources__id=resource.id,
                                                    status__name='Active'   )

                    logger.info("allocation: %s", a.__dict__)

                    # 4. get the storage quota TB allocation_attribute that has allocation=a.
                    allocation_values = { 'Storage Quota (TB)':
                                [allocation['tb_allocation'],allocation['tb_usage']]  }
                    if allocation['byte_allocation'] != None:
                        allocation_values['Quota_In_Bytes'] = [ allocation['byte_allocation'],
                                                                allocation['byte_usage']]

                    for k, v in allocation_values.items():
                        allocation_attribute_type_obj = AllocationAttributeType.objects.get(
                            name=k)
                        try:
                            allocation_attribute_obj = AllocationAttribute.objects.get(
                                allocation_attribute_type=allocation_attribute_type_obj,
                                allocation=a,
                            )
                            allocation_attribute_obj.value = v[0]
                            allocation_attribute_obj.save()
                            allocation_attribute_exist = True
                        except AllocationAttribute.DoesNotExist:
                            allocation_attribute_exist = False

                        if (not allocation_attribute_exist):
                            allocation_attribute_obj,_ =AllocationAttribute.objects.get_or_create(
                                allocation_attribute_type=allocation_attribute_type_obj,
                                allocation=a,
                                value = v[0])
                            allocation_attribute_type_obj.save()

                        allocation_attribute_obj.allocationattributeusage.value = v[1]
                        allocation_attribute_obj.allocationattributeusage.save()

                    # 5. AllocationAttribute
                    allocation_attribute_type_payment = AllocationAttributeType.objects.get(name='RequiresPayment')
                    allocation_attribute_payment, _ = AllocationAttribute.objects.get_or_create(
                            allocation_attribute_type=allocation_attribute_type_payment,
                            allocation=a,
                            value=True)
                    allocation_attribute_payment.save()
                    counts['complete'] += 1
                except Exception as e:
                    allocation_name = f"{allocation['lab']}/{allocation['server']}"
                    errored_allocations[allocation_name] = e
        logger.info("error counts: %s", counts)
        logger.info('errored_allocations:\n%s', errored_allocations)


def create_new_projects(projects_list: list):
    '''
    Use ATT user, group, and relationship information to automatically create new
    Coldfront Projects from projects_list.
    '''
    att_conn = AllTheThingsConn()
    errortracker = ErrorTracker()
    # if project already exists, end here
    existing_projects = Project.objects.filter(title__in=projects_list)
    if existing_projects:
        logger.debug("existing projects: %s", [p.title for p in existing_projects])
    projects_to_add = [p for p in projects_list if p not in [p.title for p in existing_projects]]

    # if PI is inactive or otherwise unavailable, don't add project or users
    pi_data = att_conn.collect_pi_data(projects_to_add)
    logger.debug("projects lacking active PIs: %s",
        [entry['group_name'] for entry in pi_data if not entry['user_enabled']])
    active_pi_groups = [entry for entry in pi_data if entry['user_enabled']]

    # bulk-query user/group data
    user_group_search = "|".join(entry['group_name'] for entry in active_pi_groups)
    aduser_data = att_conn.collect_group_membership(f"({user_group_search})")
    aduser_data = [user for user in aduser_data if user['user_enabled']]

    # log and remove from list any AD users not in Coldfront
    aduser_names = [u['user_name'] for u in aduser_data]
    ifxusernames = [u.username for u in get_user_model.objects.filter(username__in=aduser_names)]
    missing = log_missing('user', ifxusernames, aduser_names)
    aduser_data = [u for u in aduser_data if u['user_name'] not in missing]

    for entry in active_pi_groups:
        # collect group membership entries
        ad_members = [user for user in aduser_data if user['group_name'] == entry['group_name']]

        # if no active group members, log and don't add Project
        if not ad_members:
            errortracker.no_members.append(entry['group_name'])
            continue

        ad_managers = [u['user_name'] for u in ad_members if u['relationship'] == 'ManagedBy']
        # if no active managers, log and don't add Project
        if not ad_managers:
            logger.warning('no active managers for project %s', entry['group_name'])
            print(f'WARNING: no active managers for project {entry["group_name"]}')
            errortracker.no_managers.append(entry['group_name'])
            continue


        # locate PI User entry
        try:
            project_pi = get_user_model().objects.get(username=entry['user_name'])
        except get_user_model().DoesNotExist:
            logger.warning('pi for project %s not in ifxusers; skipping', entry['group_name'])
            errortracker.no_managers.append(entry['group_name'])
            continue


        current_dt = datetime.datetime.now(tz=timezone.utc)

        # create description
        description = "Allocations for " + entry['group_name']

        # locate field_of_science
        field_of_science_name=entry['department']
        try:
            field_of_science_obj = FieldOfScience.objects.get(description=field_of_science_name)
        except FieldOfScience.DoesNotExist:
            print(field_of_science_name)
            field_of_science_obj = FieldOfScience(
                        is_selectable='True',
                        description=field_of_science_name,
                    )
            field_of_science_obj.save()


        ### CREATE PROJECT ###
        # is the project pi automatically added as a ProjectUser with PI status?
        new_project = Project.objects.create(
            created=current_dt,
            modified=current_dt,
            title=entry['group_name'],
            pi=project_pi,
            description=description.strip(),
            field_of_science=field_of_science_obj,
            status=ProjectStatusChoice.objects.get(name='New')
        )

        ### add projectusers ###
        # use set comprehension to avoid duplicate entries when MemberOf/ManagedBy relationships both exist
        ad_member_usernames = {u['user_name'] for u in ad_members}
        users_to_add = get_user_model().objects.filter(username__in=ad_member_usernames)
        new_projectusers = [
            ProjectUser(
                project=new_project,
                user=user,
                status=ProjectUserStatusChoice.objects.get(name='Active'),
                role=ProjectUserRoleChoice.objects.get(name='User'),
                )
            for user in users_to_add
            ]
        added_projectusers = ProjectUser.objects.bulk_create(new_projectusers)

        # add permissions to PI/manager-status ProjectUsers
        manager_usernames = ad_managers + [entry['user_name']]
        for username in manager_usernames:
            logger.debug('adding manager status to ProjectUser %s for Project %s',
                        username, entry['group_name'])
            manager = added_projectusers.get(user__username=username)
            manager.role = ProjectUserRoleChoice.objects.get(name='Manager')
            manager.save()

    errortracker.report()


def update_group_membership():
    '''
    Use ATT's user, group, and relationship information to keep the ProjectUser
    list up-to-date for existing Coldfront Projects.
    '''
    # change logger filehandler
    logger.removeHandler(filehandler)
    handler = logging.FileHandler(f'logs/att_membership_update-{today}.log', 'w')
    logger.addHandler(handler)
    errortracker = ErrorTracker()
    att_conn = AllTheThingsConn()

    for project in Project.objects.filter(status__name__in=["Active", "New"]):
        # pull membership data for the given project
        proj_name = project.title
        logger.debug('updating group membership for %s', proj_name)
        group_data = att_conn.collect_group_membership(proj_name)
        logger.debug('raw AD group data:\n%s', group_data)
        group_data = [user for user in group_data if user['user_enabled']]
        if not group_data:
            errortracker.no_members.append(proj_name)
            continue
        # project = Project.objects.get(title=proj_name)
        projectusernames = [pu.user.username for pu in project.projectuser_set.filter(
                    (~Q(status__name='Removed'))
                            )]
        logger.debug('projectusernames: %s', projectusernames)

        ### check through membership list ###
        ad_users = {user['user_name'] for user in group_data}
        # check for missing ProjectUsers
        missing_projectusers = [uname for uname in ad_users if uname not in projectusernames]
        logger.debug('AD users not in ProjectUsers:\n%s', missing_projectusers)

        if missing_projectusers:
            # find accompanying ifxusers in the system
            ifxusers = get_user_model().objects.filter(username__in=missing_projectusers)
            # log any users missing from the system
            ifxuser_names = [u.username for u in ifxusers]
            log_missing('user', ifxuser_names, missing_projectusers)
            for user in ifxusers:
                # in case user is being re-added to the project, first find/create a
                # project_user matching just project/user, then change role & status
                try:
                    project_user = ProjectUser.objects.get(project=project,
                                user=user)
                    project_user.role=ProjectUserRoleChoice.objects.get(name='User')
                    project_user.status = ProjectUserStatusChoice.objects.get(name='Active')
                    project_user.save()
                except ProjectUser.DoesNotExist:
                    ProjectUser.objects.create(project=project,
                                user=user,
                                role=ProjectUserRoleChoice.objects.get(name='User'),
                                status=ProjectUserStatusChoice.objects.get(name='Active')
                                )

        ### check through management list ###
        ad_managers = [u['user_name'] for u in group_data if u['relationship'] == 'ManagedBy']
        if not ad_managers:
            logger.warning('no active managers for project %s; skipping.', proj_name)
            print(f'WARNING: no active managers for project {proj_name}')
            errortracker.no_managers.append(proj_name)
            continue

        # get accompanying ProjectUser entries
        project_managers = ProjectUser.objects.filter(project=project, user__username__in=ad_managers)
        for manager in project_managers:
            # if ProjectUser's role__name is 'User', change it to 'Manager'
            if manager.role.name == 'User':
                manager.role = ProjectUserRoleChoice.objects.get(name='Manager')
                manager.save()

        ### change statuses of inactive ProjectUsers to 'Removed' ###
        projusers_to_remove = [uname for uname in projectusernames if uname not in ad_users]
        if projusers_to_remove:
            # log removed users
            logger.debug('users to remove: %s', projusers_to_remove)

            # if ProjectUser is still an AllocationUser, change to Pending - Remove
            for username in projusers_to_remove:
                project_user = ProjectUser.objects.get( project=project,
                                                        user__username=username)
                activeallocationusership = AllocationUser.objects.filter(
                                            allocation__project=project,
                                            user=project_user.user,
                                            status__name__in=['Active', 'Pending - Add']
                                            )
                if activeallocationusership:
                    message = f'cannot remove User {username} for Project {project.title} - active AllocationUser'
                    logger.warning(message)
                    print(message)
                    project_user.status = ProjectUserStatusChoice.objects.get(name='Pending - Remove')
                else:
                    project_user.status = ProjectUserStatusChoice.objects.get(name='Removed')
                    logger.debug('removed User %s from Project %s', username, project.title)
                project_user.save()
    errortracker.report()



def log_missing(modelname,
                item_list,
                search_list,
                group='',
                fpath_pref='./coldfront/plugins/fasrc/data/',
                pattern='I,D'):
    '''check if an item from search_list is present in item_list; produce a
    CSV of all items not present.

    Parameters
    ----------
    modelname : str
        Name of the Coldfront user model being sought
    item_list : list
    search_list : list
        list of items to confirm presence of in item_list
    '''
    fpath = f'{fpath_pref}missing_{modelname}s.csv'
    missing = [i for i in search_list if i not in list(item_list)]
    if missing:
        datestr = datetime.today().strftime('%Y%m%d')
        patterns = [pattern.replace('I', i).replace('D', datestr).replace('G', group) for i in missing]
        find_or_add_file_line(fpath, patterns)
    return missing


def find_or_add_file_line(filepath, patterns):
    '''Find or add lines matching a string contained in a list to a file.

    Parameters
    ----------
    filepath : string
        path and name of file to check.
    patterns : list
        list of lines to find or append to file.
    '''
    with open(filepath, 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        for pattern in patterns:
            if not any(pattern == line.rstrip('\r\n') for line in lines):
                file.write(pattern + '\n')


def generate_headers(token):
    '''Generate 'headers' attribute by using the 'token' attribute.
    '''
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(token),
    }
    return headers

def read_json(filepath):
    logger.debug('read_json for %s', filepath)
    with open(filepath, 'r') as myfile:
        data = json.loads(myfile.read())
    return data
