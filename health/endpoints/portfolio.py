BASE_URL = "https://hng6-r5y3.onrender.com"
NAME = "PORTFOLIO"
USER_ID = ""
AWARD_ID = ""
CERT_ID = ""
SECTION_ID = ""
ID = ""
PROJECT_ID = ""
WORK_ID = ""


ENDPOINTS_CONFIG = [
    # AWARD
    {
        "url": "/api/award/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {
                          "title": "string",
                          "year": "string",
                          "presented_by": "string",
                          "url": "string",
                          "description": "string"
                       },
        "auth_required": True 
    },

    {
        "url": "/api/award/{award_id}",
        "method": "PUT",
        "path_params": {"award_id": f"{AWARD_ID}"},
        "body_params": {
                          "title": "string",
                          "year": "string",
                          "presented_by": "string",
                          "url": "string",
                          "description": "string"
                        },
        "auth_required": True
    },
    
    {
        "url": "/api/award/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_parmas": None,
        "auth_required": True
    },
    
    {
        "url": "/api/award/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_parmas": None,
        "auth_required": True
    },
    
    {
        "url": "/api/awards",
        "method": "GET",
        "path_params": None,
        "body_parmas": None,
        "auth_required": True
    },
    
    # CERTIFICATES
    {
        "url": "/api/add-certificate/{user_id}",
        "method": "POST",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": {
                          "title": "string",
                          "year": "string",
                          "organization": "string",
                          "url": "string",
                          "description": "string",
                          "sectionId": 0
                       },
        "auth_required": True 
    },
    
    {
        "url": "/api/certificates",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/certificates/{cert_id}",
        "method": "DELETE",
        "path_params": {"cert_id": f"{CERT_ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {   
        "url": "/api/certificates/{cert_id}",
        "method": "GET",
        "path_params": {"cert_id": f"{CERT_ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {
    
        "url": "/api/update-certification/{user_id}/{id}/{section_id}",
        "method": "PUT",
        "path_params": {"user_id": f"{USER_ID}", "id": f"{ID}", "section_id": f"{SECTION_ID}"},
        "body_params": {
                        "title": "string",
                        "year": "string",
                        "organization": "string",
                        "url": "string",
                        "description": "string"
                      },
        "auth_required": True
    },
    
    # CONTACTS    
    
    {
        "url": "/api/contacts/{user_id}",
        "method": "GET",
        "path_params": {"user_id": f"{USER_ID}"},
        "body_params": None,
        "auth_required": True    
    },
    
    {
        "url": "/api/contacts",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "user_id": "string",
                          "social_media_id": 0,
                          "url": "string"
                       },
        "auth_required": True
      
      
    },
    
    {
        "url": "/api/contacts/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/socials",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "name": "string",
                       },
        "auth_required": True
    },
    
    
    {
        "url": "/api/socials",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True      
    },
    
    {
        "url": "/api/contact/{id}",
        "method": "PATCH",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    # SECTION
    
    {
        "url": "/api/section",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/section/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/section",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "position": 0,
                          "name": "string",
                          "description": "string",
                          "meta": "string"
                       },
        "auth_required": True      
    },
    
    {
      
        "url": "/api/section/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/section/{id}",
        "method": "PUT",
        "path_params": {"id": f"{ID}"},
        "body_params": {
                          "name": "string",
                          "position": 0,
                          "meta": "string",
                          "description": "string"
                       },
    },
    
    # CUSTOM
    
    {
        "url": "/api/custom",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "sectionId": 0,
                          "userId": "string"
                       },
        "auth_required": True
    },
    
    {
        "url": "/api/custom",
        "method": "GET",
        "parh_params": None,
        "body_params": None,
        "auth_required": True        
    },
    
    {
        "url": "/api/custom/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True      
    },
    
    {
        "url": "/api/custom/field/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    },
    
    {
        "url": "/api/custom/field",
        "method": "POST",
        "path_parmas": None,
        "body_params": [
                        {
                          "fieldType": "string",
                          "customSectionId": 0,
                          "customUserSectionId": 0,
                          "fieldName": "string",
                          "value": "string"
                        }
                      ],
        "auth_required": True
    },
    
    {
        "url": "/api/custom/field/{id}",
        "method": "PUT",
        "path_parmas": {"id": f"{ID}"},
        "body_params": [
                          {
                            "fieldType": "string",
                            "customSectionId": 0,
                            "customUserSectionId": 0,
                            "fieldName": "string",
                            "value": "string"
                          }
                        ]
        "auth_required": True
    },  
    
    
    {
        "url": "/api/custom-section/{id}"
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True
    }
      
      
    # DEGREE
    
    {
        "url": "/api/degree",
        "method": "POST",
        "path_params": None,
        "body_params": {
                          "type": "string",
                       },
        "auth_required": True        
    },
    
    {
        "url": "/api/degree"
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True      
    },
    
    {
        "url": "/api/degree/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True     
    },
    
    {
        "url": "/api/degree/{id}"
        "method": "PUT",
        "path_params": {"id": f"{ID}"},
        "body_params": {
                          "type": "string",
                       },
        "auth_required": True
    },
    
    {     
        "url": "/api/degree/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True  
    },
    
    
    
    # EDUCATION
    
    {
        "url": "/api/education",
        "method": "POST",
        "path_params": None,
        "body_params": {
                            "section_id": 0,
                            "degree_id": 0,
                            "fieldOfStudy": "string",
                            "school": "string",
                            "description": "string",
                            "from": "string",
                            "to": "string"
                       },
        "auth_required": True        
    },
    
    {
        "url": "/api/educationDetail/{id}"
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True      
    },
    
    {
        "url": "/api/education/{id}",
        "method": "GET",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True     
    },
    
    {
        "url": "/api/updateEducationDetail/{id}"
        "method": "PATCH",
        "path_params": {"id": f"{ID}"},
        "body_params": {
                            "degree_id": 0,
                            "fieldOfStudy": "string",
                            "school": "string",
                            "description": "string",
                            "from": "string",
                            "to": "string"
                       },
        "auth_required": True
    },
    
    {
      
        "url": "/api/education/{id}",
        "method": "DELETE",
        "path_params": {"id": f"{ID}"},
        "body_params": None,
        "auth_required": True  
    },
    
    # GREETING
    
    {
        "url": "/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },
    
    # UPLOAD
    # {
    #     "url": "/api/upload",
    #     "method": "POST",
    #     "path_params": None,
    #     "body_params": {
    #                       "file": "string"
    #     }
    #     "auth_required": True      
    # },
    
    # INTEREST
    {
        "url": "/api/interests/{user_id}",
        "method": "GET",
        "path_params": "{"id": f"{USER_ID}"}",
        "body_params": None,
        "auth_required": False
    },
      
      {
          "url": "/api/interests",
          "method": "POST",
          "path_params": None,
          "body_params": {
                            "interests": [
                              "Sports",
                              "Music"
                            ],
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "section_id": 323
                         },
          "auth_required": False
      },
      
      {
          "url": "/api/interests/{user_id}",
          "method": "PUT",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": {
                            "interests": [
                              "Teaching",
                              "Technology"
                            ]
                         },
          "auth_required": False
      },
      
      
      
      {
          "url": "/api/interests/{id}",
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": False
      },
      
      
      # LANGUAGE
      {
          "url": "/api/language",
          "method": "POST",
          "path_params": None,
          "body_params": {
                            "user_id": "f8e1d17d-0d9e-4d21-89c5-7a564f8a1e90",
                            "languages": [
                                          "Python",
                                          "Javascript"
                                          ]
                          },
          "auth_required": True
      },
      
      {
          "url": "/api/language/{userId}",
          "method": "GET",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True
      },
      
      # USER PORTFOLIO DETAILS
      {
        
          "url": "/api/users",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True        
      },
      
      
      {
        
          "url": "/api/users/{user_id}",
          "method": "GET",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True        
      },
      
      {
        
          "url": "/api/profile/{user_id}",
          "method": "POST",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": {  
                            "name": "string",
                            "city": "string",
                            "country": "string",
                            "trackId": "string"            
                         }
          "auth_required": True
      },
      
      # {
      #     "url": "/api/profile/cover/upload",
      #     "method": "POST",
      #     "path_params": None,
      #     "body_params": {
      #                       "file": "string"
      #                     },
      #     "auth_required": True       
        
      # },
      
      # {
      #     "url": "/api/profile/image/upload",
      #     "method": "POST",
      #     "path_params": None,
      #     "body_params": {
      #                       "file": "string"
      #                     },
      #     "auth_required": True       
        
      # },
      
      {
          "url": "/api/getPortfolioDetails/{user_id}",
          "method": "GET",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True
        
      },
      
      {
          "url": "/api/portfolioDetails",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True
      },
            
      {
          "url": "/api/profile-details/{id}",
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True
      },
      
      {
          "url": "/api/update-portfolio-details/{user_id}",
          "method": "PUT",
          "path_params": {"id": f"{USER_ID}"},
          "body_params": {
                            "name": "Joe King",
                            "trackId": 2,
                            "city": "Lome",
                            "country": "Togo"
                          },
          "auth_required": True
      },
      
      # PROJECT 
      {
        
          "url": "/api/projects",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True
      },
      
      {
        
          "url": "/api/projects/{id}",
          "method": "GET",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True
      },
      
      {
          "url": "/api/projects"
          "method": "POST",
          "path_params": None,
          "body_params": {
                            "title": "My Project",
                            "year": 2023,
                            "url": "https://example.com",
                            "tags": ["Tag1", "Tag2"],
                            "description": "Project Description",
                            "userId": "user123",
                            "sectionId": 1
                         },
          "auth_required": True   
      },
      
      # {
      #     "url": "/api/update-project/{project_id}"
      #     "method": "PUT",
      #     "path_params": {"project_id": f"{PROJECT_ID}"},
      #     "body_params": {
      #                       "title": "string",
      #                       "year" : "int32",
      #                       "url": "string",
      #                       "tags" : "string" ,
      #                       "description" : "string",
      #                       "user_id" : "string",
      #                       "thumbnail": "integer",
      #                       "section_id" : "int32"
      #                       "images": "file",                            
      #                    },
      #     "auth_required": True
            
      # },
        
      {
          "url": "/api/projects/{id}",
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True
      },
      
      # REFERENCE
      
      {
          "url": "/api/references/{user_id}",
          "method": "POST",
          "path_params": None,
          "body_params": {
                            "name": "Sapphire",
                            "company": "Zuri",
                            "position": "Backend Developer",
                            "emailAddress": "sofiyyahabidoye@gmail.com",
                            "phoneNumber": "08101695397"
                         },
          "auth_required": True     
      },
      
      {
          "url": "/api/references",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True
      },
      
            
      {
        
          "url": "/api/references/{id}"
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True
      },
      
      # SETTINGS
      
      {
          "url": "/api/get-notification-settings/{user_id}",
          "method": "GET",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True     
      },
      
      {
        
          "url": "/api/update-user-account-settings"
          "method": "PATCH",
          "path_params": None,
          "body_params": {
                            "emial": "string",
                            "currentPassword": "string",
                            "newPassword": "string",
                            "confirmNewPassword": "string",
                            "emailAddress": "string@string.com"
                         },       
          "auth_required": True
      },
      {
        
          "url": "/api/set-notification-settings/{user_id}"
          "method": "POST",
          "path_params": {"id": f"{USER_ID}"},
          "body_params": {
                            "communityUpdate": True,
                            "emailSummary": True,
                            "newMessages": True,
                            "followUpdate": True,
                            "specialOffers": True
                         },       
          "auth_required": True
      },
      
      {
        
          "url": "/api/update-notification-settings/{user_id}"
          "method": "PATCH",
          "path_params": {"id": f"{USER_ID}"},
          "body_params": {
                            "communityUpdate": True,
                            "emailSummary": True,
                            "newMessages": True,
                            "followUpdate": True,
                            "specialOffers": True
                            "userId": "string"
                         },       
          "auth_required": True
      },
      
      {
          "url": "/api/delete-user-account/{user_id}",
          "method": "DELETE",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True     
      },
      
      
      
      # TRACKS
            
      {
          "url": "/api/tracks",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True     
      },
      
      
      # SKILLS
      
      {
          "url": "/api/skills-details/{user_id}",
          "method": "GET",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": None,
          "auth_required": True       
      },
      
      {
          "url": "/api/delete-skills/{id}",
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True       
      },
      
      {
        
          "url": "/api/create-skills"
          "method": "POST",
          "path_params": None,
          "body_params": {
                            "skills": [
                              "string"
                            ],
                            "sectionId": 0,
                            "userId": "string"
                         },       
          "auth_required": True
      },
      
      {
        
          "url": "/api/update-skills/{id}"
          "method": "PUT",
          "path_params":  {"id": f"{ID}"},
          "body_params": {
                            "skills": "string",
                            "sectionId": 0,
                            "userId": "string"
                         },     
          "auth_required": True
      },
      
      # WORK EXPERIENCE
      
      {
          "url": "/api/work-experience",
          "method": "GET",
          "path_params": None,
          "body_params": None,
          "auth_required": True       
      },
      
      {
          "url": "/api/work-experience/{id}",
          "method": "DELETE",
          "path_params": {"id": f"{ID}"},
          "body_params": None,
          "auth_required": True       
      },
      
      {
        
          "url": "/api/create-work-experience/{user_id}"
          "method": "POST",
          "path_params": {"user_id": f"{USER_ID}"},
          "body_params": {
                            "company": "string",
                            "role": "string",
                            "startMonth": "string",
                            "startYear": "string",
                            "endMonth": "string",
                            "endYear": "string",
                            "description": "string",
                            "isEmployee": True,
                            "userId": "string",
                            "sectionId": 0"
                         },       
          "auth_required": True
      },
      
      {
        
          "url": "/api/update-work-experience/{work_id}"
          "method": "PUT",
          "path_params":  {"work_id": f"{WORK_ID}"},
          "body_params": {
                            "company": "string",
                            "role": "string",
                            "startMonth": "string",
                            "startYeah": "string",
                            "endMonth": "string",
                            "endYear": "string",
                            "description": "string",
                            "userId": "string"
                            "isEmployee": True,
                            "sectionId": 0
                         },       
          "auth_required": True
      },
      
      
      

    
    
    
    
    
    
]