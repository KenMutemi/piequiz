#!/home/re/dev/python/piequiz/venv/bin/python
import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piequiz.settings")
from viridis.models import Test

def rank_all():
    for test in Test.with_votes.all():
        test.set_rank()

def show_all():
    print "\n".join("%10s %0.sf" % (t.title, t.rank_score,
        ) for t in Test.with_votes.all())
    print "----\n\n\n"

if __name__=="__main__":
    while 1:
        print "----"
        rank_all()
        show_all()
        time.sleep(5)
