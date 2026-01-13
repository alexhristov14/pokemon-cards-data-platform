from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from common.database.postgres import Base


class RawCardPrice(Base):
    __tablename__ = "raw_card_prices"

    card_id = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(String, nullable=False)
    raw_price = Column(Float, nullable=True)
    grade7_price = Column(Float, nullable=True)
    grade8_price = Column(Float, nullable=True)
    grade9_price = Column(Float, nullable=True)
    grade9_5_price = Column(Float, nullable=True)
    grade10_price = Column(Float, nullable=True)
    scraped_at = Column(DateTime, nullable=True)
    ingested_at = Column(DateTime, server_default=func.now(), nullable=False)

    history = relationship("CardPriceHistory", back_populates="card")


class CardMetadata(Base):
    __tablename__ = "card_metadata"

    card_id = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(String, nullable=True)
    set_name = Column(String, nullable=True)
    pokemon_type = Column(String, nullable=True)
    rarity = Column(String, nullable=True)
    illustrator = Column(String, nullable=True)
    series = Column(String, nullable=True)
    numbers_in_set = Column(Integer, nullable=True)
    reverse = Column(Boolean, nullable=True)
    holo = Column(Boolean, nullable=True)
    first_edition = Column(Boolean, nullable=True)
    release_date = Column(DateTime, nullable=True)
