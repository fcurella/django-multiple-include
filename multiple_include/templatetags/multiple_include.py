from django.conf import settings
from django.template.base import Library, token_kwargs
from django.template.loader import select_template
from django.template.loader_tags import IncludeNode, TemplateSyntaxError

register = Library()


class MultipleIncludeNode(IncludeNode):
    def __init__(self, template_names, *args, **kwargs):
        super(IncludeNode, self).__init__(*args, **kwargs)
        self.template_names = template_names

    def render(self, context):
        try:
            template_names = [template_name.resolve(context) for template_name in self.template_names]
            template = select_template(template_names)
            return self.render_template(template, context)
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''


@register.tag('multiple_include')
def do_include(parser, token):
    """
    Loads a template and renders it with the current context. You can pass
    additional context using keyword arguments.

    Example::

        {% include "foo/some_include" "foo/some_other_include" %}
        {% include "foo/some_include" "foo/some_other_include" with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::

        {% include "foo/some_include" "foo/some_other_include" only %}
        {% include "foo/some_include" "foo/some_other_include" with bar="1" only %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("%r tag takes at least one argument: the name of the template to be included." % bits[0])
    options = {}

    remaining_bits = bits[1:]
    paths = []
    stop_markers = ('only', 'with')
    while remaining_bits and remaining_bits[0] not in stop_markers:
        paths.append(remaining_bits.pop(0))

    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    template_names = [parser.compile_filter(path) for path in paths]
    return MultipleIncludeNode(template_names, extra_context=namemap,
                       isolated_context=isolated_context)
