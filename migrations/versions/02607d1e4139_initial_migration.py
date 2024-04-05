"""Initial migration.

Revision ID: 02607d1e4139
Revises: 
Create Date: 2024-03-16 21:41:15.198123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02607d1e4139'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('language',
    sa.Column('langID', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('langID'),
    sa.UniqueConstraint('langID'),
    sa.UniqueConstraint('language')
    )
    op.create_table('translator',
    sa.Column('translatorID', sa.Integer(), nullable=False),
    sa.Column('translator', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('translatorID'),
    sa.UniqueConstraint('translator'),
    sa.UniqueConstraint('translatorID')
    )
    op.create_table('user',
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('login_state', sa.Boolean(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('userID'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('userID'),
    sa.UniqueConstraint('username')
    )
    op.create_table('profile',
    sa.Column('profileID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('icon', sa.String(length=100), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('profileID'),
    sa.UniqueConstraint('profileID')
    )
    op.create_table('translate_feedback',
    sa.Column('transl_feedbackID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('translatorID', sa.Integer(), nullable=False),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['translatorID'], ['translator.translatorID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('transl_feedbackID'),
    sa.UniqueConstraint('transl_feedbackID')
    )
    op.create_table('translation',
    sa.Column('translationID', sa.Integer(), nullable=False),
    sa.Column('languageCode', sa.String(length=10), nullable=False),
    sa.Column('translatorID', sa.Integer(), nullable=False),
    sa.Column('langID', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['langID'], ['language.langID'], ),
    sa.ForeignKeyConstraint(['translatorID'], ['translator.translatorID'], ),
    sa.PrimaryKeyConstraint('translationID'),
    sa.UniqueConstraint('translationID')
    )
    op.create_table('translate_record',
    sa.Column('transl_recordID', sa.Integer(), nullable=False),
    sa.Column('translationID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('text_input', sa.Text(), nullable=False),
    sa.Column('text_output', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['translationID'], ['translation.translationID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('transl_recordID'),
    sa.UniqueConstraint('transl_recordID')
    )
    op.create_table('translate_scores',
    sa.Column('transl_scoresID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('translationID', sa.Integer(), nullable=False),
    sa.Column('scores', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['translationID'], ['translation.translationID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('transl_scoresID'),
    sa.UniqueConstraint('transl_scoresID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translate_scores')
    op.drop_table('translate_record')
    op.drop_table('translation')
    op.drop_table('translate_feedback')
    op.drop_table('profile')
    op.drop_table('user')
    op.drop_table('translator')
    op.drop_table('language')
    # ### end Alembic commands ###
