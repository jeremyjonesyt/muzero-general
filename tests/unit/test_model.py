import torch
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork

def test_model_initialization():
    rep = RepresentationNetwork()
    dyn = DynamicsNetwork()
    pred = PredictionNetwork()
    
    assert isinstance(rep, torch.nn.Module)
    assert isinstance(dyn, torch.nn.Module)
    assert isinstance(pred, torch.nn.Module)
