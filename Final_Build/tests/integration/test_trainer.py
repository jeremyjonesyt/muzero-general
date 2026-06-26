import pytest
import torch
from muzero.training.trainer import MuZeroTrainer

def test_train_step_updates_weights():
    trainer = MuZeroTrainer()
    initial_weights = trainer.representation.net.weight.clone()
    
    loss = trainer.train_step(None)
    
    # Check if weights changed
    assert not torch.equal(trainer.representation.net.weight, initial_weights)
    assert loss > 0
