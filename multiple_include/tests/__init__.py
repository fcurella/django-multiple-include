from __future__ import unicode_literals
from django.template import Context, Template, TemplateDoesNotExist
from django.test import TestCase
from .models import Story


class MultipleIncludeTest(TestCase):
    def setUp(self):
        self.story1 = Story.objects.create(title='story1', category_slug='category1')
        self.story2 = Story.objects.create(title='story2', category_slug='category2')
        self.story3 = Story.objects.create(title='story3', category_slug='category3')

    def render(self, template_content, context=None):
        if context is None:
            context = {}
        t = Template(template_content)
        c = Context(context)

        return t.render(c)

    def test_simple_include(self):
        template_content = '{% load multiple_include %}{% multiple_include "story_category1.html" %}'

        rendered = self.render(template_content)
        self.assertEqual(rendered, 'story_category1.html')

    def test_constant_include(self):
        template_content = '{% load multiple_include %}{% multiple_include "story_category1.html" "story_category2.html" %}'

        rendered = self.render(template_content)
        self.assertEqual(rendered, 'story_category1.html')

        template_content = '{% load multiple_include %}{% multiple_include "story_category2.html" "story_category1.html" %}'

        rendered = self.render(template_content)
        self.assertEqual(rendered, 'story_category2.html')

    def test_fallback_include(self):
        template_content = '{% load multiple_include %}{% multiple_include "story_category3.html" "story_default.html" %}'

        rendered = self.render(template_content)
        self.assertEqual(rendered, 'story_default.html')

        template_content = '{% load multiple_include %}{% multiple_include "story_category3.html" %}'

        # should fail
        self.assertRaises(TemplateDoesNotExist, self.render, template_content)

    def test_include(self):
        template_content = '{{ "story_"|add:object.category_slug|add:".html" }}'
        rendered = self.render(template_content, {'object': self.story1})
        self.assertEqual(rendered, 'story_category1.html')

        template_content = '{% load multiple_include %}{% with "story_"|add:object.category_slug|add:".html" as template_name %}{% multiple_include template_name "story_default.html" %}{% endwith %}'
        rendered = self.render(template_content, {'object': self.story1})
        self.assertEqual(rendered, 'story_category1.html')

        template_content = '{% load multiple_include %}{% multiple_include "story_"|add:object.category_slug|add:".html" "story_default.html" %}'
        rendered = self.render(template_content, {'object': self.story1})
        self.assertEqual(rendered, 'story_category1.html')

        rendered = self.render(template_content, {'object': self.story3})
        self.assertEqual(rendered, 'story_default.html')

    def test_with(self):
        template_content = '{% load multiple_include %}{% multiple_include "story_title.html" with story=object %}'
        rendered = self.render(template_content, {'object': self.story1})
        self.assertEqual(rendered, 'story1')

    def test_only(self):
        template_content = '{% load multiple_include %}{% multiple_include "story_title.html" %}'
        rendered = self.render(template_content, {'story': self.story1})
        self.assertEqual(rendered, 'story1')

        template_content = '{% load multiple_include %}{% multiple_include "story_title.html" only %}'

        rendered = self.render(template_content, {'story': self.story1})
        self.assertEqual(rendered, '')
