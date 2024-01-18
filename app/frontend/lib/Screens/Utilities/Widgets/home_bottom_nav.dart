import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';
import 'package:url_launcher/url_launcher.dart';

class HomeBottomNavBar extends ConsumerWidget {
  const HomeBottomNavBar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    int page = ref.watch(HomeBottomNavProvider);
    return SizedBox(
      child: Align(
        alignment: Alignment.bottomCenter,
        /*child: Padding(
          padding: const EdgeInsets.only(bottom: 24.0, left: 16, right: 16),*/
        child: Container(
          height: 76,
          width: double.infinity,
          decoration: const BoxDecoration(
            color: Palette.neutralBlack,
            borderRadius: /*BorderRadius.all(
              Radius.circular(20),
            ),*/
                BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
            ),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: bottomnavbaritems(page),
          ),
        ),
        //),
      ),
    );
  }
}

List<Widget> bottomnavbaritems(int page) {
  return [
    InkWell(
      onTap: () {
        homeBottomNavNotifier.setPage(0);
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.newspaper,
            color: page == 0
                ? Palette.primaryColor
                : Palette.secondaryOffWhiteColor,
          ),
          Text(
            "News",
            style: labelMedium(
                fontColor: page == 0
                    ? Palette.primaryColor
                    : Palette.secondaryOffWhiteColor),
          )
        ],
      ),
    ),
    InkWell(
      onTap: () {
        homeBottomNavNotifier.setPage(1);
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.monetization_on_sharp,
            color: page == 1
                ? Palette.primaryColor
                : Palette.secondaryOffWhiteColor,
          ),
          Text(
            "Invest",
            style: labelMedium(
                fontColor: page == 1
                    ? Palette.primaryColor
                    : Palette.secondaryOffWhiteColor),
          )
        ],
      ),
    ),
    InkWell(
      onTap: () {
        //homeBottomNavNotifier.setPage(2);
        _launchUrl();
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.smart_toy_rounded,
            color: page == 2
                ? Palette.primaryColor
                : Palette.secondaryOffWhiteColor,
          ),
          Text(
            "ChatBot",
            style: labelMedium(
                fontColor: page == 2
                    ? Palette.primaryColor
                    : Palette.secondaryOffWhiteColor),
          )
        ],
      ),
    ),
    InkWell(
      onTap: () {
        homeBottomNavNotifier.setPage(3);
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.wallet_sharp,
            color: page == 3
                ? Palette.primaryColor
                : Palette.secondaryOffWhiteColor,
          ),
          Text(
            "Wallet",
            style: labelMedium(
                fontColor: page == 3
                    ? Palette.primaryColor
                    : Palette.secondaryOffWhiteColor),
          )
        ],
      ),
    ),
    InkWell(
      onTap: () {
        homeBottomNavNotifier.setPage(4);
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.person_outline_sharp,
            color: page == 4
                ? Palette.primaryColor
                : Palette.secondaryOffWhiteColor,
          ),
          Text(
            "Profile",
            style: labelMedium(
                fontColor: page == 4
                    ? Palette.primaryColor
                    : Palette.secondaryOffWhiteColor),
          )
        ],
      ),
    )
  ];
}

final Uri _url = Uri.parse('https://flutter.dev');

Future<void> _launchUrl() async {
  if (!await launchUrl(_url)) {
    throw Exception('Could not launch $_url');
  }
}