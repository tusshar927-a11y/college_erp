import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {

  runApp(
    const CampusFlowApp(),
  );
}

class CampusFlowApp extends StatelessWidget {

  const CampusFlowApp({super.key});

  @override
  Widget build(BuildContext context) {

    return MaterialApp(

      debugShowCheckedModeBanner: false,

      title: "CampusFlow ERP",

      theme: ThemeData(

        useMaterial3: true,

        colorSchemeSeed: Colors.blue,

        scaffoldBackgroundColor:
            const Color(0xfff4f7fb),
      ),

      home: const LoginScreen(),
    );
  }
}