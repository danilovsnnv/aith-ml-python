from sqlalchemy import ARRAY, Column, Enum, Float, Integer, String, Text

from models.base import Base

class Movies(Base):
    __tablename__ = 'movies'


    id = Column(Integer, primary_key=True, autoincrement=True)
    img_id = Column(Integer, nullable=False)
    title_id = Column(String, primary_key=True, index=False)
    poster_url = Column(String, nullable=True)
    item_type = Column(Enum("Movie", "TVSeries", name='item_type'), nullable=True)
    name = Column(String, nullable=True)
    original_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    featured_review = Column(Text, nullable=True)
    date = Column(String, nullable=True)
    rating_count = Column(Float, nullable=True)
    rating_value = Column(Float, nullable=True)
    genre = Column(ARRAY(String), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    stars = Column(ARRAY(String), nullable=True)
    directors = Column(ARRAY(String), nullable=True)
    creators = Column(ARRAY(String), nullable=True)
