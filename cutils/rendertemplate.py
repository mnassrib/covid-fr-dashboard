from flask import Flask, render_template, request, redirect, url_for

class RenderPage(object):
    """
    docstring
    """
    def __init__(self, htmlfile, **kwargs):
        self.htmlfile = htmlfile
        self.entries = list(kwargs.keys())
        for k, v in kwargs.items():
            setattr(self, '{}'.format(k), v)

    def appview(self):
        for k in self.entries:
            locals()[k] = getattr(self, '{}'.format(k))
        return render_template(self.htmlfile, **locals())