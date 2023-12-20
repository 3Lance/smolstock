import 'package:flutter/material.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';

class ChatbotMessage extends StatelessWidget {
  final String message;
  final bool isUser;
  final String date;
  const ChatbotMessage(
      {Key? key,
      required this.message,
      required this.isUser,
      required this.date})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: isUser ? 16 : 0, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            decoration: BoxDecoration(
              color: isUser ? Palette.primaryColor : Palette.neutralGrey,
              borderRadius: BorderRadius.circular(16),
            ),
            padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Text(
              message,
              style: labelMedium(
                  fontColor:
                      isUser ? Palette.neutralBlack : Palette.neutralBlack),
            ),
          ),
          SizedBox(height: 4),
          Text(
            date,
            style: labelMedium(fontColor: Palette.neutralGrey),
          ),
        ],
      ),
    );
  }
}
