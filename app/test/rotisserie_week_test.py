import sys
import pdb
from app.server import RotisserieWeek

def test():
    test = RotisserieWeek([])
    assert test.ordered_stats == []
