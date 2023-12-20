import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:smolstock/Screens/Utilities/Widgets/auth_heading.dart';
import 'package:smolstock/Screens/Utilities/Widgets/log_in_button.dart';
import 'package:smolstock/Screens/Utilities/Widgets/logo_with_name.dart';
import 'package:url_launcher/url_launcher.dart';

import '../Utilities/Widgets/utilities.dart';

class MailOpener extends StatelessWidget {
  final String email;
  const MailOpener({super.key, required this.email});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Palette.secondaryBlackColor,
      body: SingleChildScrollView(
        child: Stack(children: [
          Column(
            children: [
              const SizedBox(height: 38),
              const CenterLogo(),
              const SizedBox(height: 80),
              SvgPicture.asset(
                "assests/illustrations/mailOpener.svg",
                height: 148,
                width: 148,
              ),
              const SizedBox(height: 64),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 64),
                child: authTitleLargeText("Almost there! Check your inbox"),
              ),
              const SizedBox(height: 20),
              authCenterText(
                  "Confirm your identity by clicking the link I sent to $email"),
              const SizedBox(height: 16),
              LogInButton(
                text: "Open Your Gmail",
                function: () async {
                  final url = Uri.parse('mailto:');
                  if (!await launchUrl(url)) {
                    throw 'Could not launch $url';
                  }
                },
              )
            ],
          ),
        ]),
      ),
    );
  }
}
