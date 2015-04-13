from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
request = Table('request', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('bounty', Integer),
    Column('cost', Float),
    Column('description', Text),
    Column('isFilled', Boolean),
    Column('lastVote', DateTime),
    Column('timeAdded', DateTime),
    Column('url', Text),
    Column('voteCount', Integer),
    Column('year', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['request'].columns['cost'].create()
    post_meta.tables['request'].columns['url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['request'].columns['cost'].drop()
    post_meta.tables['request'].columns['url'].drop()
