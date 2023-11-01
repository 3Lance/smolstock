import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:smolstock/login.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: RegiserPage(),
    );
  }
}
class RegiserPage extends StatefulWidget {
  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegiserPage> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _surnameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  DateTime _selectedDate = DateTime.now();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Registration'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(
                labelText: 'Name',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _surnameController,
              decoration: InputDecoration(
                labelText: 'Surname',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _emailController,
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            SizedBox(height: 16),
            ListTile(
              title: Text(_selectedDate == null
                  ? 'Select your birthdate'
                  : 'Date of Birth: ${_selectedDate.toLocal().toString().split(' ')[0]}'),
              trailing: Icon(Icons.calendar_today),
              onTap: () async {
                DateTime? pickedDate = await showDatePicker(
                  context: context,
                  initialDate: DateTime.now(),
                  firstDate: DateTime(1900),
                  lastDate: DateTime.now(),
                );
                if (pickedDate != null) {
                  setState(() {
                    _selectedDate = pickedDate;
                  });
                }
              },
            ),
            SizedBox(height: 16),
            RichText(
              text:  TextSpan(
                  text: 'Already have an account? ',
                  style: const TextStyle(color: Colors.blue),
                  children: <TextSpan> [
                    TextSpan(
                      text: 'Login',
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
                              builder: (BuildContext context) => LoginPage(),
                            ),
                          );
                        },
                    ),
                  ]
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                // Qui potresti chiamare la tua funzione di registrazione
                print('Registering user...');
              },
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}
