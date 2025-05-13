from enum import Enum


class OrderStatus(Enum):
    pending = "pending"
    confirmed = "confirmed"
    declined = "declined"
    paid_order = "paid_order"
    delivered = "delivered"


class CurrencyType(Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    CNY = "CNY"
