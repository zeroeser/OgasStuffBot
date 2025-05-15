from app.dao.base import BaseDAO
from app.models import Company


class CompanyDAO(BaseDAO[Company]):
    model = Company
