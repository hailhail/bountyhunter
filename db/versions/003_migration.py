from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
request = Table('request', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('bounty', INTEGER),
    Column('description', TEXT),
    Column('isFilled', BOOLEAN),
    Column('lastVote', DATETIME),
    Column('timeAdded', DATETIME),
    Column('voteCount', INTEGER),
    Column('year', INTEGER),
    Column('cost', FLOAT),
    Column('url', TEXT),
    Column('bandcamp', TEXT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['request'].columns['bandcamp'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['request'].columns['bandcamp'].create()
