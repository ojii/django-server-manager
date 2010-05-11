from server_manager.models import Server
from server_manager.loader import backend_loader
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template import RequestContext, Template
from django.http import HttpResponse, Http404
from django.contrib import admin
from django.contrib.sites.models import Site

def dt2str(dt, request):
    t = Template('{{ dt }}')
    return t.render(RequestContext(request, {'dt': dt}))

class SiteWrapper(object):
    def __init__(self, site, backend, request):
        self.site = site
        self.backend = backend
        self.request = request
        
    def __getattr__(self, attr):
        return getattr(self.site, attr)
        
    def can_restart(self):
        return self.backend.can_restart(self.site.pk, self.request)
        
    def can_stop(self):
        return self.backend.can_stop(self.site.pk, self.request)
        
    def can_start(self):
        return self.backend.can_start(self.site.pk, self.request)
    
    def get_uptime(self):
        return self.backend.get_uptime(self.site.pk, self.request)


class ServerRestarterAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if not request.user.has_perm('server_manager.change_serverrestarter'):
            raise Http404
        if request.GET.get('ajax'):
            return self.ajax_call(request)
        sites = []
        for site in Site.objects.all():
            sites.append(SiteWrapper(site, self.backend, request))
        data = {
            'sites': sites,
            'media': self.media,
        }
        return render_to_response('server_manager/changelist.html', data, RequestContext(request))
        
    def ajax_call(self, request):
        site_id = request.POST.get('site_id', None)
        if not site_id:
            return self.ajax_response(False)
        try:
            site = Site.objects.get(pk=site_id)
        except Site.DoesNotExist:
            return self.ajax_response(False)
        action = request.POST.get('action', None)
        if action == 'restart':
            return self.ajax_response(self.backend.restart(site.pk, request))
        elif action == "start":
            return self.ajax_response(self.backend.start(site.pk, request))
        elif action == "stop":
            return self.ajax_response(self.backend.stop(site.pk, request))
        elif action == 'uptime':
            uptime = self.backend.get_uptime(site.pk, request)
            if uptime is None:
                return self.ajax_response(False)
            return self.ajax_response(dt2str(uptime, request))
        return self.ajax_response(False)

    def ajax_response(self, data):
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
        
    @property
    def backend(self):
        return backend_loader

admin.site.register(Server, ServerRestarterAdmin)
