import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class PatientsInfoRecord extends FirestoreRecord {
  PatientsInfoRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "PatientsName" field.
  String? _patientsName;
  String get patientsName => _patientsName ?? '';
  bool hasPatientsName() => _patientsName != null;

  // "PatientsAge" field.
  int? _patientsAge;
  int get patientsAge => _patientsAge ?? 0;
  bool hasPatientsAge() => _patientsAge != null;

  // "PatientsHeight" field.
  String? _patientsHeight;
  String get patientsHeight => _patientsHeight ?? '';
  bool hasPatientsHeight() => _patientsHeight != null;

  // "PatientsWeight" field.
  String? _patientsWeight;
  String get patientsWeight => _patientsWeight ?? '';
  bool hasPatientsWeight() => _patientsWeight != null;

  // "PatientsSex" field.
  String? _patientsSex;
  String get patientsSex => _patientsSex ?? '';
  bool hasPatientsSex() => _patientsSex != null;

  // "PatientsEmail" field.
  String? _patientsEmail;
  String get patientsEmail => _patientsEmail ?? '';
  bool hasPatientsEmail() => _patientsEmail != null;

  // "PatientsPhone" field.
  String? _patientsPhone;
  String get patientsPhone => _patientsPhone ?? '';
  bool hasPatientsPhone() => _patientsPhone != null;

  // "PatientDescription" field.
  String? _patientDescription;
  String get patientDescription => _patientDescription ?? '';
  bool hasPatientDescription() => _patientDescription != null;

  // "UsersReference" field.
  DocumentReference? _usersReference;
  DocumentReference? get usersReference => _usersReference;
  bool hasUsersReference() => _usersReference != null;

  void _initializeFields() {
    _patientsName = snapshotData['PatientsName'] as String?;
    _patientsAge = castToType<int>(snapshotData['PatientsAge']);
    _patientsHeight = snapshotData['PatientsHeight'] as String?;
    _patientsWeight = snapshotData['PatientsWeight'] as String?;
    _patientsSex = snapshotData['PatientsSex'] as String?;
    _patientsEmail = snapshotData['PatientsEmail'] as String?;
    _patientsPhone = snapshotData['PatientsPhone'] as String?;
    _patientDescription = snapshotData['PatientDescription'] as String?;
    _usersReference = snapshotData['UsersReference'] as DocumentReference?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('patientsInfo');

  static Stream<PatientsInfoRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => PatientsInfoRecord.fromSnapshot(s));

  static Future<PatientsInfoRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => PatientsInfoRecord.fromSnapshot(s));

  static PatientsInfoRecord fromSnapshot(DocumentSnapshot snapshot) =>
      PatientsInfoRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static PatientsInfoRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      PatientsInfoRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'PatientsInfoRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is PatientsInfoRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createPatientsInfoRecordData({
  String? patientsName,
  int? patientsAge,
  String? patientsHeight,
  String? patientsWeight,
  String? patientsSex,
  String? patientsEmail,
  String? patientsPhone,
  String? patientDescription,
  DocumentReference? usersReference,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'PatientsName': patientsName,
      'PatientsAge': patientsAge,
      'PatientsHeight': patientsHeight,
      'PatientsWeight': patientsWeight,
      'PatientsSex': patientsSex,
      'PatientsEmail': patientsEmail,
      'PatientsPhone': patientsPhone,
      'PatientDescription': patientDescription,
      'UsersReference': usersReference,
    }.withoutNulls,
  );

  return firestoreData;
}

class PatientsInfoRecordDocumentEquality
    implements Equality<PatientsInfoRecord> {
  const PatientsInfoRecordDocumentEquality();

  @override
  bool equals(PatientsInfoRecord? e1, PatientsInfoRecord? e2) {
    return e1?.patientsName == e2?.patientsName &&
        e1?.patientsAge == e2?.patientsAge &&
        e1?.patientsHeight == e2?.patientsHeight &&
        e1?.patientsWeight == e2?.patientsWeight &&
        e1?.patientsSex == e2?.patientsSex &&
        e1?.patientsEmail == e2?.patientsEmail &&
        e1?.patientsPhone == e2?.patientsPhone &&
        e1?.patientDescription == e2?.patientDescription &&
        e1?.usersReference == e2?.usersReference;
  }

  @override
  int hash(PatientsInfoRecord? e) => const ListEquality().hash([
        e?.patientsName,
        e?.patientsAge,
        e?.patientsHeight,
        e?.patientsWeight,
        e?.patientsSex,
        e?.patientsEmail,
        e?.patientsPhone,
        e?.patientDescription,
        e?.usersReference
      ]);

  @override
  bool isValidKey(Object? o) => o is PatientsInfoRecord;
}
