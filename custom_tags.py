from django import template
from ..models import get_all_logged_in_users, get_all_users, get_all_offline_users
register = template.Library()

@register.inclusion_tag('accounts/logged_in_user_list.html')
def render_logged_in_user_list():
    return { 'users': get_all_logged_in_users(),'all_users': get_all_users(), 'all_users2': get_all_offline_users()}
