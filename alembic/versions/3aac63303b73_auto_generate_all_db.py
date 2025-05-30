"""auto generate all db

Revision ID: 3aac63303b73
Revises: 
Create Date: 2025-05-25 17:32:56.203672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '3aac63303b73'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password_hashed', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('create_dtm', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_recurring', sa.Boolean(), nullable=False),
    sa.Column('recurrence_pattern', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY', name='recurrencepattern'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('create_dtm', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('eventversion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('version_id', sa.Uuid(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_recurring', sa.Boolean(), nullable=False),
    sa.Column('recurrence_pattern', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('edited_by', sa.Integer(), nullable=False),
    sa.Column('edited_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['edited_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eventversion_version_id'), 'eventversion', ['version_id'], unique=True)
    op.create_table('eventpermission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('permission', sa.Enum('owner', 'editor', 'view', name='permissionlevel'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eventpermission')
    op.drop_index(op.f('ix_eventversion_version_id'), table_name='eventversion')
    op.drop_table('eventversion')
    op.drop_table('event')
    op.drop_table('user')
    # ### end Alembic commands ###
