from django.conf.urls import include, url

urlpatterns = [
    url(r'', 'website.views.home', name="home"),
]
