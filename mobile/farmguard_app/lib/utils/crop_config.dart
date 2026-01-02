enum CropType { cassava, maize, plant}

class CropConfig {
  static const modelPaths = {
    CropType.cassava: 'assets/models/cassava.pt',
    CropType.maize: 'assets/models/maize.pt',
    CropType.plant: 'assets/models/plant.pt',
  };

  static const labelPaths = {
    CropType.cassava: 'assets/labels/cassava.json',
    CropType.maize: 'assets/labels/maize.json', 
    CropType.plant: 'assets/labels/plantdisease.json',
  };
}
