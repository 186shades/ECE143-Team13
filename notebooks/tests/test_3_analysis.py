
import pytest
import pickle

with open('analysisVars.pkl', 'rb') as f:
    analysisYear_ref, analysisYear, hours24_1, hours24_2, hours24_3, used_curtailed, grid, storageCapacity = pickle.load(f)
    
def test_analysisYearCheck():
    assert analysisYear_ref == analysisYear

def test_plotsCheck():
    assert hours24_1 == 1
    assert hours24_2 == 1
    assert hours24_3 == 1
    assert used_curtailed == 1
    assert grid == 1
    assert storageCapacity == 1
