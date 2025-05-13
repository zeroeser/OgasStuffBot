from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.dao.base import BaseDAO
from app.models import Order


class OrderDAO(BaseDAO[Order]):
    model = Order

    async def find_one_or_none_by_user_id(self, user_id: int):
        try:
            query = select(self.model).filter_by(user_id=user_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Запись {self.model.__name__} с ID {user_id} {'найдена' if record else 'не найдена'}."
            logger.info(log_message)
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {user_id}: {e}")
            raise
