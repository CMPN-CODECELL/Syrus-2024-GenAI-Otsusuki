import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class XrayImageVersionsRecord extends FirestoreRecord {
  XrayImageVersionsRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "XrayImageVersion" field.
  int? _xrayImageVersion;
  int get xrayImageVersion => _xrayImageVersion ?? 0;
  bool hasXrayImageVersion() => _xrayImageVersion != null;

  // "FrontAndSideReference" field.
  DocumentReference? _frontAndSideReference;
  DocumentReference? get frontAndSideReference => _frontAndSideReference;
  bool hasFrontAndSideReference() => _frontAndSideReference != null;

  void _initializeFields() {
    _xrayImageVersion = castToType<int>(snapshotData['XrayImageVersion']);
    _frontAndSideReference =
        snapshotData['FrontAndSideReference'] as DocumentReference?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('XrayImageVersions');

  static Stream<XrayImageVersionsRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => XrayImageVersionsRecord.fromSnapshot(s));

  static Future<XrayImageVersionsRecord> getDocumentOnce(
          DocumentReference ref) =>
      ref.get().then((s) => XrayImageVersionsRecord.fromSnapshot(s));

  static XrayImageVersionsRecord fromSnapshot(DocumentSnapshot snapshot) =>
      XrayImageVersionsRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static XrayImageVersionsRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      XrayImageVersionsRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'XrayImageVersionsRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is XrayImageVersionsRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createXrayImageVersionsRecordData({
  int? xrayImageVersion,
  DocumentReference? frontAndSideReference,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'XrayImageVersion': xrayImageVersion,
      'FrontAndSideReference': frontAndSideReference,
    }.withoutNulls,
  );

  return firestoreData;
}

class XrayImageVersionsRecordDocumentEquality
    implements Equality<XrayImageVersionsRecord> {
  const XrayImageVersionsRecordDocumentEquality();

  @override
  bool equals(XrayImageVersionsRecord? e1, XrayImageVersionsRecord? e2) {
    return e1?.xrayImageVersion == e2?.xrayImageVersion &&
        e1?.frontAndSideReference == e2?.frontAndSideReference;
  }

  @override
  int hash(XrayImageVersionsRecord? e) => const ListEquality()
      .hash([e?.xrayImageVersion, e?.frontAndSideReference]);

  @override
  bool isValidKey(Object? o) => o is XrayImageVersionsRecord;
}
