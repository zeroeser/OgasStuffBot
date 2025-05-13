from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey, types, BigInteger
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from .enum_models import OrderStatus, CurrencyType


class CompanyAdmin(Base):
    __tablename__ = "companies_administrators"

    # Связи
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    company_id: Mapped[UUID] = mapped_column(
        types.UUID, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="admin_companies")
    company: Mapped["Company"] = relationship(back_populates="administrators")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    address: Mapped[str | None]
    value: Mapped[float | None]

    # Связи
    admin_companies: Mapped[list["CompanyAdmin"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_updates=False,
    )
    orders: Mapped[list["Order"] | None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"))
    status: Mapped[OrderStatus] = mapped_column(
        SQLAlchemyEnum(OrderStatus), default=OrderStatus.pending
    )

    # Связи
    user: Mapped["User"] = relationship(back_populates="orders")
    company: Mapped["Company"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    merch_id: Mapped[UUID] = mapped_column(ForeignKey("base_merches.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_order: Mapped[float]

    # Связи
    order: Mapped["Order"] = relationship(back_populates="items")
    merch: Mapped["BaseMerch"] = relationship()


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True, default=uuid4)
    company: Mapped[str]

    # Связи
    merch_items: Mapped[list["BaseMerch"] | None] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )
    administrators: Mapped[list["CompanyAdmin"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        passive_updates=False,
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="company")


class BaseMerch(Base):
    __tablename__ = "base_merches"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"))
    name: Mapped[str]
    cost: Mapped[str]

    # Связи
    company: Mapped["Company"] = relationship(back_populates="merch_items")
    images: Mapped[list["MerchImage"]] = relationship(
        back_populates="mech", cascade="all, delete-orphan"
    )

    @hybrid_property
    def primary_image(self) -> str | None:
        for img in sorted(self.images, key=lambda x: x.position):
            if img.is_primary:
                return img.url
        return self.images[0].url if self.images else None


class MerchImage(Base):
    __tablename__ = "merch_images"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    merch_id: Mapped[int] = mapped_column(ForeignKey("base_merches.id"))
    url: Mapped[str] = mapped_column(String)
    is_primary: Mapped[bool] = mapped_column(default=False)
    position: Mapped[int]

    # Связи
    mech: Mapped["BaseMerch"] = relationship(back_populates="images")
