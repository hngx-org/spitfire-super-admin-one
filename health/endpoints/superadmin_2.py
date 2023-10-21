from datetime import datetime, timedelta
from health.helpers import update

BASE_URL = "https://team-mirage-super-amind2.onrender.com/api/v1/super-admin"

NAME = "SUPERADMIN 2"
CURRENT_DATE = datetime.now()
USER_ID = "a1ce9fdc-1068-4771-8e2c-795196adc1cc"
PRODUCT_ID = "07b97ad9-6065-4099-a36a-83d9f4d4f86b"
ORDER_ID = "008473c9-b24a-413e-aba6-8f24b6840466"
COMPLAINT_ID = 3554
USER_DETAILS = {
        "id": "79a7099e-34e4-4e49-8856-15ab6ed1380c",
        "first_name": "Zuri",
        "last_name": "Health Check",
        "email": "zurihealthcheck@gmail.com",
        "profile_pic": "https://random.jpg"
    }
USER_PURCHASE =  {
    "user": USER_ID,
    "order": ORDER_ID,
    "created_at": CURRENT_DATE.strftime('%Y-%m-%d')
}
COMMENT = {
    "user": USER_ID,
    "comment": "A stupid comment",
    "complaint": COMPLAINT_ID,
    "user_details": USER_DETAILS,
}
COMPLAINT = {
    "user": USER_ID,
    "product": PRODUCT_ID,
    "complaint_text": "A serious complaint",
}

QUERY_PARAMS = {
    "page": 1,
    "page_size": 10,
    "start_date": f"{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}",
    "end_date": f"{(CURRENT_DATE).strftime('%Y-%m-%d')}",
}

async def extract_complaint_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    return "complaint", response.get("data").get("id")

async def extract_comment_id(response: dict) -> "tuple[str, str]":
    """
    Extract the data from the response

    :param response: response from the endpoint

    :return: data from the response
    """
    return response.get("data").get("id")

ENDPOINTS_CONFIG = [

    #GET ALL USER ACTIVITIES
    {
        "url": "/analytics/activities/",
        "method": "GET",
        "query_params": {
            "page": QUERY_PARAMS.get("page"),
            "page_size": QUERY_PARAMS.get("page_size"),
        },
        "auth_required": True
    },

    #GET LIST OF BEST SELLING PRODUCTS BASED ON TOTAL ORDERS
    {
        "url": "/analytics/best-selling-products/",
        "method": "GET",
        "query_params": QUERY_PARAMS,
        "auth_required": True
    },

    #GENERATE ANALYTICS WITHIN A GIVEN DATE RANGE
    {
        "url": "/analytics/data/",
        "method": "GET",
        "query_params": {
            "start_date": QUERY_PARAMS.get("start_date"),
            "end_date": QUERY_PARAMS.get("end_date"),
        },
        "auth_required": True
    },

    # EXPORT REPORT DATA IN SPECIFIC FILE FORMAT
    {
        "url": "/analytics/export-report/", #NEEDS ATTENTION
        "method": "GET",
        "query_params": {
            "file_format": "pdf",
            "start_date": QUERY_PARAMS.get("start_date"),
            "end_date": QUERY_PARAMS.get("end_date"),
            "page": QUERY_PARAMS.get("page"),
            "page_size": QUERY_PARAMS.get("page_size"),
            
        },
        "auth_required": True
    },

    # GET PERFORMNACE METRICS DATA FOR A SPECIFIED DATE
    {

        "url": "/analytics/performance-data/?start_date=2023-01-01&end_date=2023-01-31&start_time=00:00:00&end_time=23:59:59&page=1&page_size=10",
        "method": "GET",
        "query_params": {
            "start_date": QUERY_PARAMS.get("start_date"),
            "end_date": QUERY_PARAMS.get("end_date"),
            "start_time": "00:00:00",
            "end_time": "23:59:59",
            "page": QUERY_PARAMS.get("page"),
            "page_size": QUERY_PARAMS.get("page_size"),
        },
        "auth_required": True
    },

    #GET USER_ID OF NEWLY CREATED PORTFOLIOS
    {
        "url": "/analytics/portfolio-activity/",
        "method": "POST",
        "auth_required": True
    },

    # GET ANALYTICS PORTFOLIO SUMMARY FOR A SPECIFIC DATE RANGE
    {
        "url": "/analytics/portfolio-summary/",
        "method": "GET",
        "query_params": {
            "start_date": QUERY_PARAMS.get("start_date"),
            "end_date": QUERY_PARAMS.get("end_date"),
        },
        "auth_required": True
    },
    
    # GET TOTAL SALES,USERS AND ORDERS WITHIN A GIVEN TIME FRAME
    {
        "url": "/analytics/total-sales-orders-users/",
        "method": "GET",
        "query_params": {
            "start_date": f"{(CURRENT_DATE - timedelta(days=7)).strftime('%Y-%m-%d')}",
            "end_date": f"{(CURRENT_DATE).strftime('%Y-%m-%d')}",
            "last": "7days"
        },
        "auth_required": True
    },

    # POST TRACK A USER PRODUCT PURCHASE - EDIT THIS ENDPOINT #Returns 500 (DB ISSUE?)
    {
        "url": "/analytics/user-purchase-activity/",
        "method": "POST",
        "body_params": USER_PURCHASE,
        "auth_required": True
    },

    # CREATE COMPLAINT
    {
        "url": "/feedback/register-complaints/",
        "method": "POST",
        "body_params": COMPLAINT,
        "auth_required": True,
        "extractor": extract_complaint_id
    },

    # POST CREATE A COMMENT FOR A COMPLAINT
    {
        "url": "/feedback/comments/",
        "method": "POST",
        "body_params": COMMENT,
        "auth_required": True,
        "extractor": extract_complaint_id

    },

    # GET LIST OF ALL COMPLAINTS
    {
        "url": "/feedback/complaints/",
        "method": "GET",
        "query_params": {"page": QUERY_PARAMS.get("page"),
                         "page_size": QUERY_PARAMS.get("page_size"),
                        },
        "auth_required": True
    },

    #DELETE A COMMENT
    {
        "url": "/feedback/complaints/7153/comments",
        "method": "DELETE",
        "auth_required": True
    },
    

    # DELETE A COMPLAINT
    {
       "url": "/feedback/complaints/16694/",
        "method": "DELETE",
        "auth_required": True
    },


    # GET LIST OF ALL COMPLAINTS
    {
        "url": "/feedback/complaints/",
        "method": "GET",
        "auth_required": True
    },

    # GET TOTAL NUMBER OF COMPLAINTS BY STATUS
    {
        "url": "/feedback/complaints/in-progress/",
        "method": "GET",
        "auth_required": True
    },

    # GET TOTAL NUMBER OF COMPLAINANTS BYM STATUS AND PERCENTAGE INCREASE DAILY
    {
        "url": "/feedback/complaints/pending/",
        "method": "GET",
        "auth_required": True
    },

    # GET TOTAL NUMBER OF RESOLVED COMPLAINTS
    {
        "url": "/feedback/complaints/resolved/",
        "method": "GET",
        "auth_required": True
    },

    # FEEDBACK COMPLAINTS SEARCH CREATE
    {
        "url": "/feedback/complaints/search/",
        "method": "POST",
        "auth_required": True
    },

    # GET Get Complaint from Reviews Team using complaint ID
    {
        "url": "/feedback/complaints/{complaint_id}/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "auth_required": True
    },

    # PATCH Update the status of Complaint from pending to in progress or resolved
    # Throwing 406
    {
        "url": "/feedback/complaints/{complaint_id}/",
        "method": "PATCH",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "body_params": update(
            COMPLAINT, {"status": "resolved"}
        ),
        "auth_required": True
    },


    # GET LIST OF ALL COMMENTS FOR SPECIFIC COMPLAINT 
    {
        "url": "/feedback/complaints/{complaint_id}/comments/",
        "method": "GET",
        "path_params": {
            "complaint_id": f"{COMPLAINT_ID}"
        },
        "auth_required": True
    },

    # GET TOTAL NUMBER OF COMPLAINTS WITH PERCENTAGE INCREASE DAILY
    {
        "url": "/feedback/total-complaints/",
        "method": "GET",
        "auth_required": True
    },
    
    

]