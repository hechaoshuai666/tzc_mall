from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage

from contents.utils import get_categories
from .utils import get_breadcrumb
from .models import GoodsCategory,SKU
from tzc_mall.utils.response_code import RETCODE


class HotView(View):

    def get(self,request,category_id):

        try:
            hot_skus = SKU.objects.filter(is_launched=True,category_id=category_id).order_by('-sales')[:2]
        except:
            return http.JsonResponse({'code':RETCODE.NODATAERR,"errmsg":"OK","hot_skus":[]})

        sku_list = []

        for sku in hot_skus:
            sku_list.append({
                'id':sku.pk,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })
        return http.JsonResponse({'code':RETCODE.OK,"errmsg":"OK","hot_skus":sku_list})


class ListView(View):
    '''
    渲染商品列表
    '''
    def get(self,request,category_id,page_num):
        '''

        :param request:
        :param category_id: 商品id
        :param page_num: 页码
        :return:
        '''
        categories = get_categories()

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('缺少category_id参数')

        breadcrumb = get_breadcrumb(category)


        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')
        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'
            sort_field = '-create_time'

        skus = category.skus.filter(is_launched=True).order_by(sort_field)


        paginator = Paginator(skus,5)
        # 获取每页商品数据
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return http.HttpResponseNotFound('页面不存在')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'page_skus':page_skus,
            'sort':sort,
            'total_page':total_page,
            'page_num':page_num,
            'category_id':category_id
        }
        return render(request,'list.html',context)
