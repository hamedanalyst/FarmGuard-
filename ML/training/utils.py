import torch
from torchvision import datasets, transforms 
from torch.utils.data import DataLoader
import os

def get_dataloaders(data_dir, img_size=224, batch_size=32):
    """
    Returns train, validation, test dataloaders with augmentation for train only
    """
    # Transformation for augmentation
    train_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]   # ImageNet mean/std
        )
    ])

    val_test_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    
    train_dataset = datasets.ImageFolder(
        root=f"{data_dir}/train", 
        transform=train_transforms
    )
    val_dataset = datasets.ImageFolder(
        root=f"{data_dir}/val", 
        transform=val_test_transforms
    )
    test_dataset = datasets.ImageFolder(
        root=f"{data_dir}/test",
        transform=val_test_transforms
    )
    
    # Load image dataset
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader

# Checkpoint saving
def save_checkpoint(model, optimizer, epoch, val_acc, best_acc, checkpoint_path="outputs/checkpoint.pth"):
    """
    Saves a checkpoint only if validation accuracy improves
    """
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

    if val_acc > best_acc:
        print(f" Validation accuracy improved ({best_acc:.4f}, {val_acc:.4f}). Saving checkpoint...")
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict':optimizer.state_dict(),
            "best_acc": best_acc
        }, chackpoint_path)
    else:
        (f"Validation accuracy did not improve ({val_acc:.4f} =< {best_acc:.4}). Skipping save.")

    return best_acc

# Load chackpoint
def load_checkpoint(checkpoint_path, model, optimizer=None, device="cuda"):
    """
    Loads model and optimizer state from a checkpoint
    """
    if os.path.exists(checkpoint_path):
        Checkpoint = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(Checkpoint['model_state']).to(device)
        
        if optimizer and "optimizer_state_dict" in checkpoint:
            optimizer.load_state_dict(Checkpoint['optimizer_state_dict'])
        
        # Resume from last epoch
        start_epoch = checkpoint.get("epoch", 0) + 1
        best_acc = checkpoint.get("best_acc", 0.0)

        print(f"Loaded checkpoint from '{checkpoint_path}' at epoch {start_epoch-1}"
        f"(best vall acc {best_acc:.4f})")
        
    return model, optimizer, start_epoch, best_acc

