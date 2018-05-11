from django.conf.urls import url
from django.urls import path, include


app_name = 'core'
urlpatterns = [
    # api urls
    url(r'^api/v0/', include('api_v0.urls'))
]
