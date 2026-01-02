import 'package:flutter/material.dart';
import '../data/treatments.dart';

class ResultScreen extends StatelessWidget {
  final String disease;
  const ResultScreen({required this.disease});

  @override
  Widget build(BuildContext context) {
    String normalize(String label) {
      final s = label.toLowerCase().replaceAll('___', '_').replaceAll(RegExp('[^a-z0-9_]'), '');
      // sometimes labels are like 'cassava_healthy' or just 'healthy' in treatments
      if (treatments.containsKey(s)) return s;
      final parts = s.split('_');
      if (parts.length > 1) {
        // try without the crop prefix (e.g. 'cassava_healthy' -> 'healthy')
        final withoutPrefix = parts.sublist(1).join('_');
        if (treatments.containsKey(withoutPrefix)) return withoutPrefix;
      }
      return s;
    }

    final key = normalize(disease);
    final treatment = treatments[key] ?? "No treatment info available.";

    return Scaffold(
      appBar: AppBar(title: const Text("Diagnosis Result")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text("Disease: $disease",
                style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 20),
            Text("Recommended Treatment:",
                style: const TextStyle(fontWeight: FontWeight.bold)),
            Text(treatment),
          ],
        ),
      ),
    );
  }
}