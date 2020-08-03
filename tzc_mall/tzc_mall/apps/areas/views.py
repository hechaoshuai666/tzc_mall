import logging

from django import http
from django.views import View
from django.core.cache import cache

from tzc_mall.utils.response_code import RETCODE
from .models import Area

logger = logging.getLogger('django')

class AreasView(View):


    def get(self,request):
        area_id = request.GET.get('area_id')

        if not area_id:

            province_list = cache.get('province_list')
            if not province_list:
                try:
                    # 没有area_id,代表是省份
                    province_model_list = Area.objects.filter(parent_id__isnull=True)
                    province_list = []
                    for province in province_model_list:
                        province_dict = {
                            'id':province.pk,
                            'name':province.name
                        }
                        province_list.append(province_dict)

                    cache.set('province_list', province_list, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code':RETCODE.DBERR,'errmsg':'查询省份数据失败'})

            return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','province_list':province_list})



        else:

            sub_data = cache.get('sub_area_' + area_id)

            if not sub_data:
                try:
                    # 没有area_id,代表是省份
                    parent_area = Area.objects.get(pk=area_id)
                    sub_area_model = parent_area.subs.all()
                    subs = []
                    sub_data = {
                        'id':parent_area.pk,
                        'name':parent_area.name,
                        'subs':subs
                    }
                    for sub in sub_area_model:
                        subs.append({'id': sub.pk,'name': sub.name})

                    cache.set('sub_area_' + area_id, sub_data, 3600)

                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查询市区数据失败'})

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'sub_data': sub_data})