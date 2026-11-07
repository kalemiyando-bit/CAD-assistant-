Attribute VB_Name = "modGearWheelShaftDemo"
Option Explicit

' SolidWorks VBA macro source.
' Creates three editable native part files and a positioned assembly.
' All lengths passed to the SolidWorks API are in metres.

Private swApp As SldWorks.SldWorks

' -------------------------- EDITABLE DEMO PARAMETERS --------------------------
Private Const GEAR_TEETH As Long = 18
Private Const GEAR_MODULE_MM As Double = 2#
Private Const GEAR_PRESSURE_ANGLE_DEG As Double = 20#
Private Const GEAR_FACE_WIDTH_MM As Double = 15#
Private Const GEAR_BORE_MM As Double = 12#

Private Const WHEEL_OD_MM As Double = 80#
Private Const WHEEL_WIDTH_MM As Double = 24#
Private Const WHEEL_HUB_OD_MM As Double = 30#
Private Const WHEEL_HUB_EXTRA_MM As Double = 8#
Private Const WHEEL_BORE_MM As Double = 12#

Private Const SHAFT_DIAMETER_MM As Double = 12#
Private Const SHAFT_LENGTH_MM As Double = 100#

Private Const GEAR_ASSEMBLY_Z_MM As Double = 10#
Private Const WHEEL_ASSEMBLY_Z_MM As Double = 55#
Private Const MM_TO_M As Double = 0.001
Private Const PI As Double = 3.14159265358979
' -------------------------------------------------------------------------------

Public Sub main()
    On Error GoTo BuildFailed

    Set swApp = Application.SldWorks
    If swApp Is Nothing Then
        Err.Raise vbObjectError + 100, "GearWheelShaftDemo", _
                  "SolidWorks application was not found."
    End If

    Dim baseFolder As String
    Dim outputFolder As String
    Dim shaftPath As String
    Dim gearPath As String
    Dim wheelPath As String
    Dim assemblyPath As String

    baseFolder = InputBox( _
        "Enter an existing folder where the demo output folder should be created:", _
        "Gear / wheel / shaft demo", _
        Environ$("USERPROFILE") & "\Desktop")

    If Len(Trim$(baseFolder)) = 0 Then Exit Sub

    Do While Right$(baseFolder, 1) = "\" And Len(baseFolder) > 3
        baseFolder = Left$(baseFolder, Len(baseFolder) - 1)
    Loop

    If Dir$(baseFolder, vbDirectory) = vbNullString Then
        MsgBox "That folder does not exist. Create it first, then run the macro again.", _
               vbExclamation, "Folder not found"
        Exit Sub
    End If

    outputFolder = baseFolder & "\GearWheelShaftDemo_" & Format$(Now, "yyyymmdd_hhnnss")
    MkDir outputFolder

    shaftPath = outputFolder & "\Shaft_12x100.SLDPRT"
    gearPath = outputFolder & "\SpurGear_18T_Module2.SLDPRT"
    wheelPath = outputFolder & "\Wheel_OD80_Hub30.SLDPRT"
    assemblyPath = outputFolder & "\GearWheelShaftDemo.SLDASM"

    BuildShaft shaftPath, outputFolder & "\Shaft_12x100.STEP"
    BuildGear gearPath, outputFolder & "\SpurGear_18T_Module2.STEP"
    BuildWheel wheelPath, outputFolder & "\Wheel_OD80_Hub30.STEP"
    BuildAssembly shaftPath, gearPath, wheelPath, assemblyPath, _
                  outputFolder & "\GearWheelShaftDemo_Assembly.STEP"

    MsgBox "Demo complete." & vbCrLf & vbCrLf & _
           "Output folder:" & vbCrLf & outputFolder & vbCrLf & vbCrLf & _
           "Created: shaft, gear, wheel, assembly, and STEP exports." & vbCrLf & _
           "The gear tooth flanks are segmented approximations, not a production gear profile.", _
           vbInformation, "Gear / wheel / shaft demo"
    Exit Sub

BuildFailed:
    MsgBox "The macro stopped before completion." & vbCrLf & _
           "Error " & Err.Number & ": " & Err.Description & vbCrLf & vbCrLf & _
           "Any files already created are in:" & vbCrLf & outputFolder, _
           vbCritical, "Gear / wheel / shaft demo"
End Sub

Private Sub BuildShaft(ByVal nativePath As String, ByVal stepPath As String)
    Dim model As SldWorks.ModelDoc2
    Dim feature As Object

    Set model = swApp.NewPart
    If model Is Nothing Then
        Err.Raise vbObjectError + 101, "BuildShaft", _
                  "Could not create a part. Check that a default part template is set in SolidWorks."
    End If

    StartFrontPlaneSketch model
    model.SketchManager.CreateCircleByRadius 0#, 0#, 0#, (SHAFT_DIAMETER_MM / 2#) * MM_TO_M
    model.SketchManager.InsertSketch True

    Set feature = ExtrudeBoss(model, SHAFT_LENGTH_MM * MM_TO_M)
    feature.Name = "Shaft blank - editable length and diameter"

    SaveSolidWorksFile model, nativePath
    TryExportStep model, stepPath
End Sub

Private Sub BuildGear(ByVal nativePath As String, ByVal stepPath As String)
    Dim model As SldWorks.ModelDoc2
    Dim feature As Object
    Dim xs() As Double
    Dim ys() As Double
    Dim pointCount As Long
    Dim i As Long
    Dim nextIndex As Long

    Set model = swApp.NewPart
    If model Is Nothing Then
        Err.Raise vbObjectError + 102, "BuildGear", _
                  "Could not create a part. Check that a default part template is set in SolidWorks."
    End If

    MakeGearOutline GEAR_TEETH, GEAR_MODULE_MM, GEAR_PRESSURE_ANGLE_DEG, _
                    xs, ys, pointCount

    StartFrontPlaneSketch model
    For i = 0 To pointCount - 1
        nextIndex = (i + 1) Mod pointCount
        model.SketchManager.CreateLine _
            xs(i) * MM_TO_M, ys(i) * MM_TO_M, 0#, _
            xs(nextIndex) * MM_TO_M, ys(nextIndex) * MM_TO_M, 0#
    Next i

    model.SketchManager.CreateCircleByRadius _
        0#, 0#, 0#, (GEAR_BORE_MM / 2#) * MM_TO_M
    model.SketchManager.InsertSketch True

    Set feature = ExtrudeBoss(model, GEAR_FACE_WIDTH_MM * MM_TO_M)
    feature.Name = "Segmented spur gear profile - editable sketch"

    SaveSolidWorksFile model, nativePath
    TryExportStep model, stepPath
End Sub

Private Sub BuildWheel(ByVal nativePath As String, ByVal stepPath As String)
    Dim model As SldWorks.ModelDoc2
    Dim feature As Object
    Dim selected As Boolean

    Set model = swApp.NewPart
    If model Is Nothing Then
        Err.Raise vbObjectError + 103, "BuildWheel", _
                  "Could not create a part. Check that a default part template is set in SolidWorks."
    End If

    ' Main wheel ring, with a through bore.
    StartFrontPlaneSketch model
    model.SketchManager.CreateCircleByRadius 0#, 0#, 0#, _
        (WHEEL_OD_MM / 2#) * MM_TO_M
    model.SketchManager.CreateCircleByRadius 0#, 0#, 0#, _
        (WHEEL_BORE_MM / 2#) * MM_TO_M
    model.SketchManager.InsertSketch True
    Set feature = ExtrudeBoss(model, WHEEL_WIDTH_MM * MM_TO_M)
    feature.Name = "Wheel rim - editable diameter and width"

    ' Raised annular hub on one side; its bore stays open through the hub.
    model.ClearSelection2 True
    selected = model.Extension.SelectByID2( _
        "", "FACE", 20# * MM_TO_M, 0#, WHEEL_WIDTH_MM * MM_TO_M, _
        False, 0, Nothing, 0)
    If Not selected Then
        Err.Raise vbObjectError + 104, "BuildWheel", _
                  "Could not select the wheel face for the hub. The SolidWorks selection behavior may differ in this version."
    End If

    model.SketchManager.InsertSketch True
    model.SketchManager.CreateCircleByRadius 0#, 0#, 0#, _
        (WHEEL_HUB_OD_MM / 2#) * MM_TO_M
    model.SketchManager.CreateCircleByRadius 0#, 0#, 0#, _
        (WHEEL_BORE_MM / 2#) * MM_TO_M
    model.SketchManager.InsertSketch True

    Set feature = ExtrudeBoss(model, WHEEL_HUB_EXTRA_MM * MM_TO_M)
    feature.Name = "Wheel hub - editable diameter and projection"

    SaveSolidWorksFile model, nativePath
    TryExportStep model, stepPath
End Sub

Private Sub BuildAssembly( _
    ByVal shaftPath As String, _
    ByVal gearPath As String, _
    ByVal wheelPath As String, _
    ByVal nativePath As String, _
    ByVal stepPath As String)

    Dim model As SldWorks.ModelDoc2
    Dim assembly As SldWorks.AssemblyDoc
    Dim component As SldWorks.Component2

    Set model = swApp.NewAssembly
    If model Is Nothing Then
        Err.Raise vbObjectError + 105, "BuildAssembly", _
                  "Could not create an assembly. Check that a default assembly template is set in SolidWorks."
    End If

    Set assembly = model

    ' All three parts use the Z axis as their shaft axis.
    ' Components are positioned for demonstration; no mates or keyways are added.
    Set component = assembly.AddComponent5(shaftPath, 0, "", False, "", 0#, 0#, 0#)
    If component Is Nothing Then Err.Raise vbObjectError + 106, "BuildAssembly", "Could not insert the shaft."

    Set component = assembly.AddComponent5( _
        gearPath, 0, "", False, "", 0#, 0#, GEAR_ASSEMBLY_Z_MM * MM_TO_M)
    If component Is Nothing Then Err.Raise vbObjectError + 107, "BuildAssembly", "Could not insert the gear."

    Set component = assembly.AddComponent5( _
        wheelPath, 0, "", False, "", 0#, 0#, WHEEL_ASSEMBLY_Z_MM * MM_TO_M)
    If component Is Nothing Then Err.Raise vbObjectError + 108, "BuildAssembly", "Could not insert the wheel."

    model.EditRebuild3
    SaveSolidWorksFile model, nativePath
    TryExportStep model, stepPath
End Sub

Private Sub StartFrontPlaneSketch(ByVal model As SldWorks.ModelDoc2)
    Dim selected As Boolean
    model.ClearSelection2 True
    selected = model.Extension.SelectByID2( _
        "Front Plane", "PLANE", 0#, 0#, 0#, False, 0, Nothing, 0)
    If Not selected Then
        Err.Raise vbObjectError + 109, "StartFrontPlaneSketch", _
                  "Could not select 'Front Plane'. Check the SolidWorks language or default template."
    End If
    model.SketchManager.InsertSketch True
End Sub

Private Function ExtrudeBoss( _
    ByVal model As SldWorks.ModelDoc2, _
    ByVal depthM As Double) As Object

    Dim feature As Object
    model.ClearSelection2 True

    Set feature = model.FeatureManager.FeatureExtrusion2( _
        True, False, False, 0, 0, depthM, 0#, _
        False, False, False, False, 0#, 0#, _
        False, False, False, False, True, True, True, 0, 0, False)

    If feature Is Nothing Then
        Err.Raise vbObjectError + 110, "ExtrudeBoss", _
                  "The extrusion failed. Check that the sketch is closed and the default part template is valid."
    End If
    Set ExtrudeBoss = feature
End Function

Private Sub SaveSolidWorksFile( _
    ByVal model As SldWorks.ModelDoc2, _
    ByVal path As String)

    Dim errors As Long
    Dim warnings As Long
    Dim ok As Boolean

    ok = model.Extension.SaveAs(path, 0, 1, Nothing, errors, warnings)
    If Not ok Or errors <> 0 Then
        Err.Raise vbObjectError + 111, "SaveSolidWorksFile", _
                  "Could not save " & path & ". SolidWorks error code: " & errors
    End If
End Sub

Private Sub TryExportStep( _
    ByVal model As SldWorks.ModelDoc2, _
    ByVal path As String)

    Dim errors As Long
    Dim warnings As Long
    Dim ok As Boolean

    On Error Resume Next
    ok = model.Extension.SaveAs(path, 0, 1, Nothing, errors, warnings)
    On Error GoTo 0

    If Not ok Or errors <> 0 Then
        MsgBox "The native SolidWorks file was saved, but this STEP export did not complete:" & _
               vbCrLf & path & vbCrLf & _
               "You can still open the native file and use File > Save As > STEP.", _
               vbExclamation, "STEP export notice"
    End If
End Sub

Private Sub MakeGearOutline( _
    ByVal toothCount As Long, _
    ByVal moduleMM As Double, _
    ByVal pressureAngleDeg As Double, _
    ByRef xs() As Double, _
    ByRef ys() As Double, _
    ByRef pointCount As Long)

    Dim rootRadius As Double
    Dim pitchRadius As Double
    Dim baseRadius As Double
    Dim outsideRadius As Double
    Dim pressureAngle As Double
    Dim involuteAtPitch As Double
    Dim halfBaseAngle As Double
    Dim rootHalfAngle As Double
    Dim halfTipAngle As Double
    Dim centerAngle As Double
    Dim radius As Double
    Dim alpha As Double
    Dim involute As Double
    Dim sample As Long
    Dim tooth As Long
    Dim capacity As Long

    If toothCount < 8 Or moduleMM <= 0# Then
        Err.Raise vbObjectError + 112, "MakeGearOutline", _
                  "Gear tooth count must be at least 8 and module must be positive."
    End If

    rootRadius = (toothCount - 2.5) * moduleMM / 2#
    pitchRadius = toothCount * moduleMM / 2#
    baseRadius = pitchRadius * Cos(pressureAngleDeg * PI / 180#)
    outsideRadius = (toothCount + 2#) * moduleMM / 2#
    pressureAngle = pressureAngleDeg * PI / 180#
    involuteAtPitch = Tan(pressureAngle) - pressureAngle
    halfBaseAngle = PI / (2# * toothCount) + involuteAtPitch
    rootHalfAngle = 8# * PI / 180#
    alpha = Atn(Sqr(outsideRadius * outsideRadius - baseRadius * baseRadius) / baseRadius)
    halfTipAngle = halfBaseAngle - (Tan(alpha) - alpha)

    capacity = toothCount * 16
    ReDim xs(0 To capacity - 1)
    ReDim ys(0 To capacity - 1)
    pointCount = 0

    For tooth = 0 To toothCount - 1
        centerAngle = 2# * PI * tooth / toothCount

        AppendGearPoint xs, ys, pointCount, _
            rootRadius * Cos(centerAngle - rootHalfAngle), _
            rootRadius * Sin(centerAngle - rootHalfAngle)

        AppendGearPoint xs, ys, pointCount, _
            baseRadius * Cos(centerAngle - halfBaseAngle), _
            baseRadius * Sin(centerAngle - halfBaseAngle)

        ' Sample an involute-like left flank with short straight sketch segments.
        For sample = 1 To 6
            radius = baseRadius + (outsideRadius - baseRadius) * sample / 6#
            alpha = Atn(Sqr(radius * radius - baseRadius * baseRadius) / baseRadius)
            involute = Tan(alpha) - alpha
            AppendGearPoint xs, ys, pointCount, _
                radius * Cos(centerAngle - halfBaseAngle + involute), _
                radius * Sin(centerAngle - halfBaseAngle + involute)
        Next sample

        AppendGearPoint xs, ys, pointCount, _
            outsideRadius * Cos(centerAngle + halfTipAngle), _
            outsideRadius * Sin(centerAngle + halfTipAngle)

        ' Return down the right flank to the base circle.
        For sample = 5 To 0 Step -1
            radius = baseRadius + (outsideRadius - baseRadius) * sample / 6#
            alpha = Atn(Sqr(radius * radius - baseRadius * baseRadius) / baseRadius)
            involute = Tan(alpha) - alpha
            AppendGearPoint xs, ys, pointCount, _
                radius * Cos(centerAngle + halfBaseAngle - involute), _
                radius * Sin(centerAngle + halfBaseAngle - involute)
        Next sample

        AppendGearPoint xs, ys, pointCount, _
            rootRadius * Cos(centerAngle + rootHalfAngle), _
            rootRadius * Sin(centerAngle + rootHalfAngle)
    Next tooth

    ReDim Preserve xs(0 To pointCount - 1)
    ReDim Preserve ys(0 To pointCount - 1)
End Sub

Private Sub AppendGearPoint( _
    ByRef xs() As Double, _
    ByRef ys() As Double, _
    ByRef pointCount As Long, _
    ByVal x As Double, _
    ByVal y As Double)

    xs(pointCount) = x
    ys(pointCount) = y
    pointCount = pointCount + 1
End Sub
