import datetime
BASE_URL = "https://team-mirage-super-amind2.onrender.com"
NAME = "SUPERADMIN 2"
CURRENT_DATE = datetime.now()
USER_ID = ""
ID = ''
COMPLAINT_ID = ''

ENDPOINTS_CONFIG = [

    #GET ALL USER ACTIVITIES
    {
        "url": "/api/admin/analytics/activities/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
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
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    #GENERATE ANALYTICS WITHIN A GIVEN DATE RANGE
    {
        "url": "/api/admin/analytics/data/",
        "method": "GET",
        "query_params": {
            "start_date": "{{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}}",
            "end_date": "{{(CURRENT_DATE).strftime('%Y-%m-%d')}}"
        },
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # GET ANALYTICS EXPORT REPORT LIST
    {
        "url": "/api/admin/analytics/export_report/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # GET METRIC VIEW, TRANSACTION LIST
    {
        "url": "/api/admin/analytics/get_metrics/",
        "method": "GET",
        "query_params": None,
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    #POST GET USER_ID OF NEWLY CREATED PORTFOLIOS
    {
        "url": "/api/admin/analytics/portfolio-activity/",
        "method": "POST",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # GET ANALYTICS PORTFOLIO SUMMARY LIST
    {
        "url": "/api/admin/analytics/portfolio_summary/",
        "method": "GET",
        "query_params":None,
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },
    
    # GET TOTAL SALES,USERS AND ORDERS WITHIN A GIVEN TIME FRAME
    {
        "url": "/api/admin/analytics/total-sales-orders-users/",
        "method": "GET",
        "query_params": {
            "start_date": "{{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}}",
            "end_date": "{{(CURRENT_DATE).strftime('%Y-%m-%d')}}",
            "last": 7
        },
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # POST TRACK A USER PRODUCT PURCHASE
    {
        "url": "/api/admin/analytics/user-purchase-activity/",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "user": "<integer>", #USER ID?
            "order": "<integer>", #ORDER ID?
            "created_at": "<dateTime>" #TIME ORDER WAS CREATED?
        },
        "auth_required": True
    },

    # GET FEEDBACK COMMENT LIST
    {
        "url": "/api/admin/feedback/comments/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # POST CREATE FEEDBACK COMMENT - FLAG FOR CORRECTION

    {
        "url": "/api/admin/feedback/comments/",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "id": f"{ID}",
            "user_id": "<string>",
            "comment": "<string>",
            "complaint_id": "<string>",
            "user_details": {
                "id": "<uuid>",
                "first_name": "<string>",
                "last_name": "<string>",
                "email": "<email>",
                "profile_pic": "<string>"
            },
            "createdAt": "<dateTime>",
            "updatedAt": "<dateTime>"
        },
        "auth_required": True

    },

    # GET FEEDBACK COMPLAINT LIST
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/listcomment/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    # GET Get Complaint from Reviews Team using complaint ID
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    # PATCH Update the status of Complaint from pending to in progress or resolved
    {
        "url": "/api/admin/feedback/complaints/{complaint_id}/",
        "method": "PATCH",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": {
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
        },
        "auth_required": True
    },

    # GET LIST OF ALL COMPLAINTS
    {
        "url": "/api/admin/feedback/complaints/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # GET TOTAL NUMBER OF IN PROGRESS COMPLAINTS
    {
        "url": "/api/admin/feedback/in-progress-complaints/",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    # GET TOTAL NUMBER OF PENDING COMPLAINTS
    {
        "url": "/api/admin/feedback/pending-complaints/",
        "method": "GET",
        "path_params": None,
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
        "path_params": None,
        "body_params":None
    }
    
    
]