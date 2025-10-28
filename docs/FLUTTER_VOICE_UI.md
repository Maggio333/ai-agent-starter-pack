# 📱 Flutter Voice UI - Dokumentacja Frontend

## 📋 Przegląd

Frontend aplikacji Eliora AI Assistant zbudowany w **Flutter** z obsługą głosu, czatu w czasie rzeczywistym i zaawansowanymi funkcjami UI/UX.

## 🎯 Główne Funkcjonalności

### 1. **Voice Interface**
- **🎤 Microphone Recording**: Nagrywanie głosu w czasie rzeczywistym
- **🎵 Audio Playback**: Odtwarzanie odpowiedzi TTS
- **🔄 Voice Streaming**: Automatyczne wysyłanie zdań po wykryciu interpunkcji
- **📢 Sentence-by-Sentence TTS**: Mówienie zdanie po zdaniu

### 2. **Chat Interface**
- **💬 Chat Bubbles**: Eleganckie bąbelki rozmowy
- **🎨 Color Support**: Obsługa kolorów `<color=#hex>tekst</color>`
- **✨ Bold Support**: Obsługa pogrubienia `**tekst**`
- **📱 Responsive Design**: Adaptacyjny design na różnych ekranach

### 3. **Real-time Features**
- **⚡ Streaming Responses**: Otrzymywanie odpowiedzi w czasie rzeczywistym
- **🔄 SSE Client**: Server-Sent Events dla live updates
- **📊 Debug Panel**: Panel debugowania z logami w czasie rzeczywistym

### 4. **Advanced UI**
- **🎨 Pastel Theme**: Elegancki motyw pastelowy
- **🌙 Dark Mode**: Ciemny motyw
- **📋 Copy Logs**: Kopiowanie logów do schowka
- **🔧 Debug Tools**: Narzędzia developerskie

## 🏗️ Architektura Frontend

### Component Structure
```
lib/
├── main.dart                 # Main app entry point
├── text_formatter.dart       # Text formatting utilities
├── models/
│   └── chat_message.dart     # Chat message model
├── services/
│   ├── api_service.dart      # API communication
│   ├── audio_service.dart    # Audio handling
│   └── speech_service.dart   # Speech recognition
└── widgets/
    ├── chat_bubble.dart      # Chat bubble widget
    ├── debug_panel.dart      # Debug panel widget
    └── voice_button.dart     # Voice recording button
```

### State Management
```dart
class _MyAppState extends State<MyApp> {
  // Chat state
  List<ChatMessage> _messages = [];
  String _currentResponse = '';
  
  // Voice state
  bool _isRecording = false;
  bool _isPlaying = false;
  bool _isMuted = false;
  
  // Streaming state
  bool _isStreaming = false;
  String _streamingText = '';
  
  // Debug state
  List<String> _debugLogs = [];
  bool _showDebugPanel = false;
}
```

## 🎨 UI Components

### 1. **Chat Bubble**
```dart
class ChatBubble extends StatelessWidget {
  final ChatMessage message;
  final bool isUser;
  
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 4, horizontal: 16),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!isUser) ...[
            CircleAvatar(
              backgroundColor: Colors.purple.shade200,
              child: Icon(Icons.smart_toy, color: Colors.white),
            ),
            SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isUser ? Colors.blue.shade100 : Colors.grey.shade100,
                borderRadius: BorderRadius.circular(16),
              ),
              child: TextFormatter.formatText(message.text),
            ),
          ),
          if (isUser) ...[
            SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: Colors.blue.shade200,
              child: Icon(Icons.person, color: Colors.white),
            ),
          ],
        ],
      ),
    );
  }
}
```

### 2. **Voice Button**
```dart
class VoiceButton extends StatefulWidget {
  final VoidCallback onPressed;
  final bool isRecording;
  
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => onPressed(),
      onTapUp: (_) => onPressed(),
      child: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          color: isRecording ? Colors.red : Colors.blue,
          shape: BoxShape.circle,
        ),
        child: Icon(
          isRecording ? Icons.mic : Icons.mic_none,
          color: Colors.white,
          size: 30,
        ),
      ),
    );
  }
}
```

### 3. **Debug Panel**
```dart
class DebugPanel extends StatelessWidget {
  final List<String> logs;
  final VoidCallback onClear;
  final VoidCallback onCopy;
  
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      decoration: BoxDecoration(
        color: Colors.black87,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          // Header with controls
          Container(
            padding: EdgeInsets.all(8),
            child: Row(
              children: [
                Text('Debug Logs', style: TextStyle(color: Colors.white)),
                Spacer(),
                IconButton(
                  icon: Icon(Icons.copy, color: Colors.white, size: 16),
                  onPressed: onCopy,
                ),
                IconButton(
                  icon: Icon(Icons.clear, color: Colors.white, size: 16),
                  onPressed: onClear,
                ),
              ],
            ),
          ),
          // Logs display
          Expanded(
            child: ListView.builder(
              itemCount: logs.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  child: Text(
                    logs[index],
                    style: TextStyle(color: Colors.green, fontSize: 12),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

## 🎵 Audio System

### 1. **TTS Queue Management**
```dart
class AudioManager {
  final AudioPlayer _player = AudioPlayer();
  final List<String> _ttsQueue = [];
  bool _isSpeaking = false;
  
  Future<void> addToTTSQueue(String sentence) async {
    _ttsQueue.add(sentence);
    if (!_isSpeaking) {
      await _processTTSQueue();
    }
  }
  
  Future<void> _processTTSQueue() async {
    if (_ttsQueue.isEmpty) return;
    
    _isSpeaking = true;
    final sentence = _ttsQueue.removeAt(0);
    
    try {
      await _synthesizeSpeech(sentence);
      await _player.onPlayerComplete.first;
    } finally {
      _isSpeaking = false;
      if (_ttsQueue.isNotEmpty) {
        await _processTTSQueue();
      }
    }
  }
}
```

### 2. **Sentence Detection**
```dart
List<String> _extractCompleteSentences(String text) {
  final regex = RegExp(r'[^.!?]*[.!?]+');
  final matches = regex.allMatches(text);
  
  return matches.map((match) => match.group(0)!.trim()).toList();
}

void _processSentenceTTS(String chunk) {
  final sentences = _extractCompleteSentences(chunk);
  
  for (final sentence in sentences) {
    if (sentence.isNotEmpty) {
      _addToTTSQueue(sentence);
    }
  }
}
```

## 🔄 Streaming System

### 1. **SSE Client**
```dart
class SSEClient {
  static Future<void> streamMessage(String message, Function(String) onChunk) async {
    final uri = Uri.parse('http://localhost:8080/api/message/stream')
        .replace(queryParameters: {'message': message});
    
    final request = http.Request('GET', uri);
    final streamedResponse = await request.send();
    
    await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
      final lines = chunk.split('\n');
      
      for (final line in lines) {
        if (line.startsWith('data: ')) {
          final data = line.substring(6);
          if (data.isNotEmpty) {
            final json = jsonDecode(data);
            onChunk(json['chunk']);
          }
        }
      }
    }
  }
}
```

### 2. **Real-time Updates**
```dart
void _sendToAI(String message) async {
  setState(() {
    _isStreaming = true;
    _streamingText = '';
  });
  
  // Add user message
  _messages.add(ChatMessage(
    role: MessageRole.user,
    text: message,
    timestamp: DateTime.now(),
  ));
  
  // Add empty AI message for streaming
  final aiMessage = ChatMessage(
    role: MessageRole.assistant,
    text: '',
    timestamp: DateTime.now(),
  );
  _messages.add(aiMessage);
  
  // Stream response
  await SSEClient.streamMessage(message, (chunk) {
    setState(() {
      _streamingText += chunk;
      // Update the last message
      _messages.removeLast();
      _messages.add(ChatMessage(
        role: MessageRole.assistant,
        text: _streamingText,
        timestamp: DateTime.now(),
      ));
    });
    
    // Process TTS for each chunk
    _processSentenceTTS(chunk);
  });
  
  setState(() {
    _isStreaming = false;
  });
}
```

## 🎨 Text Formatting

### 1. **Color and Bold Support**
```dart
class TextFormatter {
  static Widget formatText(String text) {
    final spans = <TextSpan>[];
    final regex = RegExp(r'<color=#([0-9a-fA-F]{6})>(.*?)</color>|\*\*(.*?)\*\*');
    
    int lastEnd = 0;
    for (final match in regex.allMatches(text)) {
      // Add text before match
      if (match.start > lastEnd) {
        spans.add(TextSpan(text: text.substring(lastEnd, match.start)));
      }
      
      // Add formatted text
      if (match.group(1) != null) {
        // Color tag
        final color = Color(int.parse('FF${match.group(1)}', radix: 16));
        spans.add(TextSpan(
          text: match.group(2),
          style: TextStyle(color: color),
        ));
      } else if (match.group(3) != null) {
        // Bold tag
        spans.add(TextSpan(
          text: match.group(3),
          style: TextStyle(fontWeight: FontWeight.bold),
        ));
      }
      
      lastEnd = match.end;
    }
    
    // Add remaining text
    if (lastEnd < text.length) {
      spans.add(TextSpan(text: text.substring(lastEnd)));
    }
    
    return RichText(text: TextSpan(children: spans));
  }
}
```

### 2. **Strip Formatting for TTS**
```dart
String _stripFormatting(String text) {
  return text
      .replaceAll(RegExp(r'<color=#[0-9a-fA-F]{6}>(.*?)</color>'), r'$1')
      .replaceAll(RegExp(r'\*\*(.*?)\*\*'), r'$1');
}
```

## 🎨 Theme System

### 1. **Pastel Theme**
```dart
class PastelTheme {
  static const Color primary = Color(0xFFE1BEE7);
  static const Color secondary = Color(0xFFB39DDB);
  static const Color accent = Color(0xFF9575CD);
  static const Color background = Color(0xFFF3E5F5);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color text = Color(0xFF424242);
}
```

### 2. **Dark Theme**
```dart
class DarkTheme {
  static const Color primary = Color(0xFF4A148C);
  static const Color secondary = Color(0xFF6A1B9A);
  static const Color accent = Color(0xFF8E24AA);
  static const Color background = Color(0xFF121212);
  static const Color surface = Color(0xFF1E1E1E);
  static const Color text = Color(0xFFE0E0E0);
}
```

## 🔧 Debug Features

### 1. **Debug Logging**
```dart
void _addDebugLog(String message) {
  setState(() {
    _debugLogs.add('${DateTime.now().toString().substring(11, 19)}: $message');
    
    // Keep only last 100 logs
    if (_debugLogs.length > 100) {
      _debugLogs.removeAt(0);
    }
  });
}
```

### 2. **Copy Logs**
```dart
void _copyLogsToClipboard() {
  final allLogs = _debugLogs.join('\n');
  html.window.navigator.clipboard?.writeText(allLogs);
  _addDebugLog('📋 Logs copied to clipboard!');
}
```

## 🚀 Performance Optimizations

### 1. **Widget Optimization**
- **const constructors**: Immutable widgets
- **ListView.builder**: Lazy loading for messages
- **AutomaticKeepAliveClientMixin**: Preserve state

### 2. **Memory Management**
- **Limited log history**: Keep only last 100 logs
- **Audio cleanup**: Dispose audio players
- **Stream cleanup**: Cancel ongoing streams

### 3. **Network Optimization**
- **Connection pooling**: Reuse HTTP connections
- **Request debouncing**: Prevent spam requests
- **Error handling**: Graceful degradation

## 🧪 Testing

### 1. **Widget Tests**
```dart
testWidgets('Chat bubble displays correctly', (WidgetTester tester) async {
  await tester.pumpWidget(MaterialApp(
    home: ChatBubble(
      message: ChatMessage(
        role: MessageRole.assistant,
        text: 'Hello!',
        timestamp: DateTime.now(),
      ),
      isUser: false,
    ),
  ));
  
  expect(find.text('Hello!'), findsOneWidget);
});
```

### 2. **Integration Tests**
```dart
testWidgets('Voice recording works', (WidgetTester tester) async {
  await tester.pumpWidget(MyApp());
  
  await tester.tap(find.byType(VoiceButton));
  await tester.pump();
  
  expect(find.byIcon(Icons.mic), findsOneWidget);
});
```

## 🔮 Future Enhancements

### 1. **Advanced Voice Features**
- **Voice Cloning**: Custom voice synthesis
- **Emotion Detection**: Voice emotion analysis
- **Multi-language**: Multiple language support
- **Voice Commands**: Voice-based navigation

### 2. **UI/UX Improvements**
- **Animations**: Smooth transitions
- **Gestures**: Swipe interactions
- **Accessibility**: Screen reader support
- **Customization**: User preferences

### 3. **Performance**
- **Offline Mode**: Cached responses
- **Background Processing**: Background audio
- **Progressive Loading**: Incremental content
- **Memory Optimization**: Better resource management

## 📚 Related Documentation

- **[Project Overview](PROJECT_OVERVIEW.md)** - Przegląd projektu
- **[Architecture](ARCHITECTURE.md)** - Architektura systemu
- **[API Endpoints](API_ENDPOINTS.md)** - Dokumentacja API
- **[Debug Tools](DEBUG_TOOLS.md)** - Narzędzia debugowe