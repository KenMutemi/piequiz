import django_tables2 as tables
from viridis.models import Test

class TestTable(tables.Table):
    class Meta:
        model = Test
        attrs = {"class": "table"}
        fields = ('title', 'institution', 'marks', 'pub_date')
