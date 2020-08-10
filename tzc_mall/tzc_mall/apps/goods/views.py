from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator

from contents.utils import get_categories
from .models import GoodsCategory
from .utils import get_breadcrumb


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

        context = {
            'categories':categories,
            'breadcrumb':breadcrumb
        }
        return render(request,'list.html',context)
