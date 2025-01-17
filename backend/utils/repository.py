from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import asc, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, data: dict, **filter_by) -> int:
        stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def find_all(
        self,
        filters: dict = None,
        order_by: str = None,
        order_desc: bool = False,
        limit: int = None,
        offset: int = None,
    ):
        """
        Find all records with optional filters, ordering, and pagination.
        """
        stmt = select(self.model)
        
        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                if isinstance(value, datetime):
                    stmt = stmt.where(getattr(self.model, field) == value.isoformat())
                elif isinstance(value, tuple) and len(value) == 2:  # Range filter
                    stmt = stmt.where(getattr(self.model, field).between(*value))
                else:
                    stmt = stmt.where(getattr(self.model, field) == value)
        
        # Apply ordering if provided
        if order_by:
            order_column = getattr(self.model, order_by, None)
            if order_column is not None:
                stmt = stmt.order_by(desc(order_column) if order_desc else asc(order_column))
        
        # Apply limit and offset for pagination
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)

        res = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in res.fetchall()]
    
    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        try:
            res = res.scalar_one().to_read_model()
        except NoResultFound:
            res = None
        return res
    
    async def custom_query(self, stmt):
        res = await self.session.execute(stmt)
        try:
            return [row[0].to_read_model() for row in res.fetchall()]
        except (AttributeError, TypeError):
            return res
