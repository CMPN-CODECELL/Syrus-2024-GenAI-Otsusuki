import '/flutter_flow/flutter_flow_drop_down.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import '/flutter_flow/form_field_controller.dart';
import 'add_patient_widget.dart' show AddPatientWidget;
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

  /// Initialization and disposal methods.

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    patientNameFocusNode?.dispose();
    patientNameController?.dispose();

    patientAgeFocusNode?.dispose();
    patientAgeController?.dispose();

    patientHeightFocusNode?.dispose();
    patientHeightController?.dispose();

    patientWeightFocusNode?.dispose();
    patientWeightController?.dispose();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}
