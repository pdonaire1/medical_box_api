from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken import views
from django.conf.urls import include
from . routers import router
from utils.views import ChangePasswordViewSet
from django.conf.urls.static import static
from django.conf import settings
from utils.views import ChangePasswordViewSet, ObtainAuthToken, ResetPasswordViewSet

urlpatterns = [
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', 
        # namespace='rest_framework')),
    # url(r'^api-token-auth/',
        # 'rest_framework_jwt.views.obtain_jwt_token'),
    # url(r'^api/api-token-auth/', views.obtain_auth_token),
    url(r'^api/api-token-auth/', ObtainAuthToken.as_view()),
    url(r'^api/change_password/', ChangePasswordViewSet.as_view()),
    url(r'^api/forgot-password/', ResetPasswordViewSet.as_view()),
    url(r'^api/change_password/', ChangePasswordViewSet.as_view()),
    url(r'^api/', include('cities_light.contrib.restframework3')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
)

# urlpatterns += router.urls