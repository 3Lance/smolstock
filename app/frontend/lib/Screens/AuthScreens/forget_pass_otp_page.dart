// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smolstock/Config/api_functions.dart';
import 'package:smolstock/Config/api_integration.dart';
import 'package:smolstock/Routing/route_names.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/logo_with_name.dart';
import 'package:smolstock/Screens/Utilities/Widgets/otp_box.dart';
import 'package:toast/toast.dart';

import '../Utilities/Widgets/utilities.dart';

class ForgetPassOtpPage extends StatelessWidget {
  final String email;

  const ForgetPassOtpPage({super.key, required this.email});

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
                OtpBox(
                  loaderProvider: forgetPassOtpButtonLoaderProvider,
                  timerNotifier: forgetPassOtpTimerNotifer,
                  timerProvider: forgetPassOtpTimerProvider,
                  sentAt: 'email address',
                  buttonFunction: (pin) async {
                    ToastContext().init(context);

                    forgetPassOtpButtonLoaderNotifier.toggle();
                    final response =
                        await ApiCalls.verifyEmailOTP(email: email, otp: pin);
                    forgetPassOtpButtonLoaderNotifier.toggle();
                    if (response == noInternet) {
                      internetHandler(context);
                    } else {
                      if (response['statusCode'] == 200) {
                        Toast.show("Remember the password this time",
                            duration: 5, gravity: Toast.bottom);
                        context.goNamed(RouteNames.setPassword,
                            pathParameters: {
                              'email': email,
                              'otp': pin.toString()
                            });
                      } else {
                        Toast.show(response[response.keys.first][0],
                            duration: 5, gravity: Toast.bottom);
                      }
                    }
                  },
                  resendFunction: () async {
                    ToastContext().init(context);
                    forgetPassOtpButtonLoaderNotifier.toggle();

                    final response = await ApiCalls.sendEmailOTP(email: email);
                    forgetPassOtpButtonLoaderNotifier.toggle();

                    if (response == noInternet) {
                      internetHandler(context);
                    } else {
                      if (response['statusCode'] == 200) {
                        Toast.show("Resent The OTP",
                            duration: 5, gravity: Toast.bottom);
                      } else {
                        Toast.show(response[response.keys.first][0],
                            duration: 5, gravity: Toast.bottom);
                      }
                    }
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
