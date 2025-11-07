from pydantic import BaseModel

class KoujyouReact(BaseModel):
  companyCode: str
  previousFactoryCode: str
  productFactoryCode: str
  startOperationDate: str
  endOperationDate: str
  previousFactoryName: str
  productFactoryName: str
  materialDepartmentCode: str
  environmentalInformation: str
  authenticationFlag: str
  groupCorporateCode: str
  integrationPattern: str
  hulftid: str

class Koujyou():
  company_code: str
  previous_factory_code: str
  product_factory_code: str
  start_operation_date: str
  end_operation_date: str
  previous_factory_name: str
  product_factory_name: str
  material_department_code: str
  environmental_information: str
  authentication_flag: str
  group_corporate_code: str
  integration_pattern: str
  hulftid: str