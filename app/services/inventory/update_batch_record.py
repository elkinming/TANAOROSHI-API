import psycopg2
import psycopg2.extras

from fastapi import status
from fastapi.responses import JSONResponse
from db import db_connection
from models.koujyou import KoujyouReact, Koujyou
from models.common import CommitRecordError, ErrorResponse, GenericError
from utils.utils import map_frontend_to_db, map_db_array, map_frontend_arr_to_db

# Route for inserting batch of new records
def update_batch_record(koujyou_react_array: list[KoujyouReact]):

    # transform params to Python Standards
    koujyou_array = map_frontend_arr_to_db(koujyou_react_array)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        commit_process = True
        error_list = []
        for koujyou in koujyou_array:

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
                uuid = %s """, 
            
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
                koujyou.uuid,
            ))    
      
              
          except Exception as e:
            # Rollback for allowing next transactions to excecute
            conn.rollback()
            commit_process = False

            error = CommitRecordError()
            error.level = 'E'
            error.message = e.diag.message_primary
            error.detail = e.diag.message_detail
            error.code = e.pgcode
            error.uuid = koujyou.uuid
            error_list.append(error);
  
          
        if (commit_process is True):   
          conn.commit()
          print("Transaction Saved!");
          cur.close()
          conn.close()

          # Transform data in JSON
          response = [koujyou.__dict__ for koujyou in koujyou_array]          
          return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
        
        else:
          cur.close()
          conn.close()
          print([error.__dict__ for error in error_list])
          response = ErrorResponse(errorList=error_list)  
          return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.model_dump())

    except Exception as e:
        print("Error: ", (e));
        cur.close()
        conn.close()
        error = GenericError()
        error.level = 'E'
        error.message = e.__str__()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error.model_dump())
