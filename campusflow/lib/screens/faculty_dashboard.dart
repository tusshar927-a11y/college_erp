import 'package:flutter/material.dart';
import 'faculty_attendance.dart';

class FacultyDashboard extends StatelessWidget {

  final Map<String, dynamic> user;

  const FacultyDashboard({
    super.key,
    required this.user,
  });

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("CampusFlow"),
      ),

      body: Padding(

        padding: const EdgeInsets.all(20),

        child: Column(

          crossAxisAlignment:
              CrossAxisAlignment.start,

          children: [

            Text(
              "Hello, ${user["name"]} 👋",
              style: const TextStyle(
                fontSize: 27,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            const Text(
              "Faculty Portal",
            ),

            const SizedBox(height: 30),

            Card(

              child: ListTile(

                leading: const Icon(
                  Icons.fact_check,
                  color: Colors.blue,
                ),

                title: const Text(
                  "Attendance Management",
                ),

                subtitle: const Text(
                  "Mark student attendance",
                ),

                trailing:
                    const Icon(Icons.arrow_forward),

                onTap: () {

                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          const FacultyAttendance(),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}