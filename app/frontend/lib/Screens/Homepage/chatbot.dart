// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';

import '../Utilities/Widgets/auth_heading.dart';
import 'ChatBot Tabs/chatbot_message.dart';

class Chatbot extends ConsumerWidget {
  const Chatbot({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: Palette.secondaryBlackColor,
      body: Column(
        children: [
          // Use the same top padding as the NewsPage
          Padding(
            padding: const EdgeInsets.only(top: 40),
            child: authTitleLargeText("ChatBot"),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: ListView.builder(
              itemCount: ref.watch(chatbotProvider).length,
              itemBuilder: (context, index) {
                ChatbotMessage message =
                    ref.watch(chatbotProvider)[index] as ChatbotMessage;
                return ChatbotMessage(
                  message: message.message,
                  isUser: message.isUser,
                  date: message.date,
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: ref.watch(chatbotTextProvider),
                    decoration: InputDecoration(
                      hintText: "Type a message",
                      hintStyle: labelMedium(fontColor: Palette.neutralGrey),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(16),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Palette.neutralGrey,
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                GestureDetector(
                  onTap: () {
                    ref.read(chatbotProvider.notifier).addMessage(
                          ref.watch(chatbotTextProvider).text,
                          true,
                        );
                    ref.read(chatbotTextProvider).clear();
                  },
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Palette.primaryColor,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Icon(
                      Icons.send,
                      color: Palette.neutralBlack,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
