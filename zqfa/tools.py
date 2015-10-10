from PIL import Image
from flask import url_for, redirect, request
from wtforms.fields import HiddenField
from urlparse import urlparse, urljoin

import mistune
import bleach

def static(filename, external=False):
    """A helper that will be used as a filter to avoid complicated
    url_for/static clauses. This was strings can just be filtered in
    the format of `'filename'|static`.

    :param string: the filename of a static file."""
    return url_for('static', filename=filename, _external=external)


def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back():
    target = get_redirect_target()
    return redirect(target or url_for('page.home'))


class MarkdownRenderer(mistune.Renderer):
    pass

class UserMarkdownRenderer(mistune.Renderer):
    pass

renderer = MarkdownRenderer(hard_wrap=True)
markdown_admin = mistune.Markdown(renderer=renderer).render


def sanitized_markdown(markdown_string):
    allowed_tags = bleach.ALLOWED_TAGS + ['table','tr','td','th','h1','h2','h3','h4','h5','h6', 'del','ins','small','hr','sub','sup','s','u']
    markdown_string = bleach.clean(markdown_string, strip=True, tags=allowed_tags)
    html_string = markdown_admin(markdown_string)
    return html_string

markdown_user = sanitized_markdown




def setUp(app):
    app.add_template_filter(static)
    app.add_template_global(
        is_hidden_field_filter,
        name='bootstrap_is_hidden_field')