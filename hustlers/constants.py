REGULAR_HUSTLER_GROUP = 'Regular Hustler'
SUPERUSER_HUSTLER_GROUP = 'SuperUser Hustler'
ALL_PERMISSION_GROUPS = [REGULAR_HUSTLER_GROUP, SUPERUSER_HUSTLER_GROUP]

REGULAR_HUSTLER_ADMIN_PANEL_ACCESS = {"is_staff": True, "is_superuser": False}
SUPERUSER_HUSTLER_ADMIN_PANEL_ACCESS = {"is_staff": True, "is_superuser": True}

REGULAR_HUSTLER_PERMISSIONS = {
                                "admin_panel": REGULAR_HUSTLER_ADMIN_PANEL_ACCESS,
                                "groups": [REGULAR_HUSTLER_GROUP]
                               }

SUPERUSER_HUSTLER_PERMISSIONS = {
                                  "admin_panel": SUPERUSER_HUSTLER_ADMIN_PANEL_ACCESS,
                                  "groups": [SUPERUSER_HUSTLER_GROUP, REGULAR_HUSTLER_GROUP]
                                }
