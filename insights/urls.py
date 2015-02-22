from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'insights.views.home', name='home'),
    url(r'^api/data/$', 'insights.views.api_data', name='api_data'),
    url(r'^api/data/matrix/$', 'insights.views.api_coach_data_matrix', name='api_coach_data_matrix'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
