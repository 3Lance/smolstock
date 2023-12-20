// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smolstock/Config/api_functions.dart';
import 'package:smolstock/Config/api_integration.dart';
import 'package:smolstock/Routing/route_names.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/logo_with_name.dart';
import 'package:smolstock/Screens/Utilities/Widgets/two_factor_otp_page.dart';
import 'package:smolstock/Screens/Utilities/static_classes.dart';
import 'package:toast/toast.dart';

import '../Utilities/Widgets/utilities.dart';

class TwoFactorPage extends StatelessWidget {
  const TwoFactorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Palette.secondaryBlackColor,
      body: SingleChildScrollView(
        child: Stack(
          children: [
            Column(
              children: [
                const SizedBox(height: 38),
                const CenterLogo(),
                const SizedBox(height: 93),
                TwoFactorOtpBox(
                  loaderProvider: twoFactorButtonLoaderProvider,
                  buttonFunction: (pin) async {
                    twoFactorButtonLoaderNotifier.toggle();

                    final output = await ApiCalls.loginVerifyTwoFactor(pin);

                    if (output['statusCode'] == 200) {
                      App.isLoggedIn = true;
                      await saveData(output, false);
                      await saveData(await ApiCalls.getUserDetails(), true);
                      context.goNamed(RouteNames.homePage);
                    } else if (output['statusCode'] == 400) {
                      ToastContext().init(context);
                      Toast.show("${output[output.keys.first][0]}",
                          duration: 5, gravity: Toast.bottom);
                      context.pop();
                    } else {
                      ToastContext().init(context);
                      Toast.show("${output[output.keys.first][0]}",
                          duration: 5, gravity: Toast.bottom);
                    }
                    twoFactorButtonLoaderNotifier.toggle();
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
