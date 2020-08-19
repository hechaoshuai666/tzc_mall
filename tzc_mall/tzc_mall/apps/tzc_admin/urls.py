from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical

urlpatterns = [
    # 认证用户
    url(r'^authorizations', obtain_jwt_token),
    # 用户总数
    url(r'^statistical/total_count', statistical.UserTotalCountView.as_view()),
    # 日增用户
    url(r'^statistical/day_increment', statistical.DayUserIncrementCountView.as_view()),
    # 日活跃数
    url(r'^statistical/day_active',statistical.DayUserActiveCountView.as_view()),
    # 日下单用户数量
    url(r'^statistical/day_orders',statistical.DayUserOrderCountView.as_view()),
]
