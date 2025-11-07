import psycopg2
import psycopg2.extras

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from db import db_connection
from models.koujyou import KoujyouReact, Koujyou

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
    

# Route for creating new records
@router.post("/record")
def create_record_list(koujyou_react: KoujyouReact):

    # transform params to Python Standards
    koujyou = map_frontend_to_db(koujyou_react)
    # print(koujyou.__dict__)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        cur.execute("""INSERT INTO m_koujyou 
        (
            company_code,
            previous_factory_code,
            product_factory_code,
            start_operation_date,
            end_operation_date,
            previous_factory_name,
            product_factory_name,
            material_department_code,
            environmental_information,
            authentication_flag,
            group_corporate_code,
            integration_pattern,
            hulftid
        ) 
        VALUES ( %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            koujyou.company_code,
            koujyou.previous_factory_code,
            koujyou.product_factory_code,
            koujyou.start_operation_date,
            koujyou.end_operation_date,
            koujyou.previous_factory_name,
            koujyou.product_factory_name,
            koujyou.material_department_code,
            koujyou.environmental_information,
            koujyou.authentication_flag,
            koujyou.group_corporate_code,
            koujyou.integration_pattern,
            koujyou.hulftid
        ))
        conn.commit()
        print("Transaction Saved!");
        # close connection
        cur.close()
        conn.close()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=koujyou.__dict__)

    except Exception as e:
        print("Error: %s", (e));
        cur.close()
        conn.close()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)

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


def map_frontend_to_db(frontend_data: KoujyouReact):
    mapped_obj = Koujyou()
    mapped_obj.company_code = frontend_data.companyCode
    mapped_obj.previous_factory_code = frontend_data.previousFactoryCode
    mapped_obj.product_factory_code = frontend_data.productFactoryCode
    mapped_obj.start_operation_date = frontend_data.startOperationDate
    mapped_obj.end_operation_date = frontend_data.endOperationDate
    mapped_obj.previous_factory_name = frontend_data.previousFactoryName
    mapped_obj.product_factory_name = frontend_data.productFactoryName
    mapped_obj.material_department_code = frontend_data.materialDepartmentCode
    mapped_obj.environmental_information = frontend_data.environmentalInformation
    mapped_obj.authentication_flag = frontend_data.authenticationFlag
    mapped_obj.group_corporate_code = frontend_data.groupCorporateCode
    mapped_obj.integration_pattern = frontend_data.integrationPattern
    mapped_obj.hulftid = frontend_data.hulftid

    return mapped_obj