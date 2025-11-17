import psycopg2
import psycopg2.extras

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from db import db_connection
from models.koujyou import KoujyouReact, Koujyou
from utils.utils import map_db_array, map_frontend_arr_to_db, map_frontend_to_db
from services.inventory.update_batch_record import update_batch_record

import uuid

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

columns = [
    "company_code",
    "previous_factory_code",
    "product_factory_code",
    "start_operation_date::text", # Add convertion for date in LIKE clause
    "end_operation_date::text", # Add convertion for date in LIKE clause
    "previous_factory_name",
    "product_factory_name",
    "material_department_code",
    "environmental_information",
    "authentication_flag",
    "group_corporate_code",
    "integration_pattern",
    "hulftid"
]

@router.get("/record-list")
def read_record_list(previousFactoryCode: str = "", productFactoryCode: str = "", searchKeyword:str = ""):

    # transform params to Python Standards
    previous_factory_code = previousFactoryCode
    product_factory_code = productFactoryCode
    search_keyword = searchKeyword

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    # cur = conn.cursor()

    # Query to Execute
    like_pattern_a= f"%{previous_factory_code}%"
    like_pattern_b = f"%{product_factory_code}%"
    like_pattern_c = f"%{search_keyword}%"

    where_clause = f'WHERE previous_factory_code LIKE %s AND product_factory_code LIKE %s'
    sql_params_tuple_a = (like_pattern_a, like_pattern_b)

    # logic for modifing the where clause based on search_keyword
    if search_keyword != "":
        keyword_clause = " OR ".join([f"{col} LIKE %s" for col in columns])
        where_clause = where_clause + f' AND ({keyword_clause})'
        sql_params_tuple_b = tuple([like_pattern_c] * len(columns))
        sql_params_tuple = sql_params_tuple_a + sql_params_tuple_b
    else:
        sql_params_tuple = sql_params_tuple_a


    print(where_clause)
    print(sql_params_tuple)
    
    cur.execute("SELECT * from m_koujyou " + where_clause + "ORDER BY company_code, previous_factory_code, product_factory_code, start_operation_date, end_operation_date;", 
        sql_params_tuple            
    )
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
def create_record(koujyou_react: KoujyouReact):

    # transform params to Python Standards
    koujyou = map_frontend_to_db(koujyou_react)
    # print(koujyou.__dict__)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        cur.execute("""INSERT INTO m_koujyou 
        (
            company_code, previous_factory_code, product_factory_code, start_operation_date,
            end_operation_date, previous_factory_name, product_factory_name, material_department_code,
            environmental_information, authentication_flag, group_corporate_code, integration_pattern,
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

# Function for updating Records
@router.put("/record")
def update_record(koujyou_react: KoujyouReact):

    # transform params to Python Standards
    koujyou = map_frontend_to_db(koujyou_react)
    # print(koujyou.__dict__)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        cur.execute("""UPDATE m_koujyou SET 
            company_code = %s,
            previous_factory_code = %s,
            product_factory_code = %s,
            start_operation_date = %s,
            end_operation_date = %s,
            previous_factory_name = %s,
            product_factory_name = %s,
            material_department_code = %s,
            environmental_information = %s,
            authentication_flag = %s,
            group_corporate_code = %s,
            integration_pattern = %s,
            hulftid = %s
        WHERE
            company_code = %s AND
            previous_factory_code = %s AND
            product_factory_code = %s AND
            start_operation_date = %s AND
            end_operation_date = %s """, 
        
        (
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
            koujyou.hulftid,

            # Add fields again for WHERE clause
            koujyou.company_code,
            koujyou.previous_factory_code,
            koujyou.product_factory_code,
            koujyou.start_operation_date,
            koujyou.end_operation_date,
        ))
        conn.commit()
        print("Transaction Saved!");
        # close connection
        cur.close()
        conn.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content=koujyou.__dict__)

    except Exception as e:
        print("Error: %s", (e));
        cur.close()
        conn.close()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)

# Route for inserting batch of new records
@router.post("/record-batch")
def insert_batch_record(koujyou_react_array: list[KoujyouReact]):

    # transform params to Python Standards
    koujyou_array = map_frontend_arr_to_db(koujyou_react_array)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        for koujyou in koujyou_array:

            cur.execute("""INSERT INTO m_koujyou 
            (
                company_code, previous_factory_code, product_factory_code, start_operation_date,
                end_operation_date, previous_factory_name, product_factory_name, material_department_code,
                environmental_information, authentication_flag, group_corporate_code,
                integration_pattern, hulftid
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

        # Transform data in JSON
        response = [koujyou.__dict__ for koujyou in koujyou_array]
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    except Exception as e:
        print("Error: %s", (e));
        cur.close()
        conn.close()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)

@router.put("/record-batch")
def put_record_batch(koujyou_react_array: list[KoujyouReact]):
    return update_batch_record(koujyou_react_array);

