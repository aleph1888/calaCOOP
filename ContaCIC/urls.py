from django.conf.urls import patterns, include, url

from django.contrib import admin
from Invoices.admin import user_admin_site
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
#import django_cron

#django_cron.autodiscover()

admin.autodiscover()
js_info_dict = {
	'packages': ('Invoices.package',),
}
urlpatterns = patterns('',
url(r'^soci/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
url(r'^soci/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
url(r'^soci/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',  name='password_reset_confirm'),
url(r'^soci/reset/done/$', 'django.contrib.auth.views.password_reset_complete',  name='password_reset_complete'),
url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
url(r'^i18n/', include('django.conf.urls.i18n')),
url(r'^admin/', include(admin.site.urls)),
url(r'^soci/', include(user_admin_site.urls)),
url(r'^invoices/', include('Invoices.urls', namespace='Invoices')),
url(r'^users/', include('users.urls', namespace='users')) 
)

#Add this to serve static files like csv (config in settings.py)
urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
