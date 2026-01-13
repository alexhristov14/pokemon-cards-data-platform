from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgres import JSONB
from sqlalchemy.orm import relationship

from common.database.postgres import Base


class RawCardPrice(Base):
    __tablename__ = "raw_card_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(String, nullable=False)
    raw_price = Column(Float, nullable=True)
    grade7_price = Column(Float, nullable=True)
    grade8_price = Column(Float, nullable=True)
    grade9_price = Column(Float, nullable=True)
    grade9_5_price = Column(Float, nullable=True)
    grade10_price = Column(Float, nullable=True)
    scraped_at = Column(DateTime, nullable=True)
    ingested_at = Column(DateTime, server_default=func.now(), nullable=False)


class CardMetadata(Base):
    __tablename__ = "card_metadata"

    id = Column(String, primary_key=True)
    card_id = Column(ForeignKey("raw_card_prices.id"), nullable=False)
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


class CardStatistics(Base):
    __tablename__ = "card_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(ForeignKey("raw_card_prices.id"), nullable=False)
    grade7_stats = Column(JSONB, default=dict, nullable=False)
    grade8_stats = Column(JSONB, default=dict, nullable=False)
    grade9_stats = Column(JSONB, default=dict, nullable=False)
    grade9_5_stats = Column(JSONB, default=dict, nullable=False)
    grade10_stats = Column(JSONB, default=dict, nullable=False)

    price = relationship("RawCardPrice", back_populates="statistics")
