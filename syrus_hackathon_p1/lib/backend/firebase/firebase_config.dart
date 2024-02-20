import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyBi07TopptixmK59XcWyFnc8muohTaOZWE",
            authDomain: "syrus-hackathon-p1-wmbglw.firebaseapp.com",
            projectId: "syrus-hackathon-p1-wmbglw",
            storageBucket: "syrus-hackathon-p1-wmbglw.appspot.com",
            messagingSenderId: "321874139966",
            appId: "1:321874139966:web:09105d2aca6a7cda6c2a6f"));
  } else {
    await Firebase.initializeApp();
  }
}
