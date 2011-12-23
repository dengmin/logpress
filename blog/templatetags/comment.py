from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.template.context import Context
from blog.models import Comment
from blog.forms import CommentForm

from blog.models import OptionSet
from django import template
from django.template import Library, Node,resolve_variable
from threading import Thread
from django.conf import settings
import hashlib,urllib,os,time

COMMENT_MAX_DEPTH = 5

register = template.Library()

class BaseCommentNode(template.Node):
   
    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            return cls(
                object_expr = parser.compile_filter(tokens[2]),
                as_varname = tokens[4],
            )
        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])


    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, comment=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("Comment nodes must be given either a literal object or a ctype and object pk.")
        self.comment_model = Comment
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr
        self.comment = comment

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''

    def get_query_set(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_model.objects.filter(
            content_type = ctype, object_pk = smart_unicode(object_pk),is_public = True,
        )
        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def get_context_value_from_queryset(self, context, qs):
        raise NotImplementedError

class CommentFormNode(BaseCommentNode):
    def get_form(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        initial_date = context['comment_meta']

        if object_pk:
            return CommentForm(ctype.get_object_for_this_type(pk=object_pk), initial = initial_date)
        else:
            return None

    def render(self, context):
        context[self.as_varname] = self.get_form(context)
        return ''

@register.tag
def get_comment_form(parser, token):
    return CommentFormNode.handle_token(parser, token)


class gravatorNode(Node):
    def __init__(self,email):
        self.email = email
    
    def _fetchGravatarImage(self,email_digest):
        imgurl = "http://www.gravatar.com/avatar/"
        imgurl +=email_digest+"?"+ urllib.urlencode({'d':'default', 's':str(50),'r':'G'})
        return imgurl
    
    def render(self,context):
        email = resolve_variable(self.email,context)
        return self._fetchGravatarImage(hashlib.md5(email).hexdigest())

@register.tag
def gravator(parser,token):
    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError("useage 'gravator email '")
    return gravatorNode(tokens[1])