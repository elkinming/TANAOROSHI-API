from models.koujyou import KoujyouReact, Koujyou


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
        "uuid": n,
        } for a,b,c,d,e,f,g,h,i,j,k,l,m,n in db_data]
    
    return response_mapped

# function for map the Frontend data to the DB data structure
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
    mapped_obj.uuid = frontend_data.uuid

    return mapped_obj

# function for map the Frontend data to the DB data structure (Array)
def map_frontend_arr_to_db(frontend_arr_data):
    mapped_arr = []
    for frontend_element in frontend_arr_data:
        mapped_arr.append(map_frontend_to_db(frontend_element))
    return mapped_arr