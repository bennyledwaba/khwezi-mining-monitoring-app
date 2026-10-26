def get_allowed_tabs(role: str):
    role = role.strip()
    role_map = {
        "Administrator": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Equipment Data",
            "Maintenance Data",
            "Generate Reports",
            "Manage Users Console",
        ],
        "Safety Officer": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Generate Reports",
        ],
        "Mining Engineer": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Equipment Data",
            "Maintenance Data",
            "Generate Reports",
        ],
    }
    return role_map.get(role, ["View Dashboard"])
