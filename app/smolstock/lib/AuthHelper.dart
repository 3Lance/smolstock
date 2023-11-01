import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

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

  static Future<File> registerUser(String name, String surname, String email, String password, DateTime birthDate) async {
    final file = await _localFile;
    Map<String, dynamic> users = (await readUsers()).cast<String, dynamic>();

    if(users.containsKey(email)) throw Exception('user $email already registered');

    Map<String, dynamic> userInfo = {
      'name': name,
      'surname': surname,
      'email': email,
      'password': password,
      'birthDate': birthDate.toIso8601String(),
    };

    users[email] = userInfo;
    return file.writeAsString(json.encode(users));
  }

  static Future<bool> verifyCredentials(String email, String password) async {
    Map<String, dynamic> users = await readUsers();

    return users.containsKey(email) && users[email]['password'] == password;
  }
}