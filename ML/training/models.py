import torch
import torch.nn as nn
from torchvision import models

def get_efficientnet_b0(num_classes, pretrained=True):
    """
    Load EfficientNet-B0 model and modify the classifier for our dataset
    """
    model = models.efficientnet_b0(pretrained=pretrained)
    in_features = model.classifier[1].in_features   
    model.classifier[1] = nn.Linear(in_features, num_classes)  
    
    return model