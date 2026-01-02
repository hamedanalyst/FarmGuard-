import torch
import torch.nn as nn
from torchvision import models
from torch.utils.mobile_optimizer import optimize_for_mobile
import argparse
from pathlib import Path

# Model builder
def build_efficientnet_b0(num_classes: int) -> nn.Module:
    model = models.efficientnet_b0(pretrained=False)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


# Safe loader for both state_dict and module
def load_model_auto(path: str, device: torch.device) -> nn.Module:
    loaded = torch.load(path, map_location=device)

    # Case 1: already a full nn.Module
    if isinstance(loaded, nn.Module):
        loaded.to(device)
        loaded.eval()
        return loaded

    # Case 2: state_dict or wrapped dict
    if isinstance(loaded, dict):
        if "model_state_dict" in loaded:
            state_dict = loaded["model_state_dict"]
        elif "state_dict" in loaded:
            state_dict = loaded["state_dict"]
        else:
            state_dict = loaded

        # Find classifier weight to infer num_classes
        classifier_key = None
        for k, v in state_dict.items():
            if isinstance(v, torch.Tensor) and v.ndim == 2:
                classifier_key = k
                break

        if classifier_key is None:
            raise RuntimeError("Could not infer classifier layer from state_dict")

        num_classes = state_dict[classifier_key].shape[0]

        model = build_efficientnet_b0(num_classes)
        model.load_state_dict(state_dict, strict=False)
        model.to(device)
        model.eval()
        return model

    raise RuntimeError("Unsupported model format")



# Export logic
def export_mobile_model(
    input_model_path: str,
    output_mobile_path: str,
    device: torch.device
):
    print(f"\nProcessing model: {input_model_path}")

    model = load_model_auto(input_model_path, device)

    # Script (NOT trace — safer)
    scripted = torch.jit.script(model)

    # Optimize for mobile
    optimized = optimize_for_mobile(scripted)

    # Save
    output_mobile_path = Path(output_mobile_path)
    output_mobile_path.parent.mkdir(parents=True, exist_ok=True)
    optimized.save(str(output_mobile_path))

    print(f"Saved mobile model to: {output_mobile_path}")



# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export single EfficientNet model to TorchScript Mobile")

    parser.add_argument("--input", required=True, help="Path to input .pt or .pth model")
    parser.add_argument("--output", required=True, help="Path to output mobile .pt file")

    args = parser.parse_args()

    DEVICE = torch.device("cpu")

    export_mobile_model(
        input_model_path=args.input,
        output_mobile_path=args.output,
        device=DEVICE
    )
