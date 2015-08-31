import django.views.defaults
from django.conf.urls import include, url
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout

urlpatterns = [
    url(r'^$', 'website.views.index', name="index"),
    url(r'^myfiles$', 'website.views.myfiles', name="myfiles"),
    url(r'^cockpit$', 'website.views.cockpit', name="cockpit"),
    url(r'^upload', 'website.views.upload', name="upload"),
    url(r'^about', 'website.views.about', name="about"),

    # Ajax views
    url(r'^generate_registration_key$', 'website.views.generate_registration_key', name="generate_registration_key"),
    url(r'^mark_key_distributed$', 'website.views.mark_key_distributed', name="mark_key_distributed"),
    url(r'^revoke_key$', 'website.views.revoke_key', name="revoke_key"),
    url(r'^size_available$', 'website.views.size_available', name="size_available"),


    # Authentication views
    url(r'^register$', 'website.views.register', name="register"),
    url(r'^login$', django_login, name="login"),
    url(r'^logout$', django_logout, {'template_name': "registration/logout.html"}, name="logout"),

    # File downloading view
    url(r'^dl/(?P<fid>[-A-Za-z0-9_]+)$', 'website.views.download', name="download"),
    url(r'^get/(?P<fid>[-A-Za-z0-9_]+)$', 'website.views.get_file', name="get_file"),
    # File deleting view
    url(r'^rm/(?P<fid>[-A-Za-z0-9_]+)$', 'website.views.delete', name="delete"),

    # 404 page
    url(r'^404$', 'django.views.defaults.page_not_found')
]
