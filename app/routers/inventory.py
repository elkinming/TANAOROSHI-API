import psycopg2
import psycopg2.extras

from fastapi import APIRouter
from db import db_connection

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/record-list")
def read_record_list(previousFactoryCode: str = "", productFactoryCode: str = ""):

    # transform params to Python Standards
    previous_factory_code = previousFactoryCode
    product_factory_code = productFactoryCode

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    # cur = conn.cursor()

    # Query to Execute
    like_pattern_a= f"%{previous_factory_code}%"
    like_pattern_b = f"%{product_factory_code}%"
    cur.execute("SELECT * from m_koujyou WHERE previous_factory_code LIKE %s AND product_factory_code LIKE %s ;", (
        like_pattern_a,
        like_pattern_b
    ))
    records = cur.fetchall()

    records_mapped = map_db_array(records)

    response = {
        "data": records_mapped,
        "total": len(records_mapped),
        "success": True,
        "pageSize": 20,
        "current": 1
    }

    # close connection
    cur.close()
    conn.close()
    return response

# function for map the DB data to frontend data structure
def map_db_array(db_data):

    response_mapped = [{
        "companyCode": a, 
        "previousFactoryCode": b,
        "productFactoryCode": c,
        "startOperationDate": d,
        "endOperationDate": e,
        "previousFactoryName": f,
        "productFactoryName": g,
        "materialDepartmentCode": h,
        "environmentalInformation": i,
        "authenticationFlag": j,
        "groupCorporateCode": k,
        "integrationPattern": l,
        "hulftid": m,
        } for a,b,c,d,e,f,g,h,i,j,k,l,m in db_data]
    
    return response_mapped