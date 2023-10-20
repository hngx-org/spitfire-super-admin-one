from datetime import datetime, timedelta

BASE_URL = "https://team-mirage-super-amind2.onrender.com"
NAME = "SUPERADMIN 2"
CURRENT_DATE = datetime.now()
USER_ID = ""
ORDER_ID = ""
ID = ''
COMPLAINT_ID = ''
USER_PURCHASE =  {
    "user": USER_ID,
    "order": ORDER_ID,
    "created_at": CURRENT_DATE.strftime('%Y-%m-%d')
}
COMMENT = {
    "id": f"{ID}",
    "user_id": USER_ID,
    "comment": "A stupid comment",
    "complaint_id": COMPLAINT_ID,
    "user_details": {
        "id": "<uuid>",
        "first_name": "<string>",
        "last_name": "<string>",
        "email": "<email>",
        "profile_pic": "<string>"
    },
    "createdAt": "<dateTime>",
    "updatedAt": "<dateTime>"
}
COMPLAINT = {
    "user": "76f62a58-5404-486d-9afc-07bded328704",
    "product": "e0588024-d851-42d5-ab9f-1b664ef352d4",
    "complaint_text": "string",
    "status": "string",
    "user_details": {
        "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "profile_pic": "string"
    }
}
COMPLAINT_UPDATE = {
    "user": "<uuid>",
    "product": "<uuid>",
    "complaint_text": "<string>",
    "status": "<string>",
    "user_details": {
        "id": "<uuid>",
        "first_name": "<string>",
        "last_name": "<string>",
        "email": "<email>",
        "profile_pic": "<string>"
    },
    "createdAt": "<dateTime>",
    "updatedAt": "<dateTime>"
}

ENDPOINTS_CONFIG = [

    #GET ALL USER ACTIVITIES
    {
        "url": "/api/admin/analytics/activities/",
        "method": "GET",
        "auth_required": True
    },

    #GET LIST OF BEST SELLING PRODUCTS BASED ON TOTAL ORDERS
    {
        "url": "/api/admin/analytics/best_selling_products/",
        "method": "GET",
        "query_params": {
            "page": 1,
            "page_size": 10
        },
        "auth_required": True
    },

    #GENERATE ANALYTICS WITHIN A GIVEN DATE RANGE
    {
        "url": "/api/admin/analytics/data/",
        "method": "GET",
        "query_params": {
            "start_date": f"{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}",
            "end_date": f"{(CURRENT_DATE).strftime('%Y-%m-%d')}"
        },
        "auth_required": True
    },

    # GET ANALYTICS EXPORT REPORT LIST
    {
        "url": "/api/admin/analytics/export_report/",
        "method": "GET",
        "auth_required": True
    },

    # GET METRIC VIEW, TRANSACTION LIST
    {
        "url": "/api/admin/analytics/get_metrics/",
        "method": "GET",
        "auth_required": True
    },

    #POST GET USER_ID OF NEWLY CREATED PORTFOLIOS
    {
        "url": "/api/admin/analytics/portfolio-activity/",
        "method": "POST",
        "auth_required": True
    },

    # GET ANALYTICS PORTFOLIO SUMMARY LIST
    {
        "url": "/api/admin/analytics/portfolio_summary/",
        "method": "GET",
        "auth_required": True
    },
    
    # GET TOTAL SALES,USERS AND ORDERS WITHIN A GIVEN TIME FRAME
    {
        "url": "/api/admin/analytics/total-sales-orders-users/",
        "method": "GET",
        "query_params": {
            "start_date": f"{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}",
            "end_date": f"{(CURRENT_DATE).strftime('%Y-%m-%d')}",
            "last": 7
        },
        "auth_required": True
    },

    # POST TRACK A USER PRODUCT PURCHASE
    {
        "url": "/api/admin/analytics/user-purchase-activity/",
        "method": "POST",
        "body_params": USER_PURCHASE,
        "auth_required": True
    },

    # GET FEEDBACK COMMENT LIST
    {
        "url": "/api/admin/feedback/comments/",
        "method": "GET",
        "auth_required": True
    },

    # POST CREATE FEEDBACK COMMENT - FLAG FOR CORRECTION
    {
        "url": "/api/admin/feedback/comments/",
        "method": "POST",
        "body_params": COMMENT,
        "auth_required": True

    },
    {
        "url": '/api/superadmin/feedback/register_complaints/',
        "method": 'POST',
        "body_params": COMPLAINT,
        "auth_required": True,
    },

    # POST FEEDBACK COMPLAINTS COMMENT CREATE - FLAG FOR CORRECTION
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/comments/",
        "method": "POST",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": COMMENT,
    },

    # GET FEEDBACK COMPLAINT COMMENTS LIST
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/listcomment/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "auth_required": True
    },

    # GET Get Complaint from Reviews Team using complaint ID
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "auth_required": True
    },

    # PATCH Update the status of Complaint from pending to in progress or resolved
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/",
        "method": "PATCH",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": COMPLAINT_UPDATE,
        "auth_required": True
    },

    # GET LIST OF ALL COMPLAINTS
    {
        "url": "/api/admin/feedback/complaints/",
        "method": "GET",
        "auth_required": True
    },

    # GET TOTAL NUMBER OF IN PROGRESS COMPLAINTS
    {
        "url": "/api/admin/feedback/in-progress-complaints/",
        "method": "GET",
        "auth_required": True
    },

    # GET TOTAL NUMBER OF PENDING COMPLAINTS
    {
        "url": "/api/admin/feedback/pending-complaints/",
        "method": "GET",
        "body_params": {
                    "examples": {
                        "response": {
                        "value": {
                            "total_pending": 10,
                            "percentage_increment": 25
                        }
                        }
                    }
                },
        "auth_required": True
    },

    # GET TOTAL NUMBER OF RESOLVED COMPLAINTS
    {
        "url": "/api/admin/feedback/resolved-complaints/",
        "method": "GET",
        "body_params":None
    },
]