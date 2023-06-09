"""${message}

Revision ID: 9b1d3dcf21f9
Revises: ${down_revision | comma,n}
Create Date: 

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9b1d3dcf21f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    account = op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('account')