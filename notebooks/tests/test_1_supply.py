
import pytest
import pickle
import os

with open('supplyVars.pkl', 'rb') as f:
    stateName, stateName_ref, allGhiHeatmap, stateGhiHeatmap, oneCoordGhi, stateGHIInOneYear, stateMonthHourHeatmap, stateVariance, stateGHIByMonth, inputCoord, nearestCoord = pickle.load(f)
    
def test_stateNameCheck():
    assert stateName == stateName_ref

def test_coordinateCheck():
    assert abs(inputCoord[0] - nearestCoord[0]) <= 1
    assert abs(inputCoord[1] - nearestCoord[1]) <= 1
    
def test_plotsCheck():
    assert allGhiHeatmap == 1
    assert stateGhiHeatmap == 1
    assert oneCoordGhi == 1
    assert stateGHIInOneYear == 1
    assert stateMonthHourHeatmap == 1
    assert stateVariance == 1
    assert stateGHIByMonth == 1
