import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class XrayImagesRecord extends FirestoreRecord {
  XrayImagesRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "FrontXrayImage" field.
  String? _frontXrayImage;
  String get frontXrayImage => _frontXrayImage ?? '';
  bool hasFrontXrayImage() => _frontXrayImage != null;

  // "SideXrayImage" field.
  String? _sideXrayImage;
  String get sideXrayImage => _sideXrayImage ?? '';
  bool hasSideXrayImage() => _sideXrayImage != null;

  // "PatientsReference" field.
  DocumentReference? _patientsReference;
  DocumentReference? get patientsReference => _patientsReference;
  bool hasPatientsReference() => _patientsReference != null;

  void _initializeFields() {
    _frontXrayImage = snapshotData['FrontXrayImage'] as String?;
    _sideXrayImage = snapshotData['SideXrayImage'] as String?;
    _patientsReference =
        snapshotData['PatientsReference'] as DocumentReference?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('XrayImages');

  static Stream<XrayImagesRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => XrayImagesRecord.fromSnapshot(s));

  static Future<XrayImagesRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => XrayImagesRecord.fromSnapshot(s));

  static XrayImagesRecord fromSnapshot(DocumentSnapshot snapshot) =>
      XrayImagesRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static XrayImagesRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      XrayImagesRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'XrayImagesRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is XrayImagesRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createXrayImagesRecordData({
  String? frontXrayImage,
  String? sideXrayImage,
  DocumentReference? patientsReference,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'FrontXrayImage': frontXrayImage,
      'SideXrayImage': sideXrayImage,
      'PatientsReference': patientsReference,
    }.withoutNulls,
  );

  return firestoreData;
}

class XrayImagesRecordDocumentEquality implements Equality<XrayImagesRecord> {
  const XrayImagesRecordDocumentEquality();

  @override
  bool equals(XrayImagesRecord? e1, XrayImagesRecord? e2) {
    return e1?.frontXrayImage == e2?.frontXrayImage &&
        e1?.sideXrayImage == e2?.sideXrayImage &&
        e1?.patientsReference == e2?.patientsReference;
  }

  @override
  int hash(XrayImagesRecord? e) => const ListEquality()
      .hash([e?.frontXrayImage, e?.sideXrayImage, e?.patientsReference]);

  @override
  bool isValidKey(Object? o) => o is XrayImagesRecord;
}
