import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'student_dashboard.dart';
import 'faculty_dashboard.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {

  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  bool loading = false;

  Future<void> login() async {

    setState(() {
      loading = true;
    });

    try {

      final result = await ApiService.login(
        emailController.text.trim(),
        passwordController.text,
      );

      if (!mounted) return;

      if (result["success"] == true) {

        final user = result["user"];

        if (user["role"] == "student") {

          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => StudentDashboard(
                user: user,
              ),
            ),
          );

        } else if (user["role"] == "faculty") {

          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => FacultyDashboard(
              user: user,
              ),
            ),
          );

        } else {

          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text(
                "Admin should use the web portal.",
              ),
            ),
          );
        }

      } else {

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              result["message"] ?? "Login failed",
            ),
          ),
        );
      }

    } catch (e) {

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            "Cannot connect to server: $e",
          ),
        ),
      );

    } finally {

      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }


  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: const Color(0xfff4f7fb),

      body: Center(

        child: SingleChildScrollView(

          padding: const EdgeInsets.all(24),

          child: Card(

            elevation: 5,

            child: Padding(

              padding: const EdgeInsets.all(28),

              child: Column(

                mainAxisSize: MainAxisSize.min,

                children: [

                  const Icon(
                    Icons.school,
                    size: 65,
                    color: Colors.blue,
                  ),

                  const SizedBox(height: 15),

                  const Text(
                    "CampusFlow",
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const Text(
                    "College ERP",
                    style: TextStyle(
                      color: Colors.grey,
                    ),
                  ),

                  const SizedBox(height: 35),

                  TextField(
                    controller: emailController,
                    keyboardType: TextInputType.emailAddress,
                    decoration: const InputDecoration(
                      labelText: "Email",
                      prefixIcon: Icon(Icons.email),
                      border: OutlineInputBorder(),
                    ),
                  ),

                  const SizedBox(height: 18),

                  TextField(
                    controller: passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: "Password",
                      prefixIcon: Icon(Icons.lock),
                      border: OutlineInputBorder(),
                    ),
                  ),

                  const SizedBox(height: 25),

                  SizedBox(
                    width: double.infinity,
                    height: 52,

                    child: ElevatedButton(

                      onPressed:
                          loading ? null : login,

                      child: loading
                          ? const CircularProgressIndicator()
                          : const Text(
                              "LOGIN",
                              style: TextStyle(
                                fontSize: 16,
                              ),
                            ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}