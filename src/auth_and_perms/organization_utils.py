from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from laboratory.models import OrganizationStructureRelations


def user_is_allowed_on_organization(user, organization):
    if organization is None:
        raise ObjectDoesNotExist('Organization not found')
    if not organization.users.filter(pk=user.pk).exists():
        raise PermissionDenied(_("User %(user)s not allowed on organization %(organization)r ")%{
            'user': user, 'organization': organization})

def organization_can_change_laboratory(laboratory, organization):
    if laboratory.organization == organization:
        return True
    if OrganizationStructureRelations.objects.using(settings.READONLY_DATABASE).filter(
        content_type__app_label=laboratory._meta.app_label,
        content_type__model=laboratory._meta.model_name,
        object_id=laboratory.pk,
        organization=organization
    ).exists():
        return True
    return False