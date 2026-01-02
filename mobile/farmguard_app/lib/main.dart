import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const FarmGuardApp());
}

class FarmGuardApp extends StatelessWidget {
  const FarmGuardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FarmGuard',
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }  
}