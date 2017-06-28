# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

import private

# 创建对象基类
Base = declarative_base()

class HistoricalStockPrices(Base):
    # 表名
    __tablename__ = "historical_stock_prices"
    __table_args__ = {"mysql_charset":"utf8","mysql_engine":"InnoDB"}

    # 表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String(16), nullable=False)
    symbol = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(String(16), nullable=False)
    high = Column(String(16), nullable=False)
    low = Column(String(16), nullable=False)
    close = Column(String(16), nullable=False)
    volume = Column(String(32), nullable=False)

    def __repr__(self):
        return "<Stock quote(symbol='%s',date='%s',close='%s')>" % (
            self.symbol, self.date, self.close)

# 初始化数据库连接
engine = create_engine("mysql+mysqlconnector://root:%s@localhost:3306"
            "/stock" % private.configs["db_pwd"])
# 创建数据库会话类
DBSession = sessionmaker(bind=engine)

