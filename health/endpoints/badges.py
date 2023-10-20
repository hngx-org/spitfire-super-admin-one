from health import USER_ID, SKILL_ID

BASE_URL = "https://staging.zuri.team/api/badges"
NAME = "BADGES"
BADGE_ID = 118
SKILL_ID = 7

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
        "url": "/user/badges",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "user_id": f"{USER_ID}",
            "assessment_id": 1
        },
        "auth_required": True
    },

    # #RETRIEVE USER BADGE
    # {
    #     "url": "/user/badges/skill/{id}",
    #     "method": "GET",
    #     "path_params": {
    #         "skill_id": f"{SKILL_ID}"
    #     },
    #     "auth_required": True
    # },

    #GET USER BADGE VIA ID
    {
        "url": "/badges/{badge_id}",
        "method": "GET",
        "path_params": {
            "badge_id": f"{BADGE_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    #GET ALL USER BADGES
    {
        "url": "/user/badges",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/api/badges/health",
        "method": "GET",
    }

]