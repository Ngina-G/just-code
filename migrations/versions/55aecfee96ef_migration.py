"""Migration

Revision ID: 55aecfee96ef
Revises: fe082af7bdeb
Create Date: 2022-05-19 19:36:24.570632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55aecfee96ef'
down_revision = 'fe082af7bdeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_subscriber_email', table_name='subscriber')
    op.drop_table('subscriber')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriber',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='subscriber_pkey')
    )
    op.create_index('ix_subscriber_email', 'subscriber', ['email'], unique=False)
    # ### end Alembic commands ###
