from collections import OrderedDict

from django.shortcuts import render



from django.views import View

from .models import ContentCategory
from goods import  models

class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 对商品进行筛选和排序
        # 创建有序字典
        categories = OrderedDict()

        # 提取37个频道
        channels = models.GoodsChannel.objects.order_by('group_id','sequence')

        for channel in channels:
            group_id = channel.group_id

            # 构造排序的结构
            if group_id not in categories:
                categories[group_id] = {'channels':[],'sub_cats':[]}

            # 获取一级菜单
            cat1 = channel.category

            # 添加一级菜单
            categories[group_id]['channels'].append({
                'id':cat1.id,
                'name':cat1.name,
                'url':channel.url
            })

            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)

                categories[group_id]['sub_cats'].append(cat2)

            # 广告数据
            contents = {}
            content_categories = ContentCategory.objects.all()
            for cat in content_categories:
                contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

            # 渲染模板的上下文
            context = {
                'categories': categories,
                'contents': contents,
            }




        return render(request, 'index.html',context)