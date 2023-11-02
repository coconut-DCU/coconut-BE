import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
// 
import 'package:http/http.dart' as http;

class CameraExample extends StatefulWidget {
  const CameraExample({Key? key}) : super(key: key);

  @override
  _CameraExampleState createState() => _CameraExampleState();
}

class _CameraExampleState extends State<CameraExample> {
  File? _image; //  이미지 파일을 저장할 변수
  final picker = ImagePicker();

  Future getImage(ImageSource imageSource) async {
    final image = await picker.pickImage(source: imageSource);  // 카메라 또는

    setState(() {
      _image = File(image!.path);  // 선택한 이미지로 변수 업데이트
    });

    // 선택한 이미지를 FastAPI 서버로 업로드
    uploadImage();
  }

  Future uploadImage() async {
    if (_image == null) {
      print('No image selected.');  // 이미지가 선택되지 않았을 경우 로그 출력
      return; 
    }

    final uri = Uri.parse('http://127.0.0.1:8000/upload');  // FastAPI 엔드포인트 URL
    final request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromPath('image', _image!.path));

    try {
      final response = await request.send();  // 이미지 업로드 시도

      if (response.statusCode == 200) {
        print('Image uploaded successfully');  // 성공적으로 업로드됐을 경우 로그 출력
      } else {
        print('Failed to upload image');  // 업로드 실패 시 로그 출력
      }
    } catch (e) {
      print('Error during image upload: $e');  // 업로드 중 에러 발생 시 로그 출력
    }
  }

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations(
        [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

    return Scaffold(
      backgroundColor: const Color(0xfff4f3f9),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(height: 100.0),  // Move the buttons a bit down
          Center(
            child: Image.asset(
              'assets/images/logo.png',  // Replace with your logo asset path
              width: 400.0,
              height: 400.0,
            ),
          ),
          SizedBox(height: 50.0),  // Add some space between logo and buttons
          ElevatedButton(
            onPressed: () {
              getImage(ImageSource.camera);
            },
            child: Text('사진 촬영'),
          ),
          SizedBox(height: 20.0),
          ElevatedButton(
            onPressed: () {
              getImage(ImageSource.gallery);
            },
            child: Text('갤러리 열기'),
          ),
        ],
      ),
    );
  }
}
