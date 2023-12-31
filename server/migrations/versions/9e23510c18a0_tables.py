"""tables

Revision ID: 9e23510c18a0
Revises: 
Create Date: 2023-06-16 11:46:00.514006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e23510c18a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_notes_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('overall_performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('portfolio_value', sa.Integer(), nullable=False),
    sa.Column('pnl', sa.Float(), nullable=False),
    sa.Column('roi', sa.Float(), nullable=False),
    sa.Column('win_rate', sa.Float(), nullable=False),
    sa.Column('max_drawdown', sa.Float(), nullable=False),
    sa.Column('trade_duration', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_overall_performances_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_sites_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('entry_time', sa.Time(), nullable=False),
    sa.Column('exit_time', sa.Time(), nullable=False),
    sa.Column('symbol', sa.String(length=50), nullable=False),
    sa.Column('long_short', sa.String(length=10), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('entry_price', sa.Float(), nullable=False),
    sa.Column('exit_price', sa.Float(), nullable=False),
    sa.Column('pnl', sa.Float(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_trades_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_watchlists_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trade_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('trade_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name=op.f('fk_trade_tags_tag_id_tags')),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], name=op.f('fk_trade_tags_trade_id_trades')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlist_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('watchlist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['watchlist_id'], ['watchlists.id'], name=op.f('fk_watchlist_items_watchlist_id_watchlists')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist_items')
    op.drop_table('trade_tags')
    op.drop_table('watchlists')
    op.drop_table('trades')
    op.drop_table('sites')
    op.drop_table('overall_performances')
    op.drop_table('notes')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
