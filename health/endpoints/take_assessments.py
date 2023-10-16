BASE_URL = "http://104.248.143.148/api/assessments"
NAME = 'TAKE ASSESSMENTS'
SKILL_ID = 25
ASSESMENT_ID = 127
USER_LOGIN = {
    "email":"abdulrasheedabdulsalam706@gmail.com",
    "password":"@Testing123"
    }
ASSESSMENT_ID = ""
TOKEN = "token generated from auth after login"

ENDPOINTS_CONFIG = [
     { 
         "url": "",
         "description":"Retrieve all user assessments ",
         "method": "GET",
         "path_params": None,
         "body_params": None,
         "header_params":{"token":TOKEN},
         "auth_required": True
     },
     {
         "url": "/start-assessment",
         "description":"Start an assessment for a user",
         "method": "POST",
         "path_params": None,
         "body_params": {"assessment_id":ASSESSMENT_ID},
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
      {
         "url": "/session",
         "description":"Get Session Details",
         "method": "GET",
         "path_params": None,
         "body_params": None,
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
      {
         "url": "/{assessment_id}/result",
         "description":"Retrieve assessment results for a user",
         "method": "GET",
         "path_params": {"assessment_id":ASSESSMENT_ID},
         "body_params": None,
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
      {
         "url": "/submit",
         "description":"Submit an assessment for a user",
         "method": "POST",
         "path_params": None,
         "body_params": {
                 "assessment_id": ASSESSMENT_ID,
                 "is_submitted": False,
                 "response": {
                   "question_id": 0,
                   "user_answer_id": 0,
                   "answer_text": "string"
                 }
              },
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
      {
         "url": "/get-user-assessments",
         "description":"Get User completed Assessments",
         "method": "GET",
         "path_params": None,
         "body_params": None,
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
     {
         "url": "/{skill_id}",
         "description":"Get Assessments tied to a skill_id",
         "method": "GET",
         "path_params": {"skill_id":SKILL_ID},
         "body_params": None,
         "header_params":{"token":TOKEN},
         "auth_required": True
      },
 ]