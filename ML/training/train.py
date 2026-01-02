import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from scripts.models.models import get_efficientnet_b0
from scripts.utils.utils import get_dataloaders, save_checkpoint, load_checkpoint
import os

def train_model(
    data_dir,
    num_classes=15,           
    epochs=10,
    lr=0.001,
    batch_size=32,
    device="cuda",
    patience=5,
    checkpoint_dir="outputs/checkpoints",
    freeze_backbone=True,
    unfreeze_epoch=2           # epoch to unfreeze backbone
):

    os.makedirs(checkpoint_dir, exist_ok=True)

    # Load data
    train_loader, val_loader, dataset = get_dataloaders(data_dir, batch_size=batch_size)

    # Initialize model
    model = get_efficientnet_b0(num_classes=num_classes).to(device)

    # Freeze backbone if specified
    if freeze_backbone:
        for param in model.features.parameters():
            param.requires_grad = False

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)

    # Load checkpoint if exists
    checkpoint_path = os.path.join(checkpoint_dir, "checkpoint.pth")
    start_epoch, best_acc = 0, 0.0
    if os.path.exists(checkpoint_path):
        print(f"Resuming training from checkpoint: {checkpoint_path}")
        model, optimizer, start_epoch, best_acc = load_checkpoint(checkpoint_path, model, optimizer, device)
    else:
        print("Starting training from scratch")

    patience_counter = 0

    # Training loop
    for epoch in range(start_epoch, epochs):
        model.train()
        running_loss, correct, total = 0.0, 0, 0

        for images, labels in tqdm(train_loader, desc=f"Training Epoch {epoch+1}/{epochs}"):
            try:
                images, labels = images.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
            except Exception as e:
                print(f"Skipping batch due to error: {e}")
                continue

        train_loss = running_loss / len(train_loader)
        train_acc = 100. * correct / total

        # Validation
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                try:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item()
                    _, predicted = outputs.max(1)
                    val_total += labels.size(0)
                    val_correct += predicted.eq(labels).sum().item()
                except Exception as e:
                    print(f"Skipping validation batch due to error: {e}")
                    continue

        val_loss /= len(val_loader)
        val_acc = 100. * val_correct / val_total

        print(f"Epoch {epoch+1}/{epochs} | "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

        # Save checkpoint only if validation accuracy improves
        if val_acc > best_acc:
            best_acc = val_acc
            save_checkpoint(model, optimizer, epoch, val_acc, best_acc, checkpoint_path)
            print(f"Checkpoint saved at epoch {epoch+1} with Val Acc: {val_acc:.2f}%")
            patience_counter = 0
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= patience:
            print(f"Early stopping triggered at epoch {epoch+1}")
            break

        # Unfreeze backbone for fine-tuning
        if freeze_backbone and epoch+1 == unfreeze_epoch:
            print("Unfreezing backbone for fine-tuning")
            for param in model.features.parameters():
                param.requires_grad = True
            optimizer = optim.Adam(model.parameters(), lr=lr * 0.1)  # lower LR for fine-tuning

    # Save final model
    final_model_path = os.path.join(checkpoint_dir, "final_model.pth")
    torch.save(model.state_dict(), final_model_path)
    print(f"Training complete. Final model saved at {final_model_path}")

    return model