from health.helpers import update


BASE_URL  = "https://piranha-assessment-jco5.onrender.com"
NAME = "Assessments"

ASSESSMENT_ID = 165
DRAFT_ID = 177
SKILL_ID = 20
QUESTION_ID = 15

ASSESSMENT = {
    "skill_id": SKILL_ID,
    "questions_and_answers": [
        {
            "question_no": 1,
            "question_text": "Is this endpoint working?",
            "question_type": "multiple_choice",
            "options": ["a", "b", "c", "d"],
            "correct_option": 2
        }
    ],
    "assessment_name": "System Health Check Test",
    "duration_in_minutes": 25
}

ASSESSMENT_PUT = {
    "skill_id": SKILL_ID,
    "questions": [
        {
            "question_no": 1,
            "question_text": "Is this endpoint working?",
            "question_type": "multiple_choice",
            "answer": {
                "options": ["a", "b", "c"],
                "correct_option": "c"
            }
        }
    ],
    "title": "System Health Check Test",
    "duration_minutes": 30
}

DRAFT = {
    "skill_id": SKILL_ID,
    "questions_and_answers": [
        {
            "question_no": 1,
            "question_text": "Is this endpoint working?",
            "question_type": "multiple_choice",
            "options": ["a", "b", "c", "d"],
            "correct_option": 2
        }
    ],
    "assessment_name": "System Health Check Test Draft",
    "duration_in_minutes": 25
}

DRAFT_PUT = {
    "skill_id": SKILL_ID,
    "questions": [
        {
            "question_no": 1,
            "question_text": "Is this endpoint working?",
            "question_type": "multiple_choice",
            "answer": {
                "options": ["a", "b", "c", "d"],
                "correct_option": "c"
            }
        }
    ],
    "title": "System Health Check Test Draft",
    "duration_minutes": 30
}

QUESTION = {
    "question_no": 1,
    "question_text": "Is this endpoint working?",
    "question_type": "multiple_choice",
    "answer": {
        "options": ["a", "b", "c", "d"],
        "correct_option": "d"
    },
    "assessment_id": ASSESSMENT_ID,
}


async def extract_assessment_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    assessment_id = response.get("data").get("assessment_id")
    return 'assessment', assessment_id


ENDPOINTS_CONFIG = [
    {
        "url": "/api/admin/{assessment_id}/responses/",
        "method": "GET",
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
        "auth_required": True
    },
    {
        "url": "/api/admin/assessment-dashboard/",
        "method": "GET",
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/",
        "method": "GET",
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/",
        "method": "POST",
        "body_params": ASSESSMENT,
        "auth_required": False,
        "extractor": extract_assessment_id
    },
    {
        "url": "/api/admin/assessments/{assessment_id}/",
        "method": "GET",
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/{assessment_id}/",
        "method": "PUT",
        "body_params": update(
            ASSESSMENT_PUT,
            {"title": "System Health Check Test 2"}
        ),
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
    },
    {
        "url": "/api/admin/assessments/{}/",
        "method": "DELETE",
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/{assessment_id}/grading/",
        "method": "GET",
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/{assessment_id}/preview/",
        "method": "GET",
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
        "auth_required": True
    },
    {
        "url": "/api/admin/assessments/{assessment_id}/scoring/",
        "method": "GET",
        "path_params": {
            "assessment_id": ASSESSMENT_ID
        },
        "auth_required": True,
    },
    {
        "url": "/api/admin/drafts/",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/admin/drafts/",
        "method": "POST",
        "body_params": DRAFT,
        "auth_required": True,
        "extractor": extract_assessment_id
    },
    {
        "url": "/api/admin/drafts/{assessment_id}/",
        "method": "GET",
        "path_params": {
            "assessment_id": DRAFT_ID
        },
        "auth_required": True,
    },
    {
        "url": "/api/admin/drafts/{assessment_id}/",
        "method": "PUT",
        "path_params": {
            "assessment_id": DRAFT_ID
        },
        "body_params": update(
            DRAFT_PUT,
            {"title": "System Health Check Test Draft 2"}
        ),
    },
    {
        "url": "/api/admin/drafts/{}/",
        "method": "DELETE",
        "auth_required": True,
    },
    # {
    #     "url": "/api/admin/questions/{question_id}/",
    #     "method": "GET",
    #     "path_params": {
    #         "question_id": QUESTION_ID
    #     },
    #     "auth_required": True,
    # },
    # {
    #     "url": "/api/admin/questions/{question_id}/",
    #     "method": "PUT",
    #     "path_params": {
    #         "question_id": QUESTION_ID
    #     },
    #     "body_params": update(
    #         QUESTION,
    #         {"question_text": "Is this endpoint working? 2"}
    #     ),
    #     "auth_required": True,
    # },
    # {
    #     "url": "/api/admin/questions/{question_id}/",
    #     "method": "DELETE",
    #     "path_params": {
    #         "question_id": QUESTION_ID
    #     },
    # },
]
