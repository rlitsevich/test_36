from flask import Flask, jsonify
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///task_36_db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/shops', methods=['GET'])
def get_shops():
    shops = Shop.query.all()
    serialized = []
    for shop in shops:
        serialized.append({'shop_code': shop.shop_code, 'shop_name': shop.shop_name})
    return jsonify(serialized)


@app.route('/shop_stats', methods=['GET'])
def get_shop_stats():
    shop_stats = ShopStat.query.all()
    serialized = []
    for shop_stat in shop_stats:
        serialized.append({
            'shop_code': shop_stat.shop_code,
            'period': shop_stat.period,
            'sales': shop_stat.sales,
            'markup': shop_stat.markup
        })
    return jsonify(serialized)


@app.route('/shop_stats_full', methods=['GET'])
def get_shop_stats_full():
    shop_stats_full = session.query(Shop, ShopStat).join(ShopStat, Shop.shop_code == ShopStat.shop_code).all()
    serialized = []
    for shop_stat in shop_stats_full:
        serialized.append({
            'shop_name': shop_stat[0].shop_name,
            'shop_code': shop_stat[1].shop_code,
            'period': shop_stat[1].period,
            'p_month': shop_stat[1].period // 100,
            'p_year': shop_stat[1].period % 100,
            'sales': shop_stat[1].sales,
            'markup': shop_stat[1].markup
        })
    return jsonify(serialized)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == "__main__":
    app.run()
