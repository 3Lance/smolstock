import 'package:flutter/material.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';

class CenterLogo extends StatelessWidget {
  const CenterLogo({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Padding(
          padding: const EdgeInsets.all(2.0),
        ),
        Padding(
          padding: const EdgeInsets.all(2.0),
          child: Text("FinanceFlow",
              style: titleMedium(fontColor: Palette.secondaryOffWhiteColor)),
        )
      ],
    );
  }
}
