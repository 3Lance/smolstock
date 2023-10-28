import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'dart:convert';

class NewsWidget extends StatefulWidget {
  @override
  _NewsWidgetState createState() => _NewsWidgetState();
}

class _NewsWidgetState extends State<NewsWidget> {
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
      body: FutureBuilder(
        future: fetchData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            // If the Future is still running, show a loading indicator
            return CircularProgressIndicator();
          } else if (snapshot.hasError) {
            // If an error occurred, display the error message
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          } else {
            // If the Future is complete, display the data
            final List<dynamic>? data = snapshot.data;
            if (data != null) {
              return ListView.builder(
                itemCount: data.length,
                itemBuilder: (context, index) {
                  final article = data[index];
                  return ListTile(
                    leading: SizedBox(
                      height: 100.0,
                      width: 100.0,
                      child: CachedNetworkImage(
                        imageUrl: article["image_url"],
                        placeholder: (context, url) => CircularProgressIndicator(),
                        errorWidget: (context, url, error) => Icon(Icons.error),
                      ),
                    ),
                    title: Text(utf8.decode(article['title'].codeUnits)),
                    onTap: () async {
                      final Uri url = Uri.parse(article['article_url']);
                      if (!await launchUrl(url)) {
                        throw Exception('Could not launch ${url}');
                      }
                    },
                  );
                },
              );
            } else {
              return Center(
                child: Text('No data available'),
              );
            }
          }
        },
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: NewsWidget(),
  ));
}
