import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../utils/crop_config.dart';
import '../services/model_services.dart';
import 'result_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  CropType? selectedCrop;
  final picker = ImagePicker();
  final modelService = ModelService();

  Future<void> pickImage() async {
    if (selectedCrop == null) return;

    final image = await picker.pickImage(source: ImageSource.camera);
    if (image == null) return;

    try {
      // ignore: avoid_print
      print('HomeScreen.pickImage: selectedCrop=$selectedCrop, about to loadModel');
      await modelService.loadModel(selectedCrop!);
      // ignore: avoid_print
      print('HomeScreen.pickImage: loadModel returned, calling predict');
      final prediction = await modelService.predict(File(image.path));
      // ignore: avoid_print
      print('HomeScreen.pickImage: prediction result: $prediction');

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultScreen(disease: prediction),
        ),
      );
    } catch (e, st) {
      // Log and surface the error so it's visible during release testing
      try {
        // ignore: avoid_print
        print('HomeScreen.pickImage error: $e');
        // ignore: avoid_print
        print(st);
      } catch (_) {}
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Prediction failed: ${e.toString()}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('FarmGuard')),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          DropdownButton<CropType>(
            hint: const Text("Select Crop"),
            value: selectedCrop,
            onChanged: (value) => setState(() => selectedCrop = value),
            items: const [
              DropdownMenuItem<CropType>(
                value: CropType.cassava,
                child: Text("Cassava")
              ),
              DropdownMenuItem<CropType>(
                value: CropType.maize,
                child: Text("Maize")
              ),
              DropdownMenuItem<CropType>(
                value: CropType.plant,
                child: Text("Potato / Pepper / Tomato")
              ),
            ],
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: pickImage,
            child: const Text("Capture Leaf Image")
          ),
        ],
      ),
    );
  }
}