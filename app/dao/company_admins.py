from app.dao.base import BaseDAO
from app.models import CompanyAdmin


class CompanyAdminDAO(BaseDAO[CompanyAdmin]):
    model = CompanyAdmin
