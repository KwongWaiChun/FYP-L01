"""Initial migration.

Revision ID: e41cc0fd4d83
Revises: 
Create Date: 2023-12-29 08:00:40.866950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e41cc0fd4d83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('translate_library',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=255), nullable=False),
    sa.Column('language_id', sa.String(length=255), nullable=False),
    sa.Column('translation_services', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('translate_library', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_translate_library_language_id'), ['language_id'], unique=True)

    op.create_table('user',
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('login_state', sa.Boolean(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('userID')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.Column('follow', sa.Integer(), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('nickname', sa.String(length=255), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_profile_username'), ['username'], unique=False)

    op.create_table('translate_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('text_input', sa.Text(), nullable=False),
    sa.Column('text_output', sa.Text(), nullable=False),
    sa.Column('translation_services', sa.String(length=255), nullable=False),
    sa.Column('language', sa.String(length=255), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('translate_record', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_translate_record_username'), ['username'], unique=False)

    op.create_table('translate_scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('translation_services', sa.String(length=255), nullable=False),
    sa.Column('scores', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('translate_scores', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_translate_scores_username'), ['username'], unique=False)

    op.create_table('translate_feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('translation_services', sa.String(length=255), nullable=False),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['translate_record.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('translate_feedback', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_translate_feedback_username'), ['username'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('translate_feedback', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_translate_feedback_username'))

    op.drop_table('translate_feedback')
    with op.batch_alter_table('translate_scores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_translate_scores_username'))

    op.drop_table('translate_scores')
    with op.batch_alter_table('translate_record', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_translate_record_username'))

    op.drop_table('translate_record')
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_profile_username'))

    op.drop_table('profile')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('translate_library', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_translate_library_language_id'))

    op.drop_table('translate_library')
    # ### end Alembic commands ###
