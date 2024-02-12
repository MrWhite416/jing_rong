# 开发时间：2024/2/12  20:45
# The road is nothing，the end is all    --Demon


'''
Python对象序列化的基类

'''


class BasePaginateSerializer(object):
    """分页数据序列化基类"""

    def __init__(self, paginate):  # 简化代码，可以满足对象的拷贝
        self.pg = paginate
        if not self.pg:
            return paginate
        self.has_next = self.pg.has_next  # 是否还有下一页
        self.has_prev = self.pg.has_prev  # 是否还有上一页
        self.next_num = self.pg.next_num  # 下一页的页码
        self.page = self.pg.page  # 当前页的页码
        self.pages = self.pg.pages  # 匹配的元素在当前配置一共有多少页
        self.total = self.pg.total  # 匹配的元素总数

    def get_object(self, obj):
        """对象的内容,系列化的个性操作,子类重写"""
        return {}

    #
    def paginateInfo(self):
        """分页信息，是否有上下页，页数，总页数等"""
        return {
            'has_next': self.has_next,
            'has_prev': self.has_prev,
            'next_num': self.next_num,
            'page': self.page,
            'pages': self.pages,
            'total': self.total
        }

    def to_dict(self):
        """序列化分页数据"""
        pg_info = self.paginateInfo()
        paginate_data = []
        for obj in self.pg.items:
            paginate_data.append(self.get_object(obj))
        return {
            'paginateInfo': pg_info,
            'totalElements': pg_info['total'],
            'content': paginate_data
        }




class BaseSerializer(object):
    '''
    把Python对象转化为字典
    '''
    def __init__(self,data):
        self.data = data

    def to_dict(self):
        # 个性化的函数，具体功能需要子类重写
        return {}


class BaseListSerializer(object):
    '''
    python列表对象序列化基类
    '''

    def __init__(self,data):
        self.data_list = data
        # self.select_type_serializer()


    def select_type_serializer(self):
        if not self.data_list:
            return None
        if isinstance(self.data_list,list):  # 列表解析，判断数据类型
            if len(self.data_list) == 0:
                return None
            else:
                self.data_list = [dict(zip(result.keys(),result)) for result in self.data_list]

    def to_dict(self):
        # 个性化的函数，具体功能需要子类重写
        return {}














