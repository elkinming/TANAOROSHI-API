import psycopg2
import psycopg2.extras

from fastapi import status
from fastapi.responses import JSONResponse
from db import db_connection
from models.koujyou import KoujyouReact, Koujyou
from models.common import CommitRecordError, ErrorResponse, GenericError
from utils.utils import map_frontend_to_db, map_db_array, map_frontend_arr_to_db

# Route for deleting batch of records
def delete_multiple_records(koujyou_react_array: list[KoujyouReact]):
    
    # transform params to Python Standards
    koujyou_array = map_frontend_arr_to_db(koujyou_react_array)

    conn = db_connection.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    
    try:
        commit_process = True
        error_list = []
        for koujyou in koujyou_array:
          try:
            cur.execute("""DELETE FROM m_koujyou WHERE 
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
                  ))    
      
          except Exception as e:
            # Rollback for allowing next transactions to execute
            conn.rollback()
            commit_process = False

            print(e)
            error = CommitRecordError()
            error.level = 'E'
            error.message = e.diag.message_primary
            error.detail = e.diag.message_detail
            error.code = e.pgcode
            error.record = koujyou
            error_list.append(error);
  
          
        if (commit_process is True):   
          conn.commit()
          print("Transaction Processed!");
          cur.close()
          conn.close()

          # Transform data in JSON       
          return JSONResponse(status_code=status.HTTP_200_OK, content=None)
        
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
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error.model_dump())
