# myapp/urls.py
from django.urls import path
from .import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("Image",views.ImageViewSet),
urlpatterns = [
    # image_router.register(I images Iviews. Product ImageViewSet)
    # path('upload/', ImageView.as_view(), name='image_upload'),
]
urlpatterns += router.urls