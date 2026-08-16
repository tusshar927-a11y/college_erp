import 'package:flutter/material.dart';

class MessagesScreen extends StatelessWidget {

  final int studentId;

  const MessagesScreen({
    super.key,
    required this.studentId,
  });

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Messages"),
      ),

      body: const Center(
        child: Text(
          "Faculty messages will appear here.",
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}