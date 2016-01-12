from template.render import render
from tornado.web import RequestHandler, HTTPError


class Handler(RequestHandler):
    template_name = None
    login_required = False
    methods_allowed = ['GET']

    def initialize(self):
        super().initialize()
        self.fields = self.request.arguments
        self.username = self.get_secure_cookie('username')


    def check_login(self, *args, **kwargs):
        if self.username is not None and self.login_required:
            self.redirect("/account/profile")
        else:
            file = render(self.template_name + '.html', self.extra_context(*args, **kwargs))
            self.write(file)

    def get_field(self, field):
        if field in self.fields:
            return self.fields[field][0]
        else:
            return None

    def get(self, *args, **kwargs):
        if self.request.method in self.methods_allowed:
            self.check_login(*args, **kwargs)
        else:
            raise HTTPError(405)

    post = get

    get_context = post_context = lambda self: {}

    def extra_context(self, *args, **kwargs):
        getattr(self, self.request.method.lower() + '_context')(*args, **kwargs)