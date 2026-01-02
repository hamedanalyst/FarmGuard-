import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pytorch_mobile/model.dart';
import 'package:pytorch_mobile/pytorch_mobile.dart';

import '../utils/crop_config.dart';

class ModelService {
  late Model _model;
  late List<String> _labels;

  Future<void> loadModel(CropType crop) async {
    try {
      final assetModelPath = CropConfig.modelPaths[crop]!;
      final assetLabelPath = CropConfig.labelPaths[crop]!;

      // Copy model from assets → app directory
      final byteData = await rootBundle.load(assetModelPath);
      final Uint8List bytes = byteData.buffer.asUint8List();

      final dir = await getApplicationDocumentsDirectory();
      final file = File('${dir.path}/${assetModelPath.split('/').last}');
      await file.writeAsBytes(bytes, flush: true);

      final absPath = file.path;

      // This is the key call (assetPath, absPath)
      _model = await PyTorchMobile.loadModel(absPath);

      // Load labels
      final labelData = await rootBundle.loadString(assetLabelPath);
      final decoded = json.decode(labelData);

      if (decoded is List) {
        _labels = List<String>.from(decoded);
      } else if (decoded is Map && decoded['labels'] is List) {
        _labels = List<String>.from(decoded['labels']);
      } else {
        throw Exception('Invalid label format');
      }
    } catch (e) {
      throw Exception('Failed to load model or labels: $e');
    }
  }

  Future<String> predict(File image) async {
    try {
      final scores = await _model.getImagePredictionList(
        image,
        224,
        224,
        mean: [0, 0, 0],
        std: [1, 1, 1],
      );

      if (scores == null || scores.isEmpty) return 'Unknown';

      int maxIdx = 0;
      double maxVal = scores[0].toDouble();

      for (int i = 1; i < scores.length; i++) {
        if (scores[i] > maxVal) {
          maxVal = scores[i].toDouble();
          maxIdx = i;
        }
      }

      return (maxIdx < _labels.length) ? _labels[maxIdx] : 'Unknown';
    } catch (_) {
      return 'Unknown';
    }
  }
}
