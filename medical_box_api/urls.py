from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views
from django.conf.urls import include
from . routers import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api-auth/', include('rest_framework.urls', 
    	namespace='rest_framework')),
    url(r'^api-token-auth/',
        'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/', include('cities_light.contrib.restframework3')),
    url(r'^api/', include(router.urls)),
    url(r'^api/api-token-auth/', views.obtain_auth_token)
]

# urlpatterns += router.urls