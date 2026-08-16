import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AttendanceScreen extends StatefulWidget {

  final int studentId;

  const AttendanceScreen({
    super.key,
    required this.studentId,
  });

  @override
  State<AttendanceScreen> createState() =>
      _AttendanceScreenState();
}

class _AttendanceScreenState
    extends State<AttendanceScreen> {

  late Future<Map<String, dynamic>> attendance;

  @override
  void initState() {
    super.initState();

    attendance =
        ApiService.getAttendance(widget.studentId);
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text(
          "My Attendance",
        ),
      ),

      body: FutureBuilder<Map<String, dynamic>>(

        future: attendance,

        builder: (context, snapshot) {

          if (snapshot.connectionState ==
              ConnectionState.waiting) {

            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {

            return Center(
              child: Text(
                "Error: ${snapshot.error}",
              ),
            );
          }

          final data = snapshot.data!;

          final subjects =
              data["subjects"] as List;

          return ListView(

            padding: const EdgeInsets.all(20),

            children: [

              Card(

                child: Padding(

                  padding:
                      const EdgeInsets.all(20),

                  child: Column(

                    children: [

                      const Text(
                        "Overall Attendance",
                        style: TextStyle(
                          fontSize: 18,
                        ),
                      ),

                      const SizedBox(height: 10),

                      Text(
                        "${data["overall_percentage"]}%",
                        style: const TextStyle(
                          fontSize: 38,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                      ),

                      Text(
                        "${data["total_present"]} / ${data["total_classes"]} classes",
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 20),

              const Text(
                "Subject-wise Attendance",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 10),

              ...subjects.map(
                (subject) {

                  final percentage =
                      subject["percentage"];

                  return Card(

                    margin:
                        const EdgeInsets.only(
                      bottom: 12,
                    ),

                    child: Padding(

                      padding:
                          const EdgeInsets.all(16),

                      child: Column(

                        crossAxisAlignment:
                            CrossAxisAlignment.start,

                        children: [

                          Text(
                            subject["subject"],
                            style:
                                const TextStyle(
                              fontSize: 18,
                              fontWeight:
                                  FontWeight.bold,
                            ),
                          ),

                          const SizedBox(height: 10),

                          LinearProgressIndicator(
                            value:
                                percentage / 100,
                          ),

                          const SizedBox(height: 8),

                          Text(
                            "$percentage%  •  "
                            "${subject["present"]} Present  •  "
                            "${subject["absent"]} Absent",
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ],
          );
        },
      ),
    );
  }
}