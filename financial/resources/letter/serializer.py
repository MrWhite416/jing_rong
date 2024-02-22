# 开发时间：2024/2/21  15:32
# The road is nothing，the end is all    --Demon




from comment.utils.Serializers import BasePaginateSerializer

class LetterPaginateSerializer(BasePaginateSerializer):
    '''
    继承父类，同时子类需要把消息列表数据进行序列化
    '''

    def get_object(self, obj):
        return {
            'id':obj.id,
            'sendName':obj.sendID,  # 发送者名字
            'detailID':obj.detail_id,  # 新建详情ID
            'title':obj.letter_detail.title,  # 信件标题
            'detail':obj.letter_detail.detail,  # 信件详情内容
            'state':obj.state,  # 信件已读状态
            'sendTime':obj.letter_detail.pDate.strftime("%Y-%m-%d,%H:%M:%S")  # 发送时间
        }