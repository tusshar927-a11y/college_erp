import 'package:flutter/material.dart';
import '../services/api_service.dart';

class FacultyAttendance extends StatefulWidget {

  const FacultyAttendance({super.key});

  @override
  State<FacultyAttendance> createState() =>
      _FacultyAttendanceState();
}

class _FacultyAttendanceState
    extends State<FacultyAttendance> {

  List students = [];

  @override
  void initState() {

    super.initState();

    loadStudents();
  }

  Future<void> loadStudents() async {

    final result =
        await ApiService.getStudents();

    if (result["success"] == true) {

      setState(() {

        students =
            result["students"];
      });
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text(
          "Mark Attendance",
        ),
      ),

      body: ListView.builder(

        padding: const EdgeInsets.all(15),

        itemCount: students.length,

        itemBuilder: (context, index) {

          final student =
              students[index];

          return Card(

            child: ListTile(

              leading: CircleAvatar(
                child: Text(
                  student["name"][0],
                ),
              ),

              title: Text(
                student["name"],
              ),

              subtitle: Text(
                student["email"],
              ),

              trailing: DropdownButton<String>(

                value: "Present",

                items: const [

                  DropdownMenuItem(
                    value: "Present",
                    child: Text("Present"),
                  ),

                  DropdownMenuItem(
                    value: "Absent",
                    child: Text("Absent"),
                  ),
                ],

                onChanged: (value) async {

                  if (value == null) return;

                  final today =
                      DateTime.now()
                          .toIso8601String()
                          .substring(0, 10);

                  await ApiService.markAttendance(
                    student["id"],
                    "Java",
                    today,
                    value,
                  );

                  if (!mounted) return;

                  ScaffoldMessenger.of(
                    context,
                  ).showSnackBar(
                    SnackBar(
                      content: Text(
                        "${student["name"]}: $value",
                      ),
                    ),
                  );
                },
              ),
            ),
          );
        },
      ),
    );
  }
}