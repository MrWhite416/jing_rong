"""empty message

Revision ID: 9afa1a1fc165
Revises: f453f938faaa
Create Date: 2024-03-15 21:15:18.639570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9afa1a1fc165'
down_revision = 'f453f938faaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_expected_return',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.BIGINT(), nullable=True, comment='用户ID'),
    sa.Column('productId', sa.BIGINT(), nullable=True, comment='产品ID'),
    sa.Column('investRecord', sa.BIGINT(), nullable=True, comment='投资记录ID'),
    sa.Column('expectedDate', sa.DateTime(), nullable=True, comment='收益日期'),
    sa.Column('expectedMoney', sa.Float(precision=8, asdecimal=2), nullable=True, comment='收益金额'),
    sa.Column('createDate', sa.DateTime(), nullable=True, comment='创建日期'),
    sa.ForeignKeyConstraint(['investRecord'], ['t_invest_record.pId'], ),
    sa.ForeignKeyConstraint(['productId'], ['t_product.proId'], ),
    sa.ForeignKeyConstraint(['userId'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_matched_result',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False, comment='主键'),
    sa.Column('userId', sa.BIGINT(), nullable=True, comment='用户id'),
    sa.Column('debtId', sa.BIGINT(), nullable=True, comment='债权id'),
    sa.Column('investId', sa.BIGINT(), nullable=True, comment='投资记录主键'),
    sa.Column('transferSerialNo', sa.String(length=100), nullable=True, comment='交易流水号'),
    sa.Column('purchaseMoney', sa.Float(precision=8, asdecimal=2), nullable=True, comment='购买金额（匹配金额）'),
    sa.Column('confirmedDate', sa.DateTime(), nullable=True, comment='购买日期（匹配日期）'),
    sa.Column('isConfirmed', sa.Integer(), nullable=True, comment='是否确认'),
    sa.Column('matchDate', sa.DateTime(), nullable=True, comment='匹配上的日期'),
    sa.Column('fundType', sa.Integer(), nullable=True, comment='资金类型'),
    sa.Column('debtType', sa.Integer(), nullable=True, comment='债权类型'),
    sa.Column('isExecuted', sa.Integer(), nullable=True, comment='是否清算过'),
    sa.ForeignKeyConstraint(['debtId'], ['t_debt_info.id'], ),
    sa.ForeignKeyConstraint(['investId'], ['t_invest_record.pId'], ),
    sa.ForeignKeyConstraint(['userId'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_matched_result')
    op.drop_table('t_expected_return')
    # ### end Alembic commands ###
