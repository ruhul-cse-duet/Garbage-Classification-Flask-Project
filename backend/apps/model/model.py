import torch.nn as nn
import torchvision.models as models

class GarbageModel(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.model = models.resnet50(weights=None)

        for param in self.model.parameters():
            param.requires_grad = False

        for param in self.model.layer4.parameters():
            param.requires_grad = True

        self.model.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(self.model.fc.in_features, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.model(x)
