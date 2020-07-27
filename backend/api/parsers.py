from rest_framework import renderers
from rest_framework.parsers import BaseParser


class PlainTextJsonParser(BaseParser):
    """
    JSON payload (set in Content-Type) but sent in plain text. Used to parse Stripe
    webhooks.
    """

    media_type = "application/json"

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


class PlainTextJSONRenderer(renderers.BaseRenderer):
    """
    JSON payload (set in Content-Type) but sent in plain text. Used to simulate Stripe
    webhooks on tests.
    """

    media_type = "application/json"
    format = "json-txt"

    def render(self, data, media_type=None, renderer_context=None):
        return data
