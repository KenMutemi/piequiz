import datetime
from haystack import indexes
from viridis.models import Test

class TestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    content_auto = indexes.EdgeNgramField(model_attr='title') # For autocomplete
   
    def get_model(self):
        return Test

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Test.objects.filter(pub_date__lte=datetime.datetime.now())
