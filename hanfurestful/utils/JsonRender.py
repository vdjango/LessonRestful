from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class Utf8JSONRenderer(JSONRenderer):
    charset = 'utf-8'
