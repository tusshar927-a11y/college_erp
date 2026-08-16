import 'package:flutter/material.dart';
import 'attendance_screen.dart';
import 'assignments_screen.dart';
import 'messages_screen.dart';

class StudentDashboard extends StatelessWidget {

  final Map<String, dynamic> user;

  const StudentDashboard({
    super.key,
    required this.user,
  });

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("CampusFlow"),
      ),

      body: SingleChildScrollView(

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

            const SizedBox(height: 5),

            const Text(
              "Student Portal",
              style: TextStyle(
                color: Colors.grey,
              ),
            ),

            const SizedBox(height: 25),

            GridView.count(

              shrinkWrap: true,

              physics:
                  const NeverScrollableScrollPhysics(),

              crossAxisCount: 2,

              crossAxisSpacing: 15,

              mainAxisSpacing: 15,

              children: [

                _card(
                  context,
                  Icons.person,
                  "Attendance",
                  () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            AttendanceScreen(
                          studentId: user["id"],
                        ),
                      ),
                    );
                  },
                ),

                _card(
                  context,
                  Icons.assignment,
                  "Assignments",
                  () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            const AssignmentsScreen(),
                      ),
                    );
                  },
                ),

                _card(
                  context,
                  Icons.message,
                  "Messages",
                  () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            MessagesScreen(
                          studentId: user["id"],
                        ),
                      ),
                    );
                  },
                ),

              ],
            ),
          ],
        ),
      ),
    );
  }


  Widget _card(
    BuildContext context,
    IconData icon,
    String title,
    VoidCallback action,
  ) {

    return InkWell(

      onTap: action,

      child: Card(

        elevation: 3,

        child: Column(

          mainAxisAlignment:
              MainAxisAlignment.center,

          children: [

            Icon(
              icon,
              size: 45,
              color: Colors.blue,
            ),

            const SizedBox(height: 12),

            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 17,
              ),
            ),
          ],
        ),
      ),
    );
  }
}