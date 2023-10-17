BASE_URL = "https://assessment.cofucan.tech/api/assessments"
NAME = 'TAKE ASSESSMENTS'
SKILL_ID = 126
ASSESSMENT_ID = 175
USER_LOGIN = {
    "email":"abdulrasheedabdulsalam706@gmail.com",
    "password":"@Testing123"
    }


ENDPOINTS_CONFIG = [
     { 
         "url": "",
         "description":"Retrieve all user assessments ",
         "method": "GET",
         "headers":{"token":"string"},
         "auth_required": True

     },

     {
         "url": "/start-assessment",
         "method": "POST",
         "body_params": {"assessment_id": f"{ASSESSMENT_ID}"},
         "headers":{"token":"string"},
         "auth_required": True
      },

      {
         "url": "/session/{assessment_id}",
         "method": "GET",
         "path_params": {"assessment_id":f"{ASSESSMENT_ID}"},
         "headers":{"token":"string"},
         "auth_required": True
      },

      {
         "url": "/{assessment_id}/result",
         "description":"Retrieve assessment results for a user",
         "method": "GET",
         "path_params": {"assessment_id":f"{ASSESSMENT_ID}"},
         "headers":{"token":"string"},
         "auth_required": True
      },
      {
         "url": "/submit",
         "description":"Submit an assessment for a user",
         "method": "POST",
         "body_params":{
               "assessment_id": 175,
               "is_submitted": "false",
               "time_spent": 0,
               "response": {
                  "question_id": 275,
                  "user_answer_id": 363,
                  "answer_text": "a"
            }
         },
         "headers":{"token":"string"},
         "auth_required": True
      },
      {
         "url": "/get-user-assessments",
         "description":"Get User completed Assessments",
         "method": "GET",
         "headers":{"token":"string"},
         "auth_required": True
      },
     {
         "url": "/{skill_id}",
         "description":"Get Assessments tied to a skill_id",
         "method": "GET",
         "path_params": {"skill_id": f"{SKILL_ID}"},
         "headers":{"token":"string"},
         "auth_required": True
      },
 ]