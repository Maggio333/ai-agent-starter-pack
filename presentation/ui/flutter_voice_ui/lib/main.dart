import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:developer' as developer;
import 'dart:html' as html;

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
  
  bool _isRecording = false;
  bool _isPlaying = false;
  String _transcript = '';
  String _aiResponse = '';
  bool _isLoading = false;
  html.MediaRecorder? _mediaRecorder;

  @override
  void dispose() {
    _recorder.dispose();
    _player.dispose();
    super.dispose();
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
        _transcript = '';
        _aiResponse = '';
      });
      
      developer.log('🎤 Started Web Audio recording', name: 'VoiceApp');
    } catch (e) {
      developer.log('❌ Recording error: $e', name: 'VoiceApp');
      setState(() {
        _transcript = 'Error: $e';
      });
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
      setState(() {
        _transcript = 'Error stopping recording: $e';
      });
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
        Uri.parse('http://localhost:8080/api/voice/transcribe'),
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
        setState(() {
          _transcript = data['transcript'];
        });
        
        // Send transcript to AI (or fallback if empty)
        final transcript = data['transcript']?.toString().trim();
        if (transcript != null && transcript.isNotEmpty) {
          await _sendToAI(transcript);
        } else {
          print('⚠️ Empty transcript, sending fallback message');
          await _sendToAI('Test message from Flutter - empty transcript');
        }
      } else {
        developer.log('❌ Transcription failed: ${data['message']}', name: 'VoiceApp');
        setState(() {
          _transcript = 'Error: ${data['message']}';
        });
        
        // Send error message to AI anyway for testing
        await _sendToAI('Test message from Flutter');
      }
      
    } catch (e) {
      developer.log('❌ Transcription error: $e', name: 'VoiceApp');
      setState(() {
        _transcript = 'Error: $e';
      });
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
        Uri.parse('http://localhost:8080/api/voice/transcribe'),
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
        setState(() {
          _transcript = data['transcript'];
        });
        
        // Send transcript to AI (or fallback if empty)
        final transcript = data['transcript']?.toString().trim();
        if (transcript != null && transcript.isNotEmpty) {
          await _sendToAI(transcript);
        } else {
          print('⚠️ Empty transcript, sending fallback message');
          await _sendToAI('Test message from Flutter - empty transcript');
        }
      } else {
        developer.log('❌ Transcription failed: ${data['message']}', name: 'VoiceApp');
        setState(() {
          _transcript = 'Error: ${data['message']}';
        });
        
        // Send error message to AI anyway for testing
        await _sendToAI('Test message from Flutter');
      }
      
    } catch (e) {
      developer.log('❌ Transcription error: $e', name: 'VoiceApp');
      setState(() {
        _transcript = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _sendToAI(String text) async {
    print('💬 Sending text to AI: $text');
    developer.log('💬 Sending text to AI: $text', name: 'VoiceApp');
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8080/api/chat/send'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'message': text}),
      );
      
      print('🤖 Received response from AI: ${response.statusCode}');
      print('🤖 Response body: ${response.body}');
      developer.log('🤖 Received response from AI: ${response.statusCode}', name: 'VoiceApp');
      developer.log('🤖 Response body: ${response.body}', name: 'VoiceApp');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ AI response data: $data');
        developer.log('✅ AI response data: $data', name: 'VoiceApp');
        setState(() {
          _aiResponse = data['response'] ?? 'No response';
        });
        
        // Convert AI response to speech
        await _synthesizeSpeech(data['response'] ?? 'No response');
      } else {
        print('❌ AI response failed: ${response.statusCode} - ${response.body}');
        developer.log('❌ AI response failed: ${response.statusCode} - ${response.body}', name: 'VoiceApp');
        setState(() {
          _aiResponse = 'Error: ${response.statusCode} - ${response.body}';
        });
      }
    } catch (e) {
      print('❌ AI communication error: $e');
      developer.log('❌ AI communication error: $e', name: 'VoiceApp');
    setState(() {
        _aiResponse = 'Error: $e';
      });
    }
  }

  Future<void> _synthesizeSpeech(String text) async {
    print('🔊 Synthesizing speech for: $text');
    try {
      // For Flutter Web, use simple POST instead of MultipartRequest
      final response = await http.post(
        Uri.parse('http://localhost:8080/api/voice/speak'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'text=${Uri.encodeComponent(text)}&voice=pl-PL-default',
      );
      
      print('🎧 TTS response: ${response.statusCode} - ${response.body}');
      final data = json.decode(response.body);
      
      if (data['status'] == 'ok') {
        print('✅ TTS successful, playing audio from: http://localhost:8080${data['audio_url']}');
        await _playAudio('http://localhost:8080${data['audio_url']}');
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
      
      await _player.play(UrlSource(url));
      
      _player.onPlayerComplete.listen((_) {
        setState(() {
          _isPlaying = false;
        });
      });
    } catch (e) {
      setState(() {
        _isPlaying = false;
      });
      print('Error playing audio: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Voice AI Assistant'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Table(
          children: [
            // Row 1: Recording Button (centered)
            TableRow(
              children: [
                Container(
                  height: 100,
                  child: Center(
                    child: ElevatedButton(
                      onPressed: _isRecording ? _stopRecording : _startRecording,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _isRecording ? Colors.red : Colors.blue,
                        foregroundColor: Colors.white,
                        shape: const CircleBorder(),
                        padding: const EdgeInsets.all(20),
                        elevation: 8,
                      ),
                      child: Icon(
                        _isRecording ? Icons.stop : Icons.mic,
                        size: 30,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            
            // Row 2: Status Text
            TableRow(
              children: [
                Container(
                  height: 60,
                  padding: const EdgeInsets.all(10),
                  child: Center(
                    child: Text(
                      _isRecording ? '🎤 Nagrywanie... Naciśnij aby zatrzymać' : 
                      _isLoading ? '⚙️ Przetwarzanie...' :
                      _isPlaying ? '🔊 Odtwarzanie...' :
                      '🎤 Naciśnij aby rozpocząć nagrywanie',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: _isRecording ? Colors.red : 
                               _isLoading ? Colors.orange :
                               _isPlaying ? Colors.green : Colors.grey[700],
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ],
            ),
            
            // Row 2.5: Test Button
            TableRow(
              children: [
                Container(
                  height: 50,
                  padding: const EdgeInsets.all(10),
                  child: Center(
                    child: ElevatedButton.icon(
                      onPressed: _isLoading ? null : () async {
                        setState(() {
                          _transcript = 'Test: Witaj! To jest testowy tekst do konwersji na mowę.';
                        });
                        await _sendToAI(_transcript);
                      },
                      icon: const Icon(Icons.play_arrow),
                      label: const Text('🧪 Test STT → AI → TTS'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            
            // Row 3: Spacer
            TableRow(
              children: [
                Container(height: 20),
              ],
            ),
            
            // Row 4: Transcript (if exists)
            if (_transcript.isNotEmpty)
              TableRow(
                children: [
                  Container(
                    height: 120,
                    padding: const EdgeInsets.all(16.0),
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.grey[300]!),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '📝 Transkrypcja:',
                          style: Theme.of(context).textTheme.titleSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Expanded(
                          child: SingleChildScrollView(
                            child: Text(_transcript),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            
            // Row 5: AI Response (if exists)
            if (_aiResponse.isNotEmpty)
              TableRow(
                children: [
                  Container(
                    height: 120,
                    padding: const EdgeInsets.all(16.0),
                    decoration: BoxDecoration(
                      color: Colors.blue[50],
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.blue[200]!),
                    ),
        child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
            Text(
                          '🤖 Odpowiedź AI:',
                          style: Theme.of(context).textTheme.titleSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Expanded(
                          child: SingleChildScrollView(
                            child: Text(_aiResponse),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            
            // Row 6: Loading Indicator (if loading)
            if (_isLoading)
              TableRow(
                children: [
                  Container(
                    height: 60,
                    child: const Center(
                      child: CircularProgressIndicator(),
                    ),
                  ),
                ],
            ),
          ],
        ),
      ),
    );
  }
}