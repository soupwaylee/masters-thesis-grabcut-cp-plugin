"""empty message

Revision ID: 9962bfe38479
Revises: df638ad98491
Create Date: 2021-09-02 09:38:37.219927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9962bfe38479'
down_revision = 'df638ad98491'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grab_cut_interaction',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('session_id', sa.String(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('annotated_pixels', sa.Integer(), nullable=True),
    sa.Column('foreground_pixels', sa.Integer(), nullable=True),
    sa.Column('background_pixels', sa.Integer(), nullable=True),
    sa.Column('scribbles', sa.Integer(), nullable=True),
    sa.Column('foreground_scribbles', sa.Integer(), nullable=True),
    sa.Column('background_scribbles', sa.Integer(), nullable=True),
    sa.Column('submission_counter', sa.Integer(), nullable=True),
    sa.Column('first_interaction_time', sa.DateTime(), nullable=True),
    sa.Column('submission_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grab_cut_mask',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('session_id', sa.String(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('mask', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('grab_cut_interaction_model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grab_cut_interaction_model',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('annotated_pixels', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('foreground_pixels', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('background_pixels', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('scribbles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('foreground_scribbles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('background_scribbles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('submission_counter', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('first_interaction_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('submission_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='grab_cut_interaction_model_pkey')
    )
    op.drop_table('grab_cut_mask')
    op.drop_table('grab_cut_interaction')
    # ### end Alembic commands ###
