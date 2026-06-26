import logging
import torch.distributed as dist
import time

logging.basicConfig(level=logging.INFO, filename='training.log', filemode='a')
logger = logging.getLogger("DistributedLossLogger")

def log_loss(loss_val):
    try:
        rank = dist.get_rank()
    except:
        rank = 0
    logger.info(f"[Rank {rank}] Timestamp: {time.time()} | Loss: {loss_val:.6f}")
