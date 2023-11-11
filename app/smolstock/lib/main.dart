import "package:flutter/material.dart";
import "package:smolstock/AuthHelper.dart";
import "package:smolstock/home.dart";

import "login.dart";

void main() async{
  WidgetsFlutterBinding.ensureInitialized();
  bool isLoggedIn = await AuthHelper.isLoggedIn(); // appena apro l'app l'utente non è loggato
  runApp(MyApp(isLoggedIn));
}

class MyApp extends StatelessWidget {

  final bool isLoggedIn;

  MyApp(this.isLoggedIn);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "FinanceFlow",
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: isLoggedIn ? HomeScreen() : LoginPage()
    );
  }
}