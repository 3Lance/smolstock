import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smolstock/Routing/route_names.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';

class SignInUpTabs extends StatelessWidget {
  const SignInUpTabs({super.key, required this.choice});
  final int choice;
  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        GestureDetector(
          onTap: () {
            context.goNamed(RouteNames.signIn);
          },
          child: SizedBox(
            height: 44,
            width: 156,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                SizedBox(
                  height: 42,
                  child: Center(
                    child: Text(
                      "Sign In",
                      style: titleSmall(
                          fontColor: choice == 0
                              ? Palette.primaryColor
                              : Palette.secondaryOffWhiteColor),
                    ),
                  ),
                ),
                Container(
                  height: 2,
                  color:
                      choice == 0 ? Palette.primaryColor : Colors.transparent,
                )
              ],
            ),
          ),
        ),
        GestureDetector(
          onTap: () {
            context.goNamed(RouteNames.signUp);
          },
          child: SizedBox(
            height: 44,
            width: 156,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                SizedBox(
                  height: 42,
                  child: Center(
                    child: Text(
                      "Sign Up",
                      style: titleSmall(
                          fontColor: choice == 1
                              ? Palette.primaryColor
                              : Palette.secondaryOffWhiteColor),
                    ),
                  ),
                ),
                Container(
                  height: 2,
                  color:
                      choice == 1 ? Palette.primaryColor : Colors.transparent,
                )
              ],
            ),
          ),
        ),
      ],
    );
  }
}
