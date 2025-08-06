from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop.views import CategoryViewset, ProductViewset, ArticleViewset, AdminCategoryViewset, AdminArticleViewset, AdminProductViewset

schema_view = get_schema_view(
    openapi.Info(
        title='My API',
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#ici nous creons notre routeur
router = routers.SimpleRouter()
#puis nous declarions une url basee sur le mot cle 'category' et notre view
#afin que url generee soit celle que nous souhaitons 'api/category/'
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/product', AdminProductViewset, basename='admin-product')
router.register('admin/article', AdminArticleViewset, basename='admin-article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
