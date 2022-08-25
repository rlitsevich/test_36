from app import db, session, Base


class Shop(Base):
    __tablename__ = 'shops'
    shop_code = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(150), nullable=False)


class ShopStat(Base):
    __tablename__ = 'shop_stats'
    shop_code = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Numeric(18, 4))
    markup = db.Column(db.Numeric(18, 4))
    __table_args__ = (db.PrimaryKeyConstraint(shop_code, period), {})
