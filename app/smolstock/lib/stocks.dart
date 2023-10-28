import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';
import 'dart:convert';

import 'line_chart.dart';

class StocksWidget extends StatefulWidget {
  @override
  _StocksWidgetState createState() => _StocksWidgetState();
}

class _StocksWidgetState extends State<StocksWidget> {
  Future<List<dynamic>?> fetchData() async {
    final Uri uri = Uri.parse(
        'https://api.polygon.io/v2/reference/news?apiKey=6460WG4fphwVemjxss71uvOmDqSV2dy0');
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      // If server returns an OK response, parse the JSON
      final List<dynamic>? results = json.decode(response.body)['results'];
      return results;
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception.
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('API Call Example'),
      ),
      body: LineChartSample2(),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: StocksWidget(),
  ));
}
