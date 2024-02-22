# 开发时间：2024/2/20  19:57
# The road is nothing，the end is all    --Demon
from flask import g
from flask_restful import Resource
from comment.utils.decorators import login_required
from flask_restful.reqparse import RequestParser
from comment.models.user import User
from comment.models.Letter import Letter_Detail,Letter
from comment.models import db
from financial.resources.letter.serializer import LetterPaginateSerializer

class Letter_Res(Resource):
    '''
    发送消息的资源类
    '''

    # 使用登录拦截的装饰器
    method_decorators = [login_required]

    def post(self):
        '''
        发送消息
        :return:
        '''
        rp=RequestParser()
        rp.add_argument('title',required=True)
        rp.add_argument('group',required=False)  # 群发消息时的用户组，可以为空
        rp.add_argument('receive_id',required=False)  # 单发消息时接受者的id，可以为空
        rp.add_argument('content',required=True)

        args = rp.parse_args()
        title = args.get('title')
        group = args.get('group')
        receive_id = args.get('receive_id')
        content = args.get('content')

        # 发送者的用户id
        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()

        # 群发消息，group有三个值：0：普通用户组，1：管理员组，2：全体用户
        if group=='0' or group=='1':  # 根据用户角色查询所有的接收用户
            receive_lst = User.query.filter(User.role == int(group)).all()
        if group=='2':  # 群发消息给所有用户
            receive_lst = User.query.all()

        # 单个用户发送消息
        if receive_id:
            receive_user = User.query.filter(User.id == receive_id).first()
            if receive_user:
                receive_lst=[receive_user]

        # 把消息详情对象，插入数据库
        new_letter_detail = Letter_Detail(title=title,detail=content)
        db.session.add(new_letter_detail)
        db.session.flush()  # commit：表示提交到数据库中  flush：把数据刷新到数据库的缓冲区（表中没有数据，但是有自增的id）




        for receive_user in receive_lst:
            # 给每一个用户都发送消息
            letter = Letter(sendID=user.username,recID=receive_user.id,
                            detail_id=new_letter_detail.id,state=0)
            db.session.add(letter)

        db.session.commit()
        return {"msg":'ok'}

    def get(self):
        '''
        当前用户收到的消息列表（分页）
        :return:
        '''

        u_id = g.user_id  # 当前登录的用户的id
        user = User.query.filter(User.id == u_id).first()
        rp = RequestParser()
        rp.add_argument('curPage',required=True)  # 访问的页号
        rp.add_argument('perPage',required=True)  # 每页显示数据的条数
        args = rp.parse_args()

        cur_page = int(args.get('curPage'))
        per_page = int(args.get('perPage'))

        # letter_list：时pagination类型。包含分页的数据，同时在items属性中包含消息列表数据
        letter_list = Letter.query.filter(Letter.recID == u_id).paginate(cur_page,per_page,error_out=False)
        dict_data = LetterPaginateSerializer(letter_list).to_dict()
        return {'msg':'ok','data':dict_data}







