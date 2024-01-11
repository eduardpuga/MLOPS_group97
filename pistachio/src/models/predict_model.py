import torch
import numpy as np

def create_example_images(input_file, output_file, num_images=10):
    # Load the processed data
    processed_data = torch.load(input_file)
    data = processed_data['data']

    # Select a subset of images
    if num_images > len(data):
        print("Requested number of images is more than available. Using available images.")
        num_images = len(data)
    example_images = data[:num_images]

    # Convert to numpy and save
    example_images_np = example_images.numpy()
    np.save(output_file, example_images_np)
    print(f"Saved {num_images} images to {output_file}")



import click
import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from pistachio.models.model import MyAwesomeModel  # Import your model class here

def load_data_from_numpy(file_path):
    """ Load data from a numpy file and preprocess for MyAwesomeModel. """
    data = np.load(file_path)
    data_tensor = torch.tensor(data).float()  # Convert to tensor and ensure float type

    # Reshape the data to match the input size of the model
    data_tensor = data_tensor.view(-1, 1080000)  # Reshape to [batch_size, 1080000]

    # If additional preprocessing is required (like normalization), apply it here

    # Create a dataset and loader
    dataset = TensorDataset(data_tensor, torch.zeros(len(data_tensor)))  # Dummy labels
    loader = DataLoader(dataset, batch_size=1, shuffle=False)
    return loader

@click.command()
@click.argument('model_path', type=click.Path(exists=True))
@click.argument('data_path', type=click.Path(exists=True))
def predict(model_path, data_path):
    """ Load a model and make predictions on provided data. """
    # Load the model
    model = MyAwesomeModel()  # Adjust according to your model
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # Load the data
    data_loader = load_data_from_numpy(data_path)

    # Make predictions
    predictions = []
    with torch.no_grad():
        for inputs, _ in data_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            predictions.append(predicted.item())

    print("Predictions:", predictions)

if __name__ == "__main__":
    create_example_images('data/processed/processed_data.pt', 'data/processed/example_images.npy')
    predict()