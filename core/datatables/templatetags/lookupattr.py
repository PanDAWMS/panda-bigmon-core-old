# Django
from django import template

# Django-DataTables
from core.datatables.utils import lookupattr

register = template.Library()
register.filter('lookupattr', lookupattr)
