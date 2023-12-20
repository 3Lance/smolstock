import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smolstock/Routing/route_names.dart';
import 'package:smolstock/Screens/AuthScreens/forget_pass_otp_page.dart';
import 'package:smolstock/Screens/AuthScreens/forget_password_page.dart';
import 'package:smolstock/Screens/AuthScreens/mail_opener.dart';
import 'package:smolstock/Screens/AuthScreens/pan_number_page.dart';
import 'package:smolstock/Screens/AuthScreens/set_password.dart';
import 'package:smolstock/Screens/AuthScreens/sign_in_page.dart';
import 'package:smolstock/Screens/AuthScreens/sign_up_page.dart';
import 'package:smolstock/Screens/AuthScreens/two_factor_page.dart';
import 'package:smolstock/Screens/AuthScreens/verification_checker.dart';
import 'package:smolstock/Screens/Homepage/Profile/change_password.dart';
import 'package:smolstock/Screens/Homepage/Profile/phone_number_page.dart';
import 'package:smolstock/Screens/Homepage/Profile/phone_otp_page.dart';
import 'package:smolstock/Screens/Homepage/Profile/profile_pan.dart';
import 'package:smolstock/Screens/Homepage/Profile/security.dart';
import 'package:smolstock/Screens/Homepage/coin_page.dart';
import 'package:smolstock/Screens/Homepage/news.dart';
import 'package:smolstock/Screens/Utilities/static_classes.dart';

class AppRouter {
  static GoRouter router = GoRouter(
    navigatorKey: App.navigatorKey,
    routes: [
      GoRoute(
        name: RouteNames.root,
        path: '/',
        pageBuilder: (context, state) {
          return MaterialPage(
              child: App.isLoggedIn ? const HomePage() : SignInPage());
        },
      ),
      GoRoute(
        name: RouteNames.signIn,
        path: '/signin',
        pageBuilder: (context, state) {
          return MaterialPage(
            child: SignInPage(),
          );
        },
        routes: [
          GoRoute(
              name: RouteNames.forgetPassword,
              path: 'forgetpassword',
              pageBuilder: (context, state) {
                return MaterialPage(
                  child: ForgetPasswordPage(),
                );
              },
              routes: [
                GoRoute(
                  name: RouteNames.forgetpassOTP,
                  path: 'forgetpassotp/:email',
                  pageBuilder: (context, state) {
                    return MaterialPage(
                      child: ForgetPassOtpPage(
                        email: state.pathParameters['email']!,
                      ),
                    );
                  },
                ),
                GoRoute(
                  name: RouteNames.setPassword,
                  path: 'setpassword/:email/:otp',
                  pageBuilder: (context, state) {
                    return MaterialPage(
                      child: SetPasswordPage(
                        email: state.pathParameters['email']!,
                        otp: state.pathParameters['otp']!,
                      ),
                    );
                  },
                )
              ]),
          GoRoute(
            name: RouteNames.twoFactor,
            path: 'twofactor',
            pageBuilder: (context, state) {
              return const MaterialPage(
                child: TwoFactorPage(),
              );
            },
          ),
        ],
      ),
      GoRoute(
        name: RouteNames.signUp,
        path: '/signup',
        pageBuilder: (context, state) {
          return MaterialPage(
            child: SignUpPage(),
          );
        },
        routes: [
          GoRoute(
            name: RouteNames.mailOpener,
            path: 'mailopener/:email',
            pageBuilder: (context, state) {
              return MaterialPage(
                child: MailOpener(
                  email: state.pathParameters['email']!,
                ),
              );
            },
          ),
        ],
      ),
      GoRoute(
        name: RouteNames.panNumber,
        path: '/pannumber/:email',
        pageBuilder: (context, state) {
          return MaterialPage(
            child: PanNumberPage(
              email: state.pathParameters['email']!,
            ),
          );
        },
      ),
      GoRoute(
        name: RouteNames.verifier,
        path: '/verifier/:email/:token',
        pageBuilder: (context, state) {
          return MaterialPage(
            child: VerificationChecker(
                email: state.pathParameters['email']!,
                token: state.pathParameters['token']!),
          );
        },
      ),
      GoRoute(
        name: RouteNames.homePage,
        path: '/homepage',
        pageBuilder: (context, state) {
          return const MaterialPage(
            child: HomePage(),
          );
        },
        routes: [
          GoRoute(
            name: RouteNames.coinPage,
            path: 'coinpage/:shortName',
            pageBuilder: (context, state) {
              log(state.pathParameters.toString());
              return MaterialPage(
                child: CoinPage(
                  shortName: state.pathParameters['shortName']!,
                ),
              );
            },
          ),
          GoRoute(
            name: RouteNames.personalDetails,
            path: 'personaldetails',
            pageBuilder: (context, state) {
              return MaterialPage(
                child: ProfilePan(),
              );
            },
          ),
          GoRoute(
            name: RouteNames.security,
            path: 'security',
            pageBuilder: (context, state) {
              return const MaterialPage(
                child: Security(),
              );
            },
            routes: [
              GoRoute(
                name: RouteNames.changePassword,
                path: 'changepassword',
                pageBuilder: (context, state) {
                  return MaterialPage(
                    child: ChangePassword(),
                  );
                },
              ),
              GoRoute(
                name: RouteNames.phoneNumber,
                path: 'phonenumber',
                pageBuilder: (context, state) {
                  return MaterialPage(
                    child: PhoneNumberPage(),
                  );
                },
                routes: [
                  GoRoute(
                    name: RouteNames.phoneNumberOTP,
                    path: 'phonenumberOTP:/phone_number',
                    pageBuilder: (context, state) {
                      return MaterialPage(
                        child: PhoneOtpPage(
                          phoneNumber: state.pathParameters['phone_number']!,
                        ),
                      );
                    },
                  )
                ],
              ),
            ],
          )
        ],
      ),
    ],
  );
}
