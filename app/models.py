from sqlalchemy import ForeignKey, text, Text, String, SmallInteger, Date, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from app.database import Base, int_pk
from datetime import date


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String[10], unique=True, nullable=False)
    name = Mapped[str]
    surname: Mapped[str]
    account: Mapped[int]


class Admin(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String[10], unique=True, nullable=False)
    name = Mapped[str]
    surname = Mapped[str]
    is_super: Mapped[bool] = mapped_column(nullable=False, default=False)


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status_id: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    amount: Mapped[int] = mapped_column(server_default=text("0"))
    approved_at: Mapped[date] = mapped_column(Date, nullable=False)


class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(SmallInteger)
    amount: Mapped[int]


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    model_color_id: Mapped[int] = mapped_column(ForeignKey('modelcolors.id'), nullable=False)
    size_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'), nullable=False)
    qty: Mapped[int]


class Size(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    ru: Mapped[str] = mapped_column(String[6], nullable=False)
    eu: Mapped[str] = mapped_column(String[6], nullable=False)
    us_man: Mapped[str] = mapped_column(String[6], nullable=False)
    us_woman: Mapped[str] = mapped_column(String[6], nullable=False)
    inch: Mapped[str] = mapped_column(String[6], nullable=False)
    cm: Mapped[str] = mapped_column(String[6], nullable=False)


class ModelColor(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'), nullable=False)
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id'), nullable=False)


class Image(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    model_color_id: Mapped[int] = mapped_column(ForeignKey('modelcolors.id'), nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)


class Model(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    sex_id: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categorys.id'), nullable=False)


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


base_color_color = Table(
    'base_color_color',
    Base.metadata,
    Column('base_color_id', ForeignKey('basecolors.id'), primary_key=True, nullable=False),
    Column('color_id', ForeignKey('colors.id'), primary_key=True, nullable=False),
)


class Color(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    base_colors: Mapped[List["BaseColor"]] = relationship('BaseColor', secondary=base_color_color,
                                                          back_populates='colors')


class BaseColor(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hex: Mapped[str] = mapped_column(String[6], nullable=False)

    colors: Mapped[List["Color"]] = relationship('Color', secondary=base_color_color, back_populates='basecolors')
