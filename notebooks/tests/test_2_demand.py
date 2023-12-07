
import pytest
import pickle

with open('demandVars.pkl', 'rb') as f:
    zoneCheck_ref, zoneCheck, yearCheck_ref, yearCheck, demandTemporal = pickle.load(f)
    
def test_zoneCheck():
    assert zoneCheck_ref == zoneCheck
    
def test_yearCheck():
    assert yearCheck_ref == yearCheck

def test_plotsCheck():
    assert demandTemporal == 1
