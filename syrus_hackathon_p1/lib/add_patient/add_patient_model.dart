import '/auth/firebase_auth/auth_util.dart';
import '/backend/backend.dart';
import '/flutter_flow/flutter_flow_drop_down.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import '/flutter_flow/form_field_controller.dart';
import 'add_patient_widget.dart' show AddPatientWidget;
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class AddPatientModel extends FlutterFlowModel<AddPatientWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for PatientName widget.
  FocusNode? patientNameFocusNode;
  TextEditingController? patientNameController;
  String? Function(BuildContext, String?)? patientNameControllerValidator;
  // State field(s) for PatientEmail widget.
  FocusNode? patientEmailFocusNode;
  TextEditingController? patientEmailController;
  String? Function(BuildContext, String?)? patientEmailControllerValidator;
  // State field(s) for PatientPhone widget.
  FocusNode? patientPhoneFocusNode;
  TextEditingController? patientPhoneController;
  String? Function(BuildContext, String?)? patientPhoneControllerValidator;
  // State field(s) for PatientAge widget.
  FocusNode? patientAgeFocusNode;
  TextEditingController? patientAgeController;
  String? Function(BuildContext, String?)? patientAgeControllerValidator;
  // State field(s) for PatientHeight widget.
  FocusNode? patientHeightFocusNode;
  TextEditingController? patientHeightController;
  String? Function(BuildContext, String?)? patientHeightControllerValidator;
  // State field(s) for PatientWeight widget.
  FocusNode? patientWeightFocusNode;
  TextEditingController? patientWeightController;
  String? Function(BuildContext, String?)? patientWeightControllerValidator;
  // State field(s) for DropDown widget.
  String? dropDownValue;
  FormFieldController<String>? dropDownValueController;
  // State field(s) for PatientDescription widget.
  FocusNode? patientDescriptionFocusNode;
  TextEditingController? patientDescriptionController;
  String? Function(BuildContext, String?)?
      patientDescriptionControllerValidator;

  /// Initialization and disposal methods.

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    patientNameFocusNode?.dispose();
    patientNameController?.dispose();

    patientEmailFocusNode?.dispose();
    patientEmailController?.dispose();

    patientPhoneFocusNode?.dispose();
    patientPhoneController?.dispose();

    patientAgeFocusNode?.dispose();
    patientAgeController?.dispose();

    patientHeightFocusNode?.dispose();
    patientHeightController?.dispose();

    patientWeightFocusNode?.dispose();
    patientWeightController?.dispose();

    patientDescriptionFocusNode?.dispose();
    patientDescriptionController?.dispose();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}
