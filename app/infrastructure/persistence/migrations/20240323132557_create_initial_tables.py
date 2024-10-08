"""create_initial_tables

Revision ID: 53c8fa3f4148
Revises: 
Create Date: 2024-03-23 13:25:57.010046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53c8fa3f4148'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('work_email', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_work_email'), 'users', ['work_email'], unique=True)
    op.create_table('records',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('type', sa.Enum('IN', 'OUT', name='recordtype'), nullable=False),
    sa.Column('ref_month', sa.Integer(), nullable=False),
    sa.Column('ref_year', sa.Integer(), nullable=False),
    sa.Column('ref_datetime', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_records_user_id_users'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_records'))
    )
    op.create_index(op.f('ix_records_ref_month'), 'records', ['ref_month'], unique=False)
    op.create_index(op.f('ix_records_ref_year'), 'records', ['ref_year'], unique=False)
    op.create_index(op.f('ix_records_user_id'), 'records', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_records_user_id'), table_name='records')
    op.drop_index(op.f('ix_records_ref_year'), table_name='records')
    op.drop_index(op.f('ix_records_ref_month'), table_name='records')
    op.drop_table('records')
    op.drop_index(op.f('ix_users_work_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
