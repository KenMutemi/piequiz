import django_tables2 as tables
from viridis.models import Test

class TestTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    class Meta:
        model = Test
        attrs = {"class": "table"}
        fields = ('selection','title', 'institution', 'marks', 'pub_date')
