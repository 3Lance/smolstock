// ignore_for_file: use_build_context_synchronously
import 'package:smolstock/Models/news_model.dart';
import 'package:smolstock/Screens/Utilities/Riverpod/riverpod_variables.dart';
import 'package:smolstock/Screens/Utilities/Widgets/cypto_news_item_builder.dart';
import 'package:smolstock/Screens/Utilities/Widgets/utilities.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../Utilities/Widgets/auth_heading.dart';

class NewsPage extends ConsumerWidget {
  const NewsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final news = ref.watch(getNewsProvider);
    return SizedBox(
      height: double.infinity,
      width: double.infinity,
      child: Padding(
        padding: const EdgeInsets.only(top: 40, left: 16, right: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            authTitleLargeText("News"),
            const SizedBox(height: 8),
            Expanded(
              child: news.when(
                data: (data) {
                  return ListView.builder(
                    itemBuilder: (context, index) {
                      return ((index) != (data.length))
                          ? cryptoNewsItemBuilder(
                              News(
                                headline: data[index]['headline'],
                                news: data[index]['news'],
                                image: data[index]['image'],
                              ),
                            )
                          : Container(height: 100);
                    },
                    itemCount: data.length + 1,
                  );
                },
                error: (error, stackTrace) {
                  return Center(
                    child: Text(
                      error.toString(),
                      style: titleLarge(),
                    ),
                  );
                },
                loading: () => const Center(
                  child: CircularProgressIndicator(
                    color: Palette.primaryColor,
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
