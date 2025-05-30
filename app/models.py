import bcrypt
from fastapi import HTTPException
from sqlalchemy import ForeignKey, text, String, SmallInteger, Table, Column, DateTime, select
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from starlette import status

from app.database import Base, session_maker, first_or_create
from datetime import datetime


class PasswordEncryption:
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Admin(Base, PasswordEncryption):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str] = mapped_column(String[10], unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str] = mapped_column(nullable=True)
    is_super: Mapped[bool] = mapped_column(default=False)


class Client(Base, PasswordEncryption):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String[10], unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    account: Mapped[int] = mapped_column(nullable=True, default=0)

    orders = relationship("Order", back_populates='client')

    def get_or_create_current_order(self):
        with session_maker() as session:
            order_obj = first_or_create(session, Order, None, client_id=self.id, status_id=Order.STATUS_NEW_ID)
        return order_obj

    def get_current_order(self, session):
        order_obj = session.query(Order).filter_by(
            client_id=self.id,
            status_id=Order.STATUS_NEW_ID
        ).one_or_none()
        if order_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет активной корзины")
        return order_obj


class Order(Base):
    STATUS_NEW_ID = 0
    STATUS_PAID_ID = 1
    STATUS_APPROVED_ID = 2
    STATUSES = {
        STATUS_NEW_ID: 'Новый',
        STATUS_PAID_ID: 'Оплачен',
        STATUS_APPROVED_ID: 'Отправлен',
    }

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    status_id: Mapped[int] = mapped_column(SmallInteger)
    price: Mapped[int] = mapped_column(server_default=text("0"))
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    client = relationship("Client", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")

    def update_price(self):
        total = 0
        with session_maker() as session:
            order_obj = session.get(Order, self.id)

            for product in order_obj.order_products:
                total += product.price * product.quantity

            order_obj.price = total

            session.commit()

    def payment(self, session):
        client = self.client
        if client.account < self.price:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно денег")

        client.account -= self.price

        session.add(client)
        session.commit()


class OrderProduct(Base):
    product_size_id: Mapped[int] = mapped_column(ForeignKey('product_sizes.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    quantity: Mapped[int] = mapped_column(SmallInteger)
    price: Mapped[int] = mapped_column(server_default=text("0"))

    order = relationship("Order", back_populates="order_products")
    product_size = relationship("ProductSize", back_populates="order_products")


class Product(Base):
    model_color_id: Mapped[int] = mapped_column(ForeignKey('model_colors.id'))
    price: Mapped[int] = mapped_column(server_default=text("0"))

    model_color = relationship("ModelColor", back_populates="products")
    product_size = relationship("ProductSize", back_populates="product")

    # order_products = relationship("OrderProduct", back_populates="product")


class Size(Base):
    ru: Mapped[str] = mapped_column(String[6])
    cm: Mapped[str] = mapped_column(String[6])

    product_size = relationship("ProductSize", back_populates="size")


class ProductSize(Base):
    size_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(SmallInteger)

    product = relationship('Product', back_populates='product_size')
    size = relationship('Size', back_populates='product_size')

    order_products = relationship("OrderProduct", back_populates="product_size")


class ModelColor(Base):
    name: Mapped[str]
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id'))

    model = relationship('Model', back_populates='model_colors')
    color = relationship('Color', back_populates='models')
    products = relationship('Product', back_populates='model_color')


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

    models = relationship('ModelColor', back_populates='color')
    base_colors: Mapped[List["BaseColor"]] = relationship('BaseColor', secondary=base_color_color,
                                                          back_populates='colors')


class BaseColor(Base):
    name: Mapped[str]
    hex: Mapped[str] = mapped_column(String[6])

    colors: Mapped[List["Color"]] = relationship('Color', secondary=base_color_color, back_populates='base_colors')
