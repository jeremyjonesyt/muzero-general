import torch
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork
from muzero.training.inference_loop import MuZeroModelWrapper

model = MuZeroModelWrapper(RepresentationNetwork(), DynamicsNetwork(), PredictionNetwork())
dummy_hidden = torch.randn(1, 64)
output = model.prediction(dummy_hidden)
print(f"Prediction output type: {type(output)}")
print(f"Prediction output value: {output}")
