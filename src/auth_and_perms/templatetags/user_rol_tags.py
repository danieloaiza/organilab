from django import template
from django.db.models import Q

from auth_and_perms.models import ProfilePermission, Rol
from laboratory.models import OrganizationStructureRelations, Laboratory

register = template.Library()


@register.simple_tag(takes_context=True)
def has_perm_in_org(context, org_pk, permission):
    if context['request'].user.is_superuser:
        return True
    app_label, codename = permission.split(".")
    profile_in = ProfilePermission.objects.filter(profile=context['request'].user.profile,
                                                  content_type__app_label='laboratory',
                                                  content_type__model="organizationstructure",
                                                  object_id=org_pk)
    if not profile_in.exists():
        labs = set(Laboratory.objects.filter(
            Q(organization=org_pk) | Q(pk__in=
                                       OrganizationStructureRelations.objects.filter(
                                           organization=org_pk,
                                           content_type__app_label='laboratory',
                                           content_type__model="laboratory",
                                       ).values_list('object_id', flat=True)
                                       )
        ).values_list('pk', flat=True))
        profile_in = ProfilePermission.objects.filter(profile=context['request'].user.profile,
                                                      content_type__app_label='laboratory',
                                                      content_type__model="laboratory",
                                                      object_id__in=labs)

    rols = profile_in.values_list('rol', flat=True)
    rolsquery = Rol.objects.filter(
        pk__in=rols,
        permissions__content_type__app_label=app_label,
        permissions__codename=codename
    )

    return rolsquery.exists()


@register.simple_tag(takes_context=True)
def organization_any_permission_required(context, *args, **kwargs):
    perms = list(args)
    user = context['request'].user
    org = perms.pop(0)
    for perm in perms:
        has_perm = has_perm_in_org(context, org, perm)
        if has_perm:
            return True

    return False
