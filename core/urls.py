from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .customer import views as customer_views
from .courier import views as courier_views

customer_urlpatterns = [
    path('', customer_views.home, name='home'),
    path('profile/', customer_views.profile_page, name='profile'),
]
courier_urlpatterns = [
    path('', courier_views.home, name='home'),
]

urlpatterns = [
    path('', views.home, name='home'),

    path("sign-in/", auth_view.LoginView.as_view(template_name="core/sign-in.html"), name="sign-in"),
    path("sign-out/", auth_view.LogoutView.as_view(next_page="/"), name="sign-out"),
    path("sign-up/", views.sign_up, name="sign-up"),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/', include((courier_urlpatterns, 'courier'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
