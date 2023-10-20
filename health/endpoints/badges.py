from health import USER_ID, SKILL_ID

BASE_URL = "https://staging.zuri.team/api/badges"
NAME = "BADGES"

ENDPOINTS_CONFIG = [

    #CREATE BADGE
    {
        "url": "/badges",
        "method": "POST",
        "path_params": None,
        "body_params": {
                "min_score": 0,
                "max_score": 35,
                "name": "beginner",
                "skill_id": 1
        },
        "auth_required": True
    },

    #ASSIGN BADGE
    {
        "url": "/api/user/badges",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "user_id": f"{USER_ID}",
            "assessment_id": 1
        },
        "auth_required": True
    },

    #RETRIEVE USER BADGE
    {
        "url": "/user/badges/{user_id}/skill/{skill_id}",
        "method": "GET",
        "path_params": {
            "user_id": f"{USER_ID}",
            "skill_id": f"{SKILL_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    #GET USER BADGE VIA ID
    {
        "url": "/api/badges/{user_id}",
        "method": "GET",
        "path_params": {
            "user_id": f"{USER_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    #GET ALL BADGES
    {
        "url": "/api/user/{user_id}/badges",
        "method": "GET",
        "path_params": {
            "user_id": f"{USER_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    {
        "url": "/api/badges/health",
        "method": "GET",
    }

]