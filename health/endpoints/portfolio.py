from health.helpers import update


BASE_URL = "https://hng6-r5y3.onrender.com"
NAME = "PORTFOLIO"
USER_ID = "79a7099e-34e4-4e49-8856-15ab6ed1380c"
AWARD_ID = 50
CERT_ID = 48
SECTION_ID = 57
CONTACT_ID = 6
CUSTOM_ID = 10
DEGREE_ID = 3
WORK_ID = 5
SKILL_ID = 2183
REFERENCE_ID  = 23
PROJECT_ID = 22
EDUCATION_ID = 54


AWARD_DRAFT = {
    "title": "Test Award",
    "year": "2023",
    "presented_by": "Obiwan Kenobi",
    "url": "https://test.com",
    "description": "Award for Testing"
}

CERTIFICATE_DRAFT = {

    "title": "Bsc Testing Technology",
    "year": "2023",
    "organization": "Test Tech",
    "url": "https://example.com",
    "description": "Completion of 2 year Apprentiship in Test Tech",
    "sectionId": 1
}

CONTACT_DRAFT = {

  "user_id": "79a7099e-34e4-4e49-8856-15ab6ed1380c",
  "social_media_id": 1,
  "url": "https://test.twitter.com"

}

SECTION_DRAFT =  {
            "name": "Test Section",
            "position": 3,
            "meta": "test",
            "description": "test",
        }

CUSTOM_DRAFT =  [
            {
                "fieldType": "Test",
                "customSectionId": 0,
                "customUserSectionId": 0,
                "fieldName": "Test",
                "value": "Test",
            }
        ]

CUSTOM_FIELD_DRAFT = {"sectionId": SECTION_ID, "userId": USER_ID}

INTEREST = {
            "interests": ["Sports", "Music"],
            "user_id": USER_ID,
            "section_id": 323,
        }

USER = {
            "name": "Health Check",
            "city": "Lagos",
            "country": "Nigeria",
            "trackId": "3",
        }

EDUCATION = {
            "section_id": 1,
            "degree_id": DEGREE_ID,
            "fieldOfStudy": "Engineering",
            "school": "University of Lagos",
            "description": "Bsc in Engineering",
            "from": "2020",
            "to": "2025",
        }

PROJECT = {
            "title": "Health Check Project",
            "year": 2023,
            "url": "https://example.com",
            "tags": ["Tag1", "Tag2"],
            "description": "Health Check",
            "userId": "79a7099e-34e4-4e49-8856-15ab6ed1380c",
            "sectionId": 25,
        }

REFERENCE = {
            "referer": "Health Check Test",
            "company": "Zuri",
            "position": "Backend Developer",
            "email": "health@gmail.com",
            "phoneNumber": "08100056789",
            "sectionId": 25,
}
WORKEXPERIENCE_DRAFT = {
            "company": "Andela",
            "role": "Consultant",
            "startMonth": "January",
            "startYear": "2018",
            "endMonth": "February",
            "endYear": "2023",
            "description": "Worked as a consultant for Andela",
            "isEmployee": True,
            "userId": "79a7099e-34e4-4e49-8856-15ab6ed1380c",
            "sectionId": 1,
}

USER_SETTINGS =  {
            "email": "",
            "currentPassword": "string",
            "newPassword": "string",
            "confirmNewPassword": "string",
            "emailAddress": "string@string.com",
        }

SKILL = {
            "skills": ["Test skill"],
            "sectionId": 1,
            "userId": "79a7099e-34e4-4e49-8856-15ab6ed1380c",
}

async def extract_award_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    award_id = response.get("createdAward").get("id")

    return 'award', award_id

async def extract_cert_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    cert_id = response.get("data").get("id")

    return 'certificate', cert_id

async def extract_contact_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    cert_id = response.get("data").get("id")

    return 'certificate', cert_id

async def extract_section_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    cert_id = response.get("data").get("id")

    return 'section', cert_id

async def extract_degree_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    deg_id = response.get("id")

    return 'degree', deg_id

async def extract_education_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response

    """
    edu_id = response.get("educationDetail").get("id")

    return 'education_detail', edu_id

async def extract_interest_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint
    :return: data from the response
    """
    interest_id = response.get("data").get("user_id")

    return 'interest', interest_id

async def extract_project_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """

    project_id = response.get("id")

    return 'project', project_id

async def extract_refrence_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    ref_id = response.get("data").get("id")

    return 'reference_detail', ref_id

async def extract_skill_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    skill_id = response.get("data")[-1].get("skillId")

    return 'skills_detail', skill_id

async def extract_workexp_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    id = response.get("data").get("id")

    return 'work_experience_detail', id


ENDPOINTS_CONFIG = [
    # AWARD
    {
        "url": "/api/award/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": AWARD_DRAFT,
        "auth_required": True,
        "extractor": extract_award_id
    },


    {
        "url": "/api/award/{award_id}",
        "method": "GET",
        "path_params": {"award_id": AWARD_ID},
        "auth_required": True,
    },

    {
        "url": "/api/award/{award_id}",
        "method": "PUT",
        "path_params": {"award_id": f"{AWARD_ID}"},
        "body_params":update(
            AWARD_DRAFT,
            {"description": "Award - System Health Check Test "}),
        "auth_required": True,
    },

    {
        "url": "/api/awards",
        "method": "GET",
        "auth_required": True,
    },


    {
        "url": "/api/award/{}",
        "method": "DELETE",
        "auth_required": True,
    },


    #CERTIFICATES
    {
        "url": "/api/add-certificate/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": CERTIFICATE_DRAFT,
        "auth_required": True,
        "extractor": extract_cert_id
    },

    {
        "url": "/api/certificates",
        "method": "GET",
        "auth_required": True,
    },

    {
        "url": "/api/certificates/{cert_id}",
        "method": "GET",
        "path_params": {"cert_id": f"{CERT_ID}"},
        "auth_required": True,
    },

    {
        "url": "/api/update-certification/{user_id}/{id}/{section_id}",
        "method": "PUT",
        "path_params": {
            "user_id": f"{USER_ID}",
            "id": f"{CERT_ID}",
            "section_id": f"{SECTION_ID}",
        },
        "body_params": update(CERTIFICATE_DRAFT,{"description": "Stewardship Award - System Health Check Test "}),
        "auth_required": True,
    },

    {
        "url": "/api/certificates/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    # # CONTACTS
    {
        "url": "/api/contacts/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },

    {
        "url": "/api/socials",
        "method": "GET",
        "auth_required": True,
    },

    # {
    #     "url": "/api/socials",
    #     "method": "POST",
    #     "body_params": {
    #         "name": "string",
    #     },
    #     "auth_required": True,
    # },

    {
        "url": "/api/contacts",
        "method": "POST",
        "body_params": CONTACT_DRAFT,
        "extractor": extract_contact_id,
        "auth_required": True,
    },

    {
        "url": "/api/contacts/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    {
        "url": "/api/contact/{contact_id}",
        "method": "PATCH",
        "path_params": {"contact_id": f"{CONTACT_ID}"},
        "body_params": update(CONTACT_DRAFT,{"url": "https://test.facebook.com"}),
        "auth_required": True,
    },
    # SECTION
    {
        "url": "/api/section",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/section/{id}",
        "method": "GET",
        "path_params": {"id": f"{SECTION_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/section/{id}",
        "method": "PUT",
        "path_params": {"id": f"{SECTION_ID}"},
        "body_params":update(SECTION_DRAFT, {"name": "Health Check Session"}),
    },

    {
        "url": "/api/section",
        "method": "POST",
        "body_params": SECTION_DRAFT,
        "extractor": extract_section_id,
        "auth_required": True,
    },
    {
        "url": "/api/section/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    # CUSTOM
    {
        "url": "/api/custom",
        "method": "POST",
        "body_params": CUSTOM_FIELD_DRAFT,
        "auth_required": True,
    },
    {
        "url": "/api/custom",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/custom/{id}",
        "method": "GET",
        "path_params": {"id": f"{CUSTOM_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/custom/field/{id}",
        "method": "GET",
        "path_params": {"id": f"{CUSTOM_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/custom/field",
        "method": "POST",
        "body_params":CUSTOM_DRAFT,
        "auth_required": True,
        "extractor": extract_section_id,
    },
    {
        "url": "/api/custom/field/{id}",
        "method": "PUT",
        "path_parmas": {"id": f"{CUSTOM_ID}"},
        "body_params": [
            {
                "fieldType": "string",
                "customSectionId": 0,
                "customUserSectionId": 0,
                "fieldName": "string",
                "value": "string",
            }
        ],
        "auth_required": True,
    },
    {
        "url": "/api/custom-section/{}",
        "method": "DELETE",
        "body_params": None,
        "auth_required": True,
    },
    # DEGREE
    {
        "url": "/api/degree",
        "method": "POST",
        "body_params": {
            "type": "Masters",
        },
        "auth_required": True,
        "extractor": extract_degree_id,
    },
    {
        "url": "/api/degree",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/degree/{id}",
        "method": "GET",
        "path_params": {"id": f"{DEGREE_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/degree/{id}",
        "method": "PUT",
        "path_params": {"id": f"{DEGREE_ID}"},
        "body_params": update({"type": "Bsc"}, {"type": "Bsc"}),
        "auth_required": True,
    },

    {
        "url": "/api/degree/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    # EDUCATION
    {
        "url": "/api/education/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": EDUCATION,
        "auth_required": True,
        "extractor": extract_education_id,
    },
    {
        "url": "/api/educationDetail/{id}",
        "method": "GET",
        "path_params": {"id": f"{EDUCATION_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/education/{id}",
        "method": "GET",
        "path_params": {"id": f"{USER_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/updateEducationDetail/{id}",
        "method": "PATCH",
        "path_params": {"id": f"{EDUCATION_ID}"},
        "body_params": update(EDUCATION, {"fieldOfStudy": "Medicine"}),
        "auth_required": True,
    },
    {
        "url": "/api/education/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    # GREETING
    {
        "url": "/",
        "method": "GET",
        "auth_required": True,
    },
    # # UPLOAD
    # # {
    # #     "url": "/api/upload",
    # #     "method": "POST",
    # #     "path_params": None,
    # #     "body_params": {
    # #                       "file": "string"
    # #     }
    # #     "auth_required": True
    # # },
    # INTEREST
    {
        "url": "/api/interests/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": False,
    },
    {
        "url": "/api/interests",
        "method": "POST",
        "body_params": INTEREST,
        "auth_required": False,
        "Extractor": extract_interest_id
    },
    {
        "url": "/api/interests/{user_id}",
        "method": "PUT",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {"interests": ["Teaching", "Technology"]},
        "auth_required": False,
    },

    {
        "url": "/api/interests/{}",
        "method": "DELETE",
        "body_params": None,
        "auth_required": False,
    },
    # LANGUAGE
    {
        "url": "/api/language",
        "method": "POST",
        "body_params": {
            "user_id": USER_ID,
            "languages": ["Python", "Javascript"],
        },
        "auth_required": True,
    },
    {
        "url": "/api/language/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },
    # USER PORTFOLIO DETAILS
    {
        "url": "/api/users",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/users/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },

    {
        "url": "/api/profile/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": USER,
        "auth_required": True,
    },

    {
        "url": "/api/profile/cover/upload",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "file": "string"
                        },
        "auth_required": True
    },
    {
        "url": "/api/profile/image/upload",
        "method": "POST",
        "body_params": {
                          "file": "string"
                        },
        "auth_required": True
    },
    {
        "url": "/api/getPortfolioDetails/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/portfolioDetails",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/profile-details/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{USER_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/update-portfolio-details/{user_id}",
        "method": "PUT",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {
            "name": "Joe King",
            "trackId": 2,
            "city": "Lome",
            "country": "Togo",
        },
        "auth_required": True,
    },

    # PROJECT
    {
        "url": "/api/projects",
        "method": "GET",
        "auth_required": True,
    },

    {
        "url": "/api/projects/{id}",
        "method": "GET",
        "path_params": {"id": f"{PROJECT_ID}"},
        "auth_required": True,
    },

    {
        "url": "/api/projects",
        "method": "POST",
        "body_params": PROJECT,
        "auth_required": True,
        "extractor": extract_project_id
    },

    {
        "url": "/api/update-project/{project_id}",
        "method": "PUT",
        "path_params": {"project_id": f"{PROJECT_ID}"},
        "body_params": update(PROJECT, {"title": "Health Check Project 2"}),
        "auth_required": True
    },
    {
        "url": "/api/projects/{}",
        "method": "DELETE",
        "auth_required": True,
    },
    # REFERENCE
    {
        "url": "/api/references/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": REFERENCE,
        "auth_required": True,
        "extractor": extract_refrence_id
    },
    {
        "url": "/api/references/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/references/{}",
        "method": "DELETE",
        "auth_required": True,
    },
    # SETTINGS
    {
        "url": "/api/get-notification-settings/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
    },
    {
        "url": "/api/update-user-account-settings",
        "method": "PATCH",
        "body_params":USER_SETTINGS,
        "auth_required": True,
    },
    {
        "url": "/api/set-notification-settings/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {
            "communityUpdate": True,
            "emailSummary": True,
            "newMessages": True,
            "followUpdate": True,
            "specialOffers": True,
        },
        "auth_required": True,
    },
    {
        "url": "/api/update-notification-settings/{user_id}",
        "method": "PATCH",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {
            "communityUpdate": True,
            "emailSummary": True,
            "newMessages": True,
            "followUpdate": True,
            "specialOffers": True,
            "userId": "string",
        },
        "auth_required": True,
    },
    # {
    #     "url": "/api/delete-user-account/{user_id}",
    #     "method": "DELETE",
    #     "path_params": {"user_id": f"{USER_ID}"},
    #     "auth_required": True,
    # },
    #TRACKS
    {
        "url": "/api/tracks",
        "method": "GET",
        "auth_required": True,
    },
    # SKILLS
    {
        "url": "/api/create-skills",
        "method": "POST",
        "body_params": SKILL,
        "auth_required": True,
    },
    {
        "url": "/api/update-skills/{id}",
        "method": "PUT",
        "path_params": {"id": f"{SKILL_ID}"},
        "body_params":update(SKILL, {"skills": ["Test skill", "Test skill 2"]}),
        "auth_required": True,
    },
    {
        "url": "/api/skills-details/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "auth_required": True,
        "extractor": extract_skill_id
    },
    {
        "url": "/api/delete-skills/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    # WORK EXPERIENCE
    {
        "url": "/api/work-experience",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/create-work-experience/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": WORKEXPERIENCE_DRAFT,
        "auth_required": True,
        "extractor": extract_workexp_id
    },
    {
        "url": "/api/work-experience/{}",
        "method": "DELETE",
        "auth_required": True,
    },

    {
        "url": "/api/update-work-experience/{work_id}",
        "method": "PUT",
        "path_params": {"work_id": f"{WORK_ID}"},
        "body_params": update(WORKEXPERIENCE_DRAFT, {"company": "Zuri"}),
        "auth_required": True,
    },
]
