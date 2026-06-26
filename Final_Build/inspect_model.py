import torch
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.representation import RepresentationNetwork
from muzero.model.prediction import PredictionNetwork

def inspect_model():
    print("--- Neural Architecture Inspection ---")
    # Initialize networks
    rep = RepresentationNetwork()
    dyn = DynamicsNetwork()
    pred = PredictionNetwork()
    
    print(f"Representation Network: {rep}")
    print(f"Dynamics Network: {dyn}")
    print(f"Prediction Network: {pred}")
    print("---------------------------------------")

if __name__ == '__main__':
    inspect_model()
