from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import event as sqlalchemy_event
from sqlalchemy.pool import Pool


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from zqfa.models.user import User
from zqfa.models.user_positions import UserPosition
from zqfa.models.event import Event
from zqfa.models.job import Job


def setUp(app):
    # Heroku closes idle connections after 55 seconds (see  https://devcenter.heroku.com/articles/request-timeout#long-polling-and-streaming-responses)
    # Therefore the pooling setting of sqlalchemy have to be adapted: http://docs.sqlalchemy.org/en/latest/core/pooling.html

    # in case this shouldn't be enough: http://stackoverflow.com/questions/16341911/sqlalchemy-error-mysql-server-has-gone-away

    engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"), pool_recycle=54)
    Base.metadata.create_all(bind=engine)


@sqlalchemy_event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()
