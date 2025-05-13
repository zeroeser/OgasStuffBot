from sqlalchemy import String, ForeignKey, types, BigInteger
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from app.dao.database import Base
from app.dao.enum_models import OrderStatus, CurrencyType


class CompanyAdmin(Base):
    __tablename__ = 'companies_administrators'

    # Связи
    user_id: Mapped[UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    merchant_ids: Mapped[list[UUID]] = mapped_column(types.UUID, ForeignKey("companies.id"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    user_id: Mapped[BigInteger]
    username: Mapped[str]
    address: Mapped[str | None]
    value: Mapped[float | None]


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.pending)
    cost: Mapped[float] = mapped_column(default=0)

    # Связи
    user_id: Mapped[UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    merchant_id: Mapped[list[UUID]] = mapped_column(types.UUID, ForeignKey("orders.id"))


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    base_merch_id: Mapped[UUID] = mapped_column(ForeignKey("base_merches.id"))
    variant_id: Mapped[UUID | None] = mapped_column(ForeignKey("merch_variants.id"))

    quantity: Mapped[int] = mapped_column(default=1)
    price_per_item: Mapped[float]  # Фиксируем цену на момент заказа
    total_price: Mapped[float]

    # Связи
    order: Mapped["Order"] = relationship(back_populates="items")
    base_merch: Mapped["BaseMerch"] = relationship()
    variant: Mapped["MerchVariant | None"] = relationship()


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    company: Mapped[str]

    # Связи
    merch_variants: Mapped[list["BaseMerch"] | None] = relationship(
        back_populates="merch", cascade="all, delete-orphan"
    )


class BaseMerch(Base):
    __tablename__ = "base_merches"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    name: Mapped[str]
    cost: Mapped[float]
    is_available: Mapped[bool]
    quantity: Mapped[int] = mapped_column(default=0)
    currency_type: Mapped[CurrencyType] = mapped_column(SQLAlchemyEnum(CurrencyType), default=CurrencyType.CNY)

    # Связи
    variants: Mapped[list["MerchVariant"] | None] = relationship(
        back_populates="base_merch", cascade="all, delete-orphan"
    )
    images: Mapped[list["MerchImage"]] = relationship(
        back_populates="mech",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def primary_image(self) -> str | None:
        for img in sorted(self.images, key=lambda x: x.position):
            if img.is_primary:
                return img.url
        return self.images[0].url if self.images else None


class MerchImage(Base):
    __tablename__ = 'product_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    url: Mapped[str] = mapped_column(String)
    is_primary: Mapped[bool] = mapped_column(default=False)
    position: Mapped[int]

    # Связи
    mech: Mapped["BaseMerch"] = relationship(back_populates="images")


class MerchVariant(Base):
    __tablename__ = "merch_variants"

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
    is_available: Mapped[bool | None]
    size: Mapped[str | None]
    color: Mapped[str | None]
    quantity: Mapped[int | None]



