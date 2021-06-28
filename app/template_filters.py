from flask import Flask
import base64

class TemplateFiltersManager():
    def init_app(self, app: Flask):
        app.jinja_env.filters['b64encode'] = b64encode
        app.jinja_env.filters['b64decode'] = base64.b64decode

template_filters_manager = TemplateFiltersManager()

def b64encode(s):
    print(s)
    return base64.b64encode(str(s).encode()).decode("ascii")