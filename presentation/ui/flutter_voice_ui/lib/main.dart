import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:developer' as developer;
import 'dart:html' as html;
import 'dart:convert' show utf8;
import 'dart:async';
import 'text_formatter.dart';
import 'config/api_config.dart';

// Color palette - Pastel Elegant Theme
class AppColors {
  // User message colors
  static const Color userMessageBg = Color(0xFFB8E6B8);
  static const Color userMessageText = Color(0xFF2D5A2D);
  static const Color userMessageTimestamp = Color(0xFF4A7C4A);
  static const Color userAvatarBg = Color(0xFFE8F5E8);
  static const Color userAvatarIcon = Color(0xFF58D68D);
  
  // AI message colors - Dark theme
  static const Color aiMessageBg = Color(0xFF404040);
  static const Color aiMessageText = Color(0xFFE8E8E8);
  static const Color aiMessageTimestamp = Color(0xFFB0B0B0);
  static const Color aiAvatarBg = Color(0xFF4A4A4A);
  static const Color aiAvatarIcon = Color(0xFF7DD3FC);
  
  // Button colors - Dark theme
  static const Color sendButton = Color(0xFF7DD3FC);
  static const Color micButtonActive = Color(0xFF58D68D);
  static const Color micButtonRecording = Color(0xFFE74C3C);
  
  // Mute checkbox colors
  static const Color muteBgActive = Color(0xFFE8F8F5);
  static const Color muteBgInactive = Color(0xFFFADBD8);
  static const Color muteBorderActive = Color(0xFF58D68D);
  static const Color muteBorderInactive = Color(0xFFE74C3C);
  static const Color muteTextActive = Color(0xFF58D68D);
  static const Color muteTextInactive = Color(0xFFE74C3C);
  static const Color muteCheckbox = Color(0xFF58D68D);
  
  // Input field colors
  static const Color inputFieldBg = Color(0xFFF8F9FA);
  static const Color inputFieldBorder = Color(0xFFD5DBDB);
  
  // Status colors
  static const Color statusRecording = Color(0xFFE74C3C);
  static const Color statusLoading = Color(0xFFF39C12);
  static const Color statusPlaying = Color(0xFF58D68D);
  
  // Background colors - Dark theme
  static const Color appBackground = Color(0xFF1A1A1A);
  static const Color chatBackground = Color(0xFF2D2D2D);
  static const Color inputAreaBackground = Color(0xFF3A3A3A);
}

// Chat message model
class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? audioUrl;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.audioUrl,
  });
}

void main() {
  runApp(const VoiceApp());
}

class VoiceApp extends StatelessWidget {
  const VoiceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice AI Assistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const VoiceHomePage(),
    );
  }
}

class VoiceHomePage extends StatefulWidget {
  const VoiceHomePage({super.key});

  @override
  State<VoiceHomePage> createState() => _VoiceHomePageState();
}

class _VoiceHomePageState extends State<VoiceHomePage> {
  final AudioRecorder _recorder = AudioRecorder();
  final AudioPlayer _player = AudioPlayer();
  final ScrollController _scrollController = ScrollController();
  final TextEditingController _textController = TextEditingController();
  
  bool _isRecording = false;
  bool _isPlaying = false;
  bool _isLoading = false;
  bool _isMuted = false;
  html.MediaRecorder? _mediaRecorder;
  
  // Chat messages list
  List<ChatMessage> _messages = [];
  
  // Current session ID for conversation continuity
  String? _currentSessionId;
  
  // Vector database context for current conversation
  List<Map<String, String>> _vectorContext = [];
  
  // Debug panel
  bool _showDebugPanel = false;
  List<String> _debugLogs = [];
  
  // Voice streaming
  bool _isVoiceStreaming = false;
  String _currentTranscription = '';
  Timer? _transcriptionTimer;
  
  // Sentence-by-sentence TTS
  String _lastSpokenText = '';
  List<String> _spokenSentences = [];

  // TTS Queue system
  List<String> _ttsQueue = [];
  bool _isSpeaking = false;

  @override
  void dispose() {
    _recorder.dispose();
    _player.dispose();
    _scrollController.dispose();
    _textController.dispose();
    super.dispose();
  }
  
  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }
  
  void _addDebugLog(String message) {
    final timestamp = DateTime.now().toString().substring(11, 19);
    final logEntry = '[$timestamp] $message';
    setState(() {
      _debugLogs.add(logEntry);
      // Keep only last 200 logs
      if (_debugLogs.length > 200) {
        _debugLogs.removeAt(0);
      }
    });
    print('🐛 DEBUG: $logEntry');
    developer.log(logEntry, name: 'VoiceApp');
  }

  void _copyLogsToClipboard() {
    final allLogs = _debugLogs.join('\n');
    html.window.navigator.clipboard?.writeText(allLogs);
    _addDebugLog('📋 Logs copied to clipboard!');
  }

  /// Checks if text contains sentence-ending punctuation
  bool _hasSentenceEnding(String text) {
    return text.contains('.') || text.contains('!') || text.contains('?');
  }

  /// Extracts complete sentences from text
  List<String> _extractCompleteSentences(String text) {
    final sentences = <String>[];
    
    _addDebugLog('🔍 Extracting sentences from: "${text.substring(0, text.length > 100 ? 100 : text.length)}..."');
    
    // Use regex to find all complete sentences with punctuation
    final sentenceRegex = RegExp(r'[^.!?]*[.!?]+');
    final matches = sentenceRegex.allMatches(text);
    
    _addDebugLog('🎯 Regex found ${matches.length} matches');
    
    for (final match in matches) {
      final sentence = match.group(0)?.trim();
      if (sentence != null && sentence.isNotEmpty) {
        sentences.add(sentence);
        _addDebugLog('✅ Added sentence: "$sentence"');
      }
    }
    
    _addDebugLog('📋 Final sentences: $sentences');
    return sentences;
  }

  /// Processes voice streaming - sends complete sentences automatically
  void _processVoiceStreaming(String newTranscription) {
    if (!_isVoiceStreaming) return;
    
    _currentTranscription = newTranscription;
    
    // Check if we have complete sentences
    if (_hasSentenceEnding(newTranscription)) {
      final sentences = _extractCompleteSentences(newTranscription);
      
      for (final sentence in sentences) {
        if (sentence.trim().isNotEmpty) {
          _addDebugLog('🎤 Auto-sending sentence: "$sentence"');
          _sendToAI(sentence.trim());
        }
      }
      
      // Update current transcription to remaining text
      final lastSentenceEnd = newTranscription.lastIndexOf(RegExp(r'[.!?]')) + 1;
      if (lastSentenceEnd < newTranscription.length) {
        _currentTranscription = newTranscription.substring(lastSentenceEnd).trim();
      } else {
        _currentTranscription = '';
      }
    }
  }

  /// Processes sentence-by-sentence TTS during streaming
  void _processSentenceTTS(String fullText) {
    if (_isMuted) return;
    
    _addDebugLog('🔍 Processing TTS for text: "${fullText.length} chars"');
    
    // Extract complete sentences from the full text
    final sentences = _extractCompleteSentences(fullText);
    _addDebugLog('📝 Found ${sentences.length} sentences: $sentences');
    
    // Find new sentences that haven't been spoken yet
    for (final sentence in sentences) {
      if (!_spokenSentences.contains(sentence)) {
        _spokenSentences.add(sentence);
        _addDebugLog('🔊 Queueing sentence: "$sentence"');
        
        // Add to TTS queue instead of speaking immediately
        _addToTTSQueue(sentence);
      } else {
        _addDebugLog('⏭️ Skipping already spoken: "$sentence"');
      }
    }
  }

  /// Adds sentence to TTS queue and starts processing if not already speaking
  void _addToTTSQueue(String sentence) {
    _ttsQueue.add(sentence);
    _addDebugLog('📋 TTS Queue: ${_ttsQueue.length} sentences');
    
    // Start processing queue if not already speaking
    if (!_isSpeaking) {
      _processTTSQueue();
    }
  }

  /// Processes TTS queue sequentially
  Future<void> _processTTSQueue() async {
    if (_isSpeaking || _ttsQueue.isEmpty) return;
    
    _isSpeaking = true;
    _addDebugLog('🎤 Starting TTS queue processing');
    
    while (_ttsQueue.isNotEmpty) {
      final sentence = _ttsQueue.removeAt(0);
      _addDebugLog('🔊 Speaking: "$sentence"');
      
      try {
        // Stop any currently playing audio before starting new sentence
        if (_isPlaying) {
          await _player.stop();
          _isPlaying = false;
          _addDebugLog('⏹️ Stopped previous audio');
        }
        
        await _synthesizeSpeech(sentence);
        _addDebugLog('✅ Finished speaking: "$sentence"');
      } catch (e) {
        _addDebugLog('❌ TTS Error: $e');
      }
      
      // Small delay between sentences for natural flow
      await Future.delayed(Duration(milliseconds: 200));
    }
    
    _isSpeaking = false;
    _addDebugLog('🏁 TTS queue processing completed');
  }

  /// Clears TTS queue and stops current speech
  void _clearTTSQueue() {
    _ttsQueue.clear();
    _isSpeaking = false;
    
    // Stop any currently playing audio
    if (_isPlaying) {
      _player.stop();
      _isPlaying = false;
      _addDebugLog('⏹️ Stopped audio when clearing queue');
    }
    
    _addDebugLog('🧹 TTS queue cleared');
  }

  /// Builds conversation context from last 3 interactions (6 messages: 3 user + 3 AI)
  List<Map<String, String>> _buildConversationContext() {
    List<Map<String, String>> context = [];
    
    // Get last 6 messages (3 interactions)
    final recentMessages = _messages.length > 6 
        ? _messages.sublist(_messages.length - 6)
        : _messages;
    
    for (final message in recentMessages) {
      context.add({
        'role': message.isUser ? 'user' : 'assistant',
        'content': message.text,
        'timestamp': message.timestamp.toIso8601String(),
      });
    }
    
    return context;
  }

  /// Loads vector database context for the conversation
  Future<void> _loadVectorContext(String query) async {
    try {
      print('🔍 Loading vector context for query: $query');
      
      final response = await http.post(
        ApiConfig.getUri(ApiConfig.vectorSearch),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'query': query}),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final vectorResults = data['results'] as List<dynamic>? ?? [];
        
        _vectorContext = vectorResults.map((result) => {
          'content': result['content']?.toString() ?? '',
          'source': result['source']?.toString() ?? '',
          'score': result['score']?.toString() ?? '0.0',
        }).toList();
        
        print('📚 Loaded ${_vectorContext.length} vector results');
      } else {
        print('⚠️ Vector search failed: ${response.statusCode}');
        _vectorContext = [];
      }
    } catch (e) {
      print('❌ Vector context error: $e');
      _vectorContext = [];
    }
  }

  /// Gets knowledge base statistics using application services
  Future<Map<String, dynamic>?> _getKnowledgeStats() async {
    try {
      print('📊 Getting knowledge base statistics...');
      
      final response = await http.get(
        ApiConfig.getUri(ApiConfig.knowledgeStats),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('📊 Knowledge stats: ${data['stats']}');
        return data['stats'];
      } else {
        print('⚠️ Knowledge stats failed: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Knowledge stats error: $e');
      return null;
    }
  }

  /// Gets service capabilities using application services
  Future<Map<String, dynamic>?> _getServiceCapabilities() async {
    try {
      print('🔧 Getting service capabilities...');
      
      final response = await http.get(
        ApiConfig.getUri(ApiConfig.capabilities),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('🔧 Service capabilities: ${data['capabilities']}');
        return data['capabilities'];
      } else {
        print('⚠️ Service capabilities failed: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Service capabilities error: $e');
      return null;
    }
  }
  
  Future<void> _sendTextMessage() async {
    final text = _textController.text.trim();
    if (text.isEmpty || _isLoading) return;
    
    // Clear text field
    _textController.clear();
    
    // Send to AI

    
    await _sendToAI(text);
  }
  
  void _toggleMute() {
    setState(() {
      _isMuted = !_isMuted;
    });
    
    if (_isPlaying) {
      if (_isMuted) {
        _player.pause();
      } else {
        _player.resume();
      }
    }
  }

  Future<void> _startRecording() async {
    developer.log('🎤 Starting Web Audio recording...', name: 'VoiceApp');
    try {
      // Get user media
      final stream = await html.window.navigator.mediaDevices!.getUserMedia({'audio': true});
      final mediaRecorder = html.MediaRecorder(stream);
      
      // Store chunks
      final chunks = <html.Blob>[];
      
      // Use addEventListener for Web Audio API
      mediaRecorder.addEventListener('dataavailable', (event) {
        final dataEvent = event as html.BlobEvent;
        if (dataEvent.data != null) {
          chunks.add(dataEvent.data!);
        }
      });
      
      mediaRecorder.addEventListener('stop', (event) async {
        // Combine chunks into single blob
        final blob = html.Blob(chunks);
        
        // Convert blob to bytes
        final reader = html.FileReader();
        reader.readAsArrayBuffer(blob);
        
        reader.addEventListener('loadend', (event) async {
          final bytes = reader.result as List<int>;
          developer.log('✅ Recorded ${bytes.length} bytes', name: 'VoiceApp');
          
          // Send to Whisper API
          await _transcribeAudioBytes(bytes);
        });
      });
      
      // Start recording
      mediaRecorder.start();
      
      setState(() {
        _isRecording = true;
        _mediaRecorder = mediaRecorder;
      });
      
      developer.log('🎤 Started Web Audio recording', name: 'VoiceApp');
    } catch (e) {
      developer.log('❌ Recording error: $e', name: 'VoiceApp');
    }
  }

  Future<void> _stopRecording() async {
    developer.log('🛑 Stopping Web Audio recording...', name: 'VoiceApp');
    try {
      if (_mediaRecorder != null) {
        _mediaRecorder!.stop();
        setState(() {
          _isRecording = false;
        });
        developer.log('🛑 Stopped Web Audio recording', name: 'VoiceApp');
      }
    } catch (e) {
      developer.log('❌ Error stopping recording: $e', name: 'VoiceApp');
    }
  }

  Future<void> _transcribeAudioBytes(List<int> audioBytes) async {
    developer.log('🔄 Starting transcription for ${audioBytes.length} bytes', name: 'VoiceApp');
    setState(() {
      _isLoading = true;
    });

    try {
      developer.log('📤 Sending audio to Whisper API...', name: 'VoiceApp');
      // Send to our Whisper API
      final request = http.MultipartRequest(
        'POST',
        ApiConfig.getUri(ApiConfig.transcribe),
      );
      
      request.files.add(http.MultipartFile.fromBytes(
        'audio',
        audioBytes,
        filename: 'recording.wav',
      ));
      request.fields['language'] = 'pl';
      
      final response = await request.send();
      developer.log('📥 Received response from Whisper API: ${response.statusCode}', name: 'VoiceApp');
      final responseBody = await response.stream.bytesToString();
      final data = json.decode(responseBody);
      
      developer.log('📝 Whisper response: $data', name: 'VoiceApp');
      
      if (data['status'] == 'ok') {
        developer.log('✅ Transcription successful: ${data['transcript']}', name: 'VoiceApp');
        
        // Send transcript to AI (or fallback if empty)
        final transcript = data['transcript']?.toString().trim();
        if (transcript != null && transcript.isNotEmpty) {
          if (_isVoiceStreaming) {
            // Voice streaming mode - process for sentence detection
            _processVoiceStreaming(transcript);
          } else {
            // Normal mode - send entire transcript
            await _sendToAI(transcript);
          }
        } else {
          print('⚠️ Empty transcript, sending fallback message');
          await _sendToAI('Test message from Flutter - empty transcript');
        }
      } else {
        developer.log('❌ Transcription failed: ${data['message']}', name: 'VoiceApp');
        
        // Send error message to AI anyway for testing
        await _sendToAI('Test message from Flutter');
      }
      
    } catch (e) {
      developer.log('❌ Transcription error: $e', name: 'VoiceApp');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _transcribeAudio(String audioPath) async {
    developer.log('🔄 Starting transcription for: $audioPath', name: 'VoiceApp');
    setState(() {
      _isLoading = true;
    });

    try {
      // For Flutter Web, we need to use the recorded audio data
      // The record package should have saved the audio to a file
      
      developer.log('📦 Reading recorded audio file...', name: 'VoiceApp');
      
      // For Flutter Web, we need to get the recorded audio from the record package
      developer.log('🌐 Flutter Web - getting recorded audio...', name: 'VoiceApp');
      
      // The record package should have saved the audio
      // We need to get the audio data and send it to our Whisper API
      
      // For now, let's create a simple test audio file
      // In a real implementation, we would get the actual recorded audio
      final testAudioBytes = Uint8List.fromList([
        0x52, 0x49, 0x46, 0x46, // RIFF header
        0x24, 0x00, 0x00, 0x00, // File size
        0x57, 0x41, 0x56, 0x45, // WAVE
        0x66, 0x6D, 0x74, 0x20, // fmt
        0x10, 0x00, 0x00, 0x00, // fmt chunk size
        0x01, 0x00, // Audio format (PCM)
        0x01, 0x00, // Number of channels
        0x44, 0xAC, 0x00, 0x00, // Sample rate
        0x88, 0x58, 0x01, 0x00, // Byte rate
        0x02, 0x00, // Block align
        0x10, 0x00, // Bits per sample
        0x64, 0x61, 0x74, 0x61, // data
        0x00, 0x00, 0x00, 0x00, // data size
      ]);
      
      developer.log('📤 Sending audio to Whisper API...', name: 'VoiceApp');
      // Send to our Whisper API
      final request = http.MultipartRequest(
        'POST',
        ApiConfig.getUri(ApiConfig.transcribe),
      );
      
      request.files.add(http.MultipartFile.fromBytes(
        'audio',
        testAudioBytes,
        filename: 'recording.wav',
      ));
      request.fields['language'] = 'pl';
      
      final response = await request.send();
      developer.log('📥 Received response from Whisper API: ${response.statusCode}', name: 'VoiceApp');
      final responseBody = await response.stream.bytesToString();
      final data = json.decode(responseBody);
      
      developer.log('📝 Whisper response: $data', name: 'VoiceApp');
      
      if (data['status'] == 'ok') {
        developer.log('✅ Transcription successful: ${data['transcript']}', name: 'VoiceApp');
        
        // Send transcript to AI (or fallback if empty)
        final transcript = data['transcript']?.toString().trim();
        if (transcript != null && transcript.isNotEmpty) {
          if (_isVoiceStreaming) {
            // Voice streaming mode - process for sentence detection
            _processVoiceStreaming(transcript);
          } else {
            // Normal mode - send entire transcript
            await _sendToAI(transcript);
          }
        } else {
          print('⚠️ Empty transcript, sending fallback message');
          await _sendToAI('Test message from Flutter - empty transcript');
        }
      } else {
        developer.log('❌ Transcription failed: ${data['message']}', name: 'VoiceApp');
        
        // Send error message to AI anyway for testing
        await _sendToAI('Test message from Flutter');
      }
      
    } catch (e) {
      developer.log('❌ Transcription error: $e', name: 'VoiceApp');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _sendToAI(String text) async {
    if (text.isEmpty) return;
    
    _addDebugLog('🚀 Starting AI streaming request: "$text"');
    
    // Clear spoken sentences and TTS queue for new conversation
    _spokenSentences.clear();
    _clearTTSQueue();
    
    // Add user message to chat
    setState(() {
      _messages.add(ChatMessage(
        text: text,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _isLoading = true;
    });
    
    // Scroll to bottom
    _scrollToBottom();
    
    print('💬 Sending text to AI via SSE: $text');
    developer.log('💬 Sending text to AI via SSE: $text', name: 'VoiceApp');
    
    try {
      _addDebugLog('📤 Starting SSE connection to: ${ApiConfig.messageStream}');
      
      // Create AI message placeholder for streaming
      ChatMessage? aiMessage;
      String fullResponse = '';
      
      final request = http.Request('POST', ApiConfig.getUri(ApiConfig.messageStream));
      request.headers.addAll({
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
        'Cache-Control': 'no-cache',
      });
      final requestBody = <String, dynamic>{
        'message': text,
      };
      
      // Add session_id if we have one (for conversation continuity)
      if (_currentSessionId != null) {
        requestBody['session_id'] = _currentSessionId;
        _addDebugLog('📤 Sending with session_id: $_currentSessionId');
      } else {
        _addDebugLog('📤 Sending without session_id (will create new session)');
      }
      
      request.body = json.encode(requestBody);
      
      final streamedResponse = await request.send();
      _addDebugLog('📥 SSE Response: ${streamedResponse.statusCode}');
      
      if (streamedResponse.statusCode == 200) {
        await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
          final lines = chunk.split('\n');
          for (final line in lines) {
            if (line.startsWith('data: ')) {
              try {
                final data = json.decode(line.substring(6));
                
                // Loguj tylko typy inne niż 'chunk' (chunk jest za częsty)
                if (data['type'] != 'chunk') {
                  _addDebugLog('📨 SSE Data: ${data['type']}');
                }
                
                switch (data['type']) {
                  case 'session':
                    _currentSessionId = data['session_id'];
                    _addDebugLog('📝 Session ID saved: $_currentSessionId');
                    break;
                    
                  case 'status':
                    final statusMessage = data['message'] ?? '';
                    // Wyświetlaj logi RAG, ukryj logi o dźwiękach
                    if (statusMessage.contains('RAG') || 
                        statusMessage.contains('Dynamic') ||
                        statusMessage.contains('Znaleziono') ||
                        statusMessage.contains('wektor')) {
                      _addDebugLog('📚 RAG: ${data['message']}');
                    } else if (!statusMessage.contains('dźwięk') && 
                               !statusMessage.contains('audio') &&
                               !statusMessage.contains('TTS') &&
                               !statusMessage.contains('speech')) {
                      _addDebugLog('ℹ️ Status: ${data['message']}');
                    }
                    break;
                    
                  case 'chunk':
                    final content = data['content'] ?? '';
                    fullResponse += content;
                    
                    // Create or update AI message
                    if (aiMessage == null) {
                      aiMessage = ChatMessage(
                        text: content,
                        isUser: false,
                        timestamp: DateTime.now(),
                      );
                      setState(() {
                        _messages.add(aiMessage!);
                      });
                    } else {
                      // Replace the last AI message with updated content
                      setState(() {
                        _messages.removeLast(); // Remove old message
                        aiMessage = ChatMessage(
                          text: fullResponse,
                          isUser: false,
                          timestamp: DateTime.now(),
                        );
                        _messages.add(aiMessage!);
                      });
                    }
                    
                    // Process TTS for each chunk (jak w oryginalnej wersji)
                    if (!_isMuted && content.trim().isNotEmpty) {
                      _processSentenceTTS(fullResponse);
                    }
                    
                    _scrollToBottom();
                    break;
                    
                  case 'done':
                    _addDebugLog('✅ Streaming completed');
                    // TTS is handled by queue during streaming
                    break;
                    
                  case 'error':
                    _addDebugLog('❌ SSE Error: ${data['error']}');
                    setState(() {
                      _messages.add(ChatMessage(
                        text: 'Error: ${data['error']}',
                        isUser: false,
                        timestamp: DateTime.now(),
                      ));
                    });
                    break;
                }
              } catch (e) {
                _addDebugLog('❌ JSON parse error: $e');
              }
            }
          }
        }
      } else {
        _addDebugLog('❌ SSE Error: ${streamedResponse.statusCode}');
        setState(() {
          _messages.add(ChatMessage(
            text: 'Error: ${streamedResponse.statusCode}',
            isUser: false,
            timestamp: DateTime.now(),
          ));
        });
      }
    } catch (e) {
      _addDebugLog('❌ SSE Exception: $e');
      print('❌ AI streaming error: $e');
      developer.log('❌ AI streaming error: $e', name: 'VoiceApp');
      setState(() {
        _messages.add(ChatMessage(
          text: 'Error: $e',
          isUser: false,
          timestamp: DateTime.now(),
        ));
      });
    } finally {
      _addDebugLog('🏁 Streaming completed, setting loading=false');
      setState(() {
        _isLoading = false;
      });
      _scrollToBottom();
    }
  }

  /// Removes code blocks and inline code from text for TTS
  String _removeCodeBlocks(String text) {
    String result = text;
    
    // Remove triple backtick code blocks (```...```)
    result = result.replaceAll(RegExp(r'```[\s\S]*?```'), '');
    
    // Remove single backtick inline code (`...`)
    result = result.replaceAll(RegExp(r'`[^`]+`'), '');
    
    return result.trim();
  }

  Future<void> _synthesizeSpeech(String text) async {
    // Usuń bloki kodu i tagi formatowania przed TTS
    final withoutCode = _removeCodeBlocks(text);
    final cleanText = TextFormatter.stripFormatting(withoutCode);
    
    // Jeśli po usunięciu kodu tekst jest pusty, nie mów nic
    if (cleanText.trim().isEmpty) {
      _addDebugLog('⏭️ Skipping empty text after removing code');
      return;
    }
    
    print('🔊 Synthesizing speech for: $cleanText');
    
    // Check if muted - if so, skip audio generation
    if (_isMuted) {
      print('🔇 Audio muted, skipping speech synthesis');
      return;
    }
    
    // ALWAYS stop any currently playing audio before starting new
    if (_isPlaying) {
      await _player.stop();
      _isPlaying = false;
      _addDebugLog('⏹️ Stopped previous audio before new TTS');
    }
    
    try {
      // For Flutter Web, use simple POST instead of MultipartRequest
      final response = await http.post(
        ApiConfig.getUri(ApiConfig.speak),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'text=${Uri.encodeComponent(cleanText)}&voice=pl-PL-default',
      );
      
      print('🎧 TTS response: ${response.statusCode} - ${response.body}');
      final data = json.decode(response.body);
      
      if (data['status'] == 'ok') {
        // Use ApiConfig to get proper audio URL (handles Docker proxy)
        final audioUrl = ApiConfig.getAudioUrl(data['audio_url'] ?? '');
        print('✅ TTS successful, playing audio from: $audioUrl');
        await _playAudio(audioUrl);
      } else {
        print('❌ TTS failed: ${data['message']}');
      }
    } catch (e) {
      print('❌ TTS error: $e');
    }
  }

  Future<void> _playAudio(String url) async {
    try {
      setState(() {
        _isPlaying = true;
      });
      
      // Convert relative URL to absolute URL for Flutter Web
      // In Docker, nginx proxy handles /static/* routing
      String audioUrl = url;
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        // Relative URL - construct absolute URL using current origin
        final origin = html.window.location.origin;
        audioUrl = '$origin$url';
      }
      
      _addDebugLog('🎵 Playing audio from: $audioUrl');
      await _player.play(UrlSource(audioUrl));
      
      // Wait for audio to complete
      await _player.onPlayerComplete.first;
      
      setState(() {
        _isPlaying = false;
      });
      
      _addDebugLog('🎵 Audio playback completed');
    } catch (e) {
      setState(() {
        _isPlaying = false;
      });
      _addDebugLog('❌ Audio playback error: $e');
      print('Error playing audio: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.appBackground,
      appBar: AppBar(
        title: const Text('🎤 Eliora - Asystentka AI'),
        backgroundColor: AppColors.aiAvatarBg,
        foregroundColor: AppColors.aiMessageText,
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(_showDebugPanel ? Icons.bug_report : Icons.bug_report_outlined),
            onPressed: () {
              setState(() {
                _showDebugPanel = !_showDebugPanel;
              });
              _addDebugLog(_showDebugPanel ? '🐛 Debug panel opened' : '🐛 Debug panel closed');
            },
            tooltip: _showDebugPanel ? 'Hide Debug Panel' : 'Show Debug Panel',
          ),
        ],
      ),
      body: Column(
        children: [
          // Chat messages area
          Expanded(
            child: Container(
              color: AppColors.chatBackground,
              child: _messages.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.chat_bubble_outline,
                            size: 80,
                            color: AppColors.aiMessageTimestamp,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Witaj! 👋\nNaciśnij mikrofon i zacznij rozmowę',
                            textAlign: TextAlign.center,
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                              color: AppColors.aiMessageText,
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      controller: _scrollController,
                      padding: const EdgeInsets.all(16),
                      itemCount: _messages.length + (_isLoading ? 1 : 0),
                      itemBuilder: (context, index) {
                        if (index == _messages.length && _isLoading) {
                          return _buildLoadingMessage();
                        }
                        return _buildMessageBubble(_messages[index]);
                      },
                    ),
            ),
          ),
          
          // Input area with text field and microphone button
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.inputAreaBackground,
              border: Border(
                top: BorderSide(color: AppColors.inputFieldBorder),
              ),
            ),
            child: Column(
              children: [
                // Status text
                if (_isRecording || _isLoading || _isPlaying)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: Text(
                      _isRecording ? '🎤 Nagrywanie...' : 
                      _isLoading ? '⚙️ Przetwarzanie...' :
                      _isPlaying ? '🔊 Odtwarzanie...' : '',
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: _isRecording ? AppColors.statusRecording : 
                               _isLoading ? AppColors.statusLoading :
                               _isPlaying ? AppColors.statusPlaying : AppColors.aiMessageTimestamp,
                      ),
                    ),
                  ),
                
                // Input row
                Row(
                  children: [
                    // Text input field
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          color: AppColors.inputFieldBg,
                          borderRadius: BorderRadius.circular(25),
                          border: Border.all(color: AppColors.inputFieldBorder),
                        ),
                        child: TextField(
                          controller: _textController,
                          enabled: !_isLoading,
                          decoration: const InputDecoration(
                            hintText: 'Napisz wiadomość...',
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 12,
                            ),
                          ),
                          maxLines: null,
                          textInputAction: TextInputAction.send,
                          onSubmitted: (_) => _sendTextMessage(),
                        ),
                      ),
                    ),
                    
                    const SizedBox(width: 8),
                    
                    // Send button
                    Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.1),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _sendTextMessage,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.sendButton,
                          foregroundColor: Colors.white,
                          shape: const CircleBorder(),
                          padding: const EdgeInsets.all(12),
                          elevation: 0,
                        ),
                        child: const Icon(Icons.send, size: 20),
                      ),
                    ),
                    
                    const SizedBox(width: 8),
                    
                    // Microphone button
                    Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.2),
                            blurRadius: 8,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : (_isRecording ? _stopRecording : _startRecording),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: _isRecording ? AppColors.micButtonRecording : AppColors.micButtonActive,
                          foregroundColor: Colors.white,
                          shape: const CircleBorder(),
                          padding: const EdgeInsets.all(12),
                          elevation: 0,
                        ),
                        child: Icon(
                          _isRecording ? Icons.stop : Icons.mic,
                          size: 20,
                        ),
                      ),
                    ),
                    
                    const SizedBox(width: 8),
                    
                    // Mute checkbox
                    Container(
                      decoration: BoxDecoration(
                        color: _isMuted ? AppColors.muteBgInactive : AppColors.muteBgActive,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: _isMuted ? AppColors.muteBorderInactive : AppColors.muteBorderActive,
                        ),
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Checkbox(
                            value: !_isMuted, // Inverted because we want "unmuted" to be checked
                            onChanged: _isLoading ? null : (_) => _toggleMute(),
                            activeColor: AppColors.muteCheckbox,
                          ),
                          Text(
                            _isMuted ? '🔇' : '🔊',
                            style: const TextStyle(fontSize: 16),
                          ),
                          Text(
                            _isMuted ? 'Wycisz' : 'Dźwięk',
                            style: TextStyle(
                              fontSize: 10,
                              color: _isMuted ? AppColors.muteTextInactive : AppColors.muteTextActive,
                            ),
                          ),
                        ],
                      ),
                    ),
                    
                    const SizedBox(width: 8),
                    
                    // TTS Queue indicator
                    Container(
                      decoration: BoxDecoration(
                        color: _ttsQueue.isNotEmpty ? AppColors.aiAvatarBg : AppColors.userMessageBg,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: _ttsQueue.isNotEmpty ? AppColors.aiMessageText : AppColors.userMessageText,
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              _isSpeaking ? Icons.volume_up : Icons.queue_music,
                              color: _ttsQueue.isNotEmpty ? AppColors.aiMessageText : AppColors.userMessageText,
                              size: 16,
                            ),
                            Text(
                              '${_ttsQueue.length}',
                              style: TextStyle(
                                fontSize: 10,
                                color: _ttsQueue.isNotEmpty ? AppColors.aiMessageText : AppColors.userMessageText,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    
                    const SizedBox(width: 8),
                    
                    // Voice Streaming toggle
                    Container(
                      decoration: BoxDecoration(
                        color: _isVoiceStreaming ? AppColors.aiAvatarBg : AppColors.userMessageBg,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: _isVoiceStreaming ? AppColors.aiMessageText : AppColors.userMessageText,
                        ),
                      ),
                      child: InkWell(
                        onTap: () {
                          setState(() {
                            _isVoiceStreaming = !_isVoiceStreaming;
                            if (!_isVoiceStreaming) {
                              _currentTranscription = '';
                              _transcriptionTimer?.cancel();
                            }
                          });
                          _addDebugLog(_isVoiceStreaming ? '🎤 Voice streaming ON' : '🎤 Voice streaming OFF');
                        },
                        borderRadius: BorderRadius.circular(8),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                _isVoiceStreaming ? Icons.stream : Icons.mic_none,
                                color: _isVoiceStreaming ? AppColors.aiMessageText : AppColors.userMessageText,
                                size: 16,
                              ),
                              Text(
                                _isVoiceStreaming ? 'Stream' : 'Normal',
                                style: TextStyle(
                                  fontSize: 10,
                                  color: _isVoiceStreaming ? AppColors.aiMessageText : AppColors.userMessageText,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    
                  ],
                ),
              ],
            ),
          ),
          
          // Debug Panel
          if (_showDebugPanel)
            Container(
              height: 200,
              decoration: BoxDecoration(
                color: Colors.black87,
                border: Border(
                  top: BorderSide(color: Colors.green, width: 2),
                ),
              ),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    color: Colors.green,
                    child: Row(
                      children: [
                        const Icon(Icons.bug_report, color: Colors.white, size: 16),
                        const SizedBox(width: 8),
                        const Text(
                          'Debug Logs',
                          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                        const Spacer(),
                        Text(
                          '${_debugLogs.length} logs',
                          style: const TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                        const SizedBox(width: 8),
                        IconButton(
                          icon: const Icon(Icons.copy, color: Colors.white, size: 16),
                          padding: EdgeInsets.zero,
                          constraints: const BoxConstraints(),
                          onPressed: _copyLogsToClipboard,
                          tooltip: 'Copy logs',
                        ),
                        IconButton(
                          icon: const Icon(Icons.clear, color: Colors.white, size: 16),
                          padding: EdgeInsets.zero,
                          constraints: const BoxConstraints(),
                          onPressed: () {
                            setState(() {
                              _debugLogs.clear();
                            });
                          },
                          tooltip: 'Clear logs',
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: _debugLogs.isEmpty
                        ? const Center(
                            child: Text(
                              'No debug logs yet...',
                              style: TextStyle(color: Colors.grey),
                            ),
                          )
                        : ListView.builder(
                            reverse: true,
                            itemCount: _debugLogs.length,
                            itemBuilder: (context, index) {
                              final log = _debugLogs[_debugLogs.length - 1 - index];
                              return Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                child: Text(
                                  log,
                                  style: const TextStyle(
                                    color: Colors.greenAccent,
                                    fontSize: 11,
                                    fontFamily: 'monospace',
                                  ),
                                ),
                              );
                            },
                          ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
  
  Widget _buildMessageBubble(ChatMessage message) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            CircleAvatar(
              backgroundColor: AppColors.aiAvatarBg,
              child: const Icon(Icons.smart_toy, color: AppColors.aiAvatarIcon),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: message.isUser ? AppColors.userMessageBg : AppColors.aiMessageBg,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  RichText(
                    text: message.isUser 
                        ? TextSpan(
                            text: message.text,
                            style: TextStyle(
                              color: AppColors.userMessageText,
                              fontSize: 16,
                            ),
                          )
                        : TextFormatter.formatText(
                            message.text,
                            defaultColor: AppColors.aiMessageText,
                            fontSize: 16,
                          ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${message.timestamp.hour.toString().padLeft(2, '0')}:${message.timestamp.minute.toString().padLeft(2, '0')}',
                    style: TextStyle(
                      color: message.isUser ? AppColors.userMessageTimestamp : AppColors.aiMessageTimestamp,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ),
          if (message.isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: AppColors.userAvatarBg,
              child: const Icon(Icons.person, color: AppColors.userAvatarIcon),
            ),
          ],
        ],
      ),
    );
  }
  
  Widget _buildLoadingMessage() {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: Colors.blue[100],
            child: const Icon(Icons.smart_toy, color: Colors.blue),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.grey[200],
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                const SizedBox(width: 8),
                Text(
                  'AI myśli...',
                  style: TextStyle(color: Colors.grey[600]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}