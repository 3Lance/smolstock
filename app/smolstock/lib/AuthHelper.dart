import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class RegistrationResult {
  final bool success;
  final String message;

  RegistrationResult(this.success, this.message);
}

class AuthHelper {
  static Future<File> get _localFile async {
    final directory = await getApplicationDocumentsDirectory();
    // default path is /data/user/0/com.example.smolstock/app_flutter in the device file system
    return File('${directory.path}/users.json');
  }

  static Future<Map<String, dynamic>> readUsers() async {
    try {
      final file = await _localFile;
      if(!file.existsSync()) return {};

      String contents = await file.readAsString();
      return Map<String, dynamic>.from(json.decode(contents));
    } catch (e) {
      return {};
    }
  }

  static Future<RegistrationResult> registerUser(String name, String surname, String email, String password, DateTime birthDate) async {
    final file = await _localFile;
    Map<String, dynamic> users = (await readUsers()).cast<String, dynamic>();

    if(users.containsKey(email)) {
      return RegistrationResult(false, 'user $email already exists');
    }

    Map<String, dynamic> userInfo = {
      'name': name,
      'surname': surname,
      'email': email,
      'password': password,
      'birthDate': birthDate.toIso8601String(),
    };

    users[email] = userInfo;
    await file.writeAsString(json.encode(users));
    return RegistrationResult(true, 'user $email registered successfully');
  }

  static Future<RegistrationResult> verifyCredentials(String email, String password) async {
    Map<String, dynamic> users = await readUsers();
    bool success = users.containsKey(email) && users[email]['password'] == password;
    return RegistrationResult(success, success ? 'user $email logged in successfully' : 'invalid credentials');
  }
}