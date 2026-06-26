from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork
from muzero.training.inference_loop import MuZeroModelWrapper

model = MuZeroModelWrapper(RepresentationNetwork(), DynamicsNetwork(), PredictionNetwork())
print("Available attributes in model:")
for attr in dir(model):
    if not attr.startswith('__'):
        print(f"- {attr}")
