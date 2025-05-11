from datetime import datetime

from sqlalchemy import func, create_engine, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, sessionmaker

from app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__[0].lower() + cls.__name__[1:]
        name = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

        if name.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return name + 'es'
        elif name.endswith('y'):
            # Заменяем 'y' на 'ies' (company -> companies)
            return name[:-1] + 'ies'
        else:
            # Добавляем 's' только если нет окончания 's'
            return name if name.endswith('s') else name + 's'

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=datetime.now)


def first_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        params = {**kwargs}
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance
