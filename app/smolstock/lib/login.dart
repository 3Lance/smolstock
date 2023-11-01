import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';
import 'package:smolstock/register.dart';
import 'package:smolstock/AuthHelper.dart';
import 'package:smolstock/home.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _usernameController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16.0),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 16.0),
            RichText(
              text:  TextSpan(
                text: "Don't have an account? ",
                style: const TextStyle(color: Colors.blue),
                children: <TextSpan> [
                  TextSpan(
                    text: 'Register',
                    style: const TextStyle(
                      color: Colors.blue,
                      decoration: TextDecoration.underline,
                      fontWeight: FontWeight.bold,
                    ),
                    recognizer: TapGestureRecognizer()
                      ..onTap = () {
                        // TODO: aprire la pagina di creazione account
                        Navigator
                            .of(context)
                            .pushReplacement(
                              MaterialPageRoute(
                                builder: (BuildContext context) => RegiserPage(),
                              ),
                        );
                      },
                  ),
                ]
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                String username = _usernameController.text;
                String password = _passwordController.text;

                RegistrationResult credentialValid = await AuthHelper.verifyCredentials(username, password);

                if(credentialValid.success) {
                  // TODO: inizializzare la sessione
                  Navigator
                      .of(context)
                      .pushReplacement(
                        MaterialPageRoute(
                          builder: (BuildContext context) => HomeScreen(),
                        )
                      );
                }
                else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(credentialValid.message),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              },
              child: Text('Login'),
            ),
          ],
        )
      )
    );
  }
}