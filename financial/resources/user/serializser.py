# 开发时间：2024/3/1  22:29
# The road is nothing，the end is all    --Demon

from comment.utils.Serializers import BaseListSerializer,BaseSerializer

class InvitedListSerializer(BaseListSerializer):
    '''
    邀请名单列表的序列化
    '''

    def to_dict(self):
        lst = []
        for obj in self.data_list:
            lst.append(
                {
                    'name': obj.username,
                    'registerTime': obj.registerTime.strftime('%Y-%m-%d'),
                    'award': '代金券'
                }
            )


class UserInfoSerializer(BaseSerializer):
    """用户信息序列化"""

    def to_dict(self):
        obj = self.data
        return {
            'id': obj.username,
            "realNameAuth": obj.realNameStatus,
            "phoneStatus": obj.phone,
            'loginPwdstatus': 1,
            "payPwdStatus": obj.payPwdStatus,
            'avatar': obj.avatar,
            'invite_code': obj.remark,
            'phone': obj.phone
        }