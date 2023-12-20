class ChatbotMessage {
  String message;
  bool isUser;
  String date;
  ChatbotMessage(
      {required this.message, required this.isUser, required this.date});
  getDate() {
    DateTime now = DateTime.now();
    String formattedDate = now.toString();
    return formattedDate;
  }
}
