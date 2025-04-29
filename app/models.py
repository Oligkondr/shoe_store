from sqlalchemy import ForeignKey, text, String, SmallInteger, Table, Column, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from app.database import Base
from datetime import datetime


class Admin(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column(String[10], unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str] = mapped_column(nullable=True)
    is_super: Mapped[bool] = mapped_column(default=False)


class Client(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str] = mapped_column(String[10], unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    account: Mapped[int] = mapped_column(server_default=text("0"))

    orders = relationship("Order", back_populates='client')


class Order(Base):
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    status_id: Mapped[int] = mapped_column(SmallInteger)
    price: Mapped[int] = mapped_column(server_default=text("0"))
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    quantity: Mapped[int] = mapped_column(SmallInteger)
    price: Mapped[int] = mapped_column(server_default=text("0"))

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


class Product(Base):
    model_color_id: Mapped[int] = mapped_column(ForeignKey('model_colors.id'))
    size_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'))
    price: Mapped[int] = mapped_column(server_default=text("0"))
    quantity: Mapped[int] = mapped_column(SmallInteger)

    size = relationship('Size', back_populates='products')
    order_products = relationship("OrderProduct", back_populates="product")


class Size(Base):
    ru: Mapped[str] = mapped_column(String[6])
    cm: Mapped[str] = mapped_column(String[6])

    products = relationship('Product', back_populates='size')


class ModelColor(Base):
    name: Mapped[str]
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id'))

    model = relationship('Model', back_populates='model_colors')


class Model(Base):
    name: Mapped[str]
    description: Mapped[str]
    sex_id: Mapped[int] = mapped_column(SmallInteger)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    model_colors = relationship('ModelColor', back_populates='model')
    category = relationship('Category', back_populates='models')


class Category(Base):
    name: Mapped[str]

    models = relationship('Model', back_populates='category')


base_color_color = Table(
    'base_color_color',
    Base.metadata,
    Column('base_color_id', ForeignKey('base_colors.id'), primary_key=True),
    Column('color_id', ForeignKey('colors.id'), primary_key=True),
)


class Color(Base):
    name: Mapped[str] = mapped_column(nullable=True)

    base_colors: Mapped[List["BaseColor"]] = relationship('BaseColor', secondary=base_color_color,
                                                          back_populates='colors')


class BaseColor(Base):
    name: Mapped[str]
    hex: Mapped[str] = mapped_column(String[6])

    colors: Mapped[List["Color"]] = relationship('Color', secondary=base_color_color, back_populates='base_colors')
