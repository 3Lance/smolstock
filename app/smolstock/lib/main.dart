import 'package:flutter/material.dart';

import 'chatbot.dart'; // Import the ChatBot screen
import 'home.dart'; // Import the Home screen
import 'news.dart'; // Import the News screen
import 'profile.dart'; // Import the Profile screen
import 'stocks.dart'; // Import the Stocks screen

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> with SingleTickerProviderStateMixin {
  int _currentIndex = 0;
  final List<Widget> _pages = [
    HomeScreen(),
    StocksScreen(),
    ChatBotScreen(),
    NewsScreen(),
    ProfileScreen(),
  ];

  late TabController _tabController;

  final List<String> pageTitles = [
    'Feed',
    'Stocks',
    'Help',
    'News',
    'Profile',
  ];

  final List<IconData> pageIcons = [
    Icons.feed,
    Icons.stacked_line_chart,
    Icons.quiz,
    Icons.newspaper,
    Icons.person,
  ];

  // Define your color variables here
  final Color primaryColor = const Color(0xFF0F2140); // Primary color
  final Color secondaryColor = const Color(0xFF749CAC); // Secondary color
  final Color thirdColor = const Color(0xFFDCF5FD); // Third color

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
      length: _pages.length,
      initialIndex: _currentIndex,
      vsync: this,
    );
    _tabController.addListener(() {
      setState(() {
        _currentIndex = _tabController.index;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '',
      theme: ThemeData(
        // Your theme configuration
        useMaterial3: true,
      ),
      home: DefaultTabController(
        length: _pages.length,
        child: Scaffold(
          body: TabBarView(
            controller: _tabController,
            children: _pages,
          ),
          bottomNavigationBar: Container(
            height: 64.0, // Adjust the height as needed
            decoration: const BoxDecoration(
              border: Border(
                top: BorderSide(
                  color: Color(0xFF0F2140), // Set a transparent underline
                  width: 2, // Set the underline thickness to 0
                ),
              ),
            ),
            child: TabBar(
              controller: _tabController,
              indicatorColor: secondaryColor, // Transparent underline
              tabs: [
                for (var i = 0; i < _pages.length; i++)
                  Tab(
                    icon: Icon(
                      pageIcons[i],
                      color: i == _currentIndex ? secondaryColor : primaryColor,
                    ),
                    child: Text(
                      pageTitles[i],
                      style: TextStyle(
                        color:
                            i == _currentIndex ? secondaryColor : primaryColor,
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
