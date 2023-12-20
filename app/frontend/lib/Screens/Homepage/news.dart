// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smolstock/Screens/Homepage/News%20Tabs/news_page.dart';
import 'package:smolstock/Screens/Homepage/Profile/profile_tab.dart';
import 'package:smolstock/Screens/Homepage/chatbot.dart';
import 'package:smolstock/Screens/Homepage/wallet_tab.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/home_bottom_nav.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';

import 'invest_tab.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: Palette.secondaryBlackColor,
      // appBar: homeAppBar(),
      // se vogliamo togliere l'icona del profilo in alto togliamo questa riga di codice
      body: Stack(
        children: [
          newsPageWidgets[ref.watch(HomeBottomNavProvider)],
          const HomeBottomNavBar(),
        ],
      ),
    );
  }
}

List<Widget> newsPageWidgets = [
  //if (User.panVerify ?? false) const HomeTabPan() else const HomeTabNoPan(),
  const NewsPage(),
  const InvestTab(),
  const Chatbot(),
  const WalletTab(),
  ProfileTab()
];
