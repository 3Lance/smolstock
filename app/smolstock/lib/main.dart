import 'package:flutter/material.dart';

import 'chatbot.dart';
import 'home.dart';
import 'login.dart';
import 'news.dart';
import 'profile.dart';
import 'stocks.dart';

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
    StocksWidget(),
    ChatBotScreen(),
    NewsWidget(),
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
    Icons.leaderboard,
    Icons.quiz,
    Icons.newspaper,
    Icons.person,
  ];

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
      title: 'LoginApp',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginPage(),
    );
  }
    /*
    return MaterialApp(
      title: '',
      theme: ThemeData(
        useMaterial3: true,

        colorScheme: ColorScheme(
          brightness: Brightness.light,
          primary: Colors.lightBlue,
          onPrimary: Colors.white,
          secondary: Colors.white,
          onSecondary: Colors.white,
          error: Colors.white,
          onError: Colors.white,
          background: Colors.white,
          onBackground: Colors.white,
          surface: Colors.white,
          onSurface: Colors.grey,
        ),
      ),

      home: DefaultTabController(
        length: _pages.length,
        child: Scaffold(
          body: TabBarView(
            physics: const NeverScrollableScrollPhysics(),
            controller: _tabController,
            children: _pages,
          ),
          bottomNavigationBar: Container(
            height: 64.0,
            child: TabBar(
              controller: _tabController,
              indicatorColor: Theme.of(context).colorScheme.background,
              tabs: [
                for (var i = 0; i < _pages.length; i++)
                  Tab(
                    icon: Icon(
                      pageIcons[i],
                    ),
                    child: Text(
                      pageTitles[i],
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
  */
}
