import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {

  // IMPORTANT:
  // Change this after deploying Flask online.
  static const String baseUrl =
      "http://10.0.2.2:5000/api";

  // =========================
  // LOGIN
  // =========================

  static Future<Map<String, dynamic>> login(
      String email,
      String password) async {

    final response = await http.post(
      Uri.parse("$baseUrl/login"),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );

    return jsonDecode(response.body);
  }


  // =========================
  // STUDENT ATTENDANCE
  // =========================

  static Future<Map<String, dynamic>> getAttendance(
      int studentId) async {

    final response = await http.get(
      Uri.parse(
        "$baseUrl/student/attendance/$studentId",
      ),
    );

    return jsonDecode(response.body);
  }


  // =========================
  // ASSIGNMENTS
  // =========================

  static Future<Map<String, dynamic>> getAssignments() async {

    final response = await http.get(
      Uri.parse(
        "$baseUrl/student/assignments",
      ),
    );

    return jsonDecode(response.body);
  }


  // =========================
  // MESSAGES
  // =========================

  static Future<Map<String, dynamic>> getMessages(
      int studentId) async {

    final response = await http.get(
      Uri.parse(
        "$baseUrl/student/messages/$studentId",
      ),
    );

    return jsonDecode(response.body);
  }


  // =========================
  // FACULTY STUDENTS
  // =========================

  static Future<Map<String, dynamic>> getStudents() async {

    final response = await http.get(
      Uri.parse(
        "$baseUrl/faculty/students",
      ),
    );

    return jsonDecode(response.body);
  }


  // =========================
  // MARK ATTENDANCE
  // =========================

  static Future<Map<String, dynamic>> markAttendance(
      int studentId,
      String subject,
      String date,
      String status) async {

    final response = await http.post(
      Uri.parse(
        "$baseUrl/faculty/attendance",
      ),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "student_id": studentId,
        "subject": subject,
        "date": date,
        "status": status,
      }),
    );

    return jsonDecode(response.body);
  }
}