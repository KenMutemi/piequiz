import django_tables2 as tables
from viridis.models import Test

class TestTable(tables.Table):
    pub_date = tables.DateColumn(short=True)
    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":{"onclick": "toggle(this)", "title": "select all"}}, orderable=False)
    title = tables.TemplateColumn('<a href="{{record.get_absolute_url}}">{{record.title}}</a>')
    class Meta:
        model = Test
        attrs = {"class": "table table-striped"}
        fields = ('selection','title', 'institution', 'marks', 'pub_date')
