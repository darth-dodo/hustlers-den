from hustlers.models import Group
from hustlers.constants import REGULAR_HUSTLER_GROUP


def assign_hustler_permission_group(hustler_object, permission_groups=[REGULAR_HUSTLER_GROUP]):
    """
    Assigning the django user attached to a hustler object to a Django Permission Group
    
    :param hustler_object: Hustler object
    :param permission_groups: List of groups to be assigned to the Hustler's django user
    :return: bool
    """
    django_user_obj = hustler_object.django_user

    for current_permission_group in permission_groups:
        try:
            required_hustler_group = Group.objects.get(name=current_permission_group)
            required_hustler_group.user_set.add(django_user_obj)
        except Group.DoesNotExist:
            # TODO implement logging later
            print("{0} group does not exist!".format(current_permission_group))
            pass


def assign_hustler_admin_panel_access(hustler_object, **panel_access):
    """
    Assign Hustler `is_staff` or/and `is_superuser` access
    :param hustler_object: Hustler object
    
    # kwargs using constants
    :param is_staff: value to be assigned to django user model
    :param is_superuser: value to be assigned to django user model 
    :return: 
    """
    django_user_object = hustler_object.django_user
    staff_access = panel_access.get("is_staff", False)
    superuser_access = panel_access.get("is_superuser", False)

    django_user_object.is_staff = staff_access
    django_user_object.is_superuser = superuser_access

    # implicitly assign staff access if superuser
    if superuser_access:
        django_user_object.is_staff = True

    django_user_object.save()
