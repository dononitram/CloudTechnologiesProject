Attribute VB_Name = "Predict"
Sub Predict()
    Dim xhr As Object
    Dim url As String
    Dim response As String
    Dim prediction As String
    Dim predictionsArray() As String
    Dim inputValues As String
    Dim cell As Range
    Dim randomValue As Double
    Dim i As Long
    Dim decimalSeparator As String
    Dim col As Long
    Dim hasInput As Boolean
    Dim configFilePath As String
    Dim jsonContent As String
    Dim jsonObject As Object

    ' Get the system's decimal separator
    decimalSeparator = Application.International(xlDecimalSeparator)

    ' Create the XMLHttpRequest object
    Set xhr = CreateObject("MSXML2.XMLHTTP")

    ' Define the path to the config.json file (same directory as the workbook)
    configFilePath = ThisWorkbook.Path & "\config.json"

    ' Read the content of the config.json file
    On Error Resume Next
    jsonContent = CreateObject("Scripting.FileSystemObject").OpenTextFile(configFilePath, 1).ReadAll
    On Error GoTo 0

    ' Extract host and port using your custom function
    Dim host As String, port As String
    host = ExtractJsonField(jsonContent, "host")
    port = ExtractJsonField(jsonContent, "port")

    ' Set default values if fields are missing
    If host = "" Then host = "localhost" '"158.101.170.44"
    If port = "" Then port = "8000"

    ' Initialize base URL for the API
    url = "http://" & host & ":" & port & "/predict"

    ' Initialize the input values string and flag for input validation
    inputValues = ""
    hasInput = False

    ' Loop through cells in row 4 (starting from column C) to check for input
    For col = 3 To ThisWorkbook.Sheets(1).UsedRange.Columns.Count
        Set cell = ThisWorkbook.Sheets(1).Cells(4, col)
        If cell.Value <> "" Then
            hasInput = True
            ' Append each value as a comma-separated string
            If Len(inputValues) > 0 Then
                inputValues = inputValues & "%"
            End If
            inputValues = inputValues & URLEncode(cell.Value)
        End If
    Next col

    ' Validate that input row is not empty
    If Not hasInput Then
        MsgBox "Error: No input found in row 4. Please provide input values.", vbExclamation
        Exit Sub
    End If

    ' Build the full URL with the query parameters
    randomValue = Rnd()
    url = url & "?input=" & inputValues & "&rand=" & randomValue

    ' Open the request (GET method)
    xhr.Open "GET", url, False

    ' Set necessary headers to prevent caching
    xhr.setRequestHeader "Content-Type", "application/json"

    ' Send the GET request
    xhr.Send

    ' Error handling for the request
    If xhr.Status = 200 Then
        response = xhr.responseText
    Else
        MsgBox "Error: " & xhr.Status & " - " & xhr.statusText, vbCritical
        Exit Sub
    End If

    ' Extract the prediction field using a more robust JSON parsing method
    prediction = ExtractJsonField(response, "prediction")
    If prediction = "" Then
        MsgBox "Error: 'prediction' field not found in response", vbExclamation
        Exit Sub
    End If

    ' Split predictions by comma
    predictionsArray = Split(prediction, ",")

    ' Replace the decimal separator in each value (if needed)
    For i = 0 To UBound(predictionsArray)
        If decimalSeparator <> "." Then
            predictionsArray(i) = Replace(predictionsArray(i), ".", decimalSeparator)
        End If
    Next i

    ' Clear row 5 from column C onwards before writing new values
    ThisWorkbook.Sheets(1).Rows(5).Columns("C:Z").ClearContents

    ' Write each prediction value in the corresponding columns starting from C5
    For i = 0 To UBound(predictionsArray)
        ThisWorkbook.Sheets(1).Cells(5, 3 + i).Value = CDbl(Trim(predictionsArray(i))) ' Ensure proper conversion to decimal
    Next i

    ' Store the raw response in a worksheet cell for debugging (optional)
    ' ThisWorkbook.Sheets(1).Range("A1").Value = response

    ' Clear the xhr object
    Set xhr = Nothing

End Sub

' Helper function to URL encode the input values
Function URLEncode(str As String) As String
    Dim result As String
    Dim i As Long
    Dim charCode As Long
    result = ""
    For i = 1 To Len(str)
        charCode = Asc(Mid(str, i, 1))
        If (charCode >= 48 And charCode <= 57) Or (charCode >= 65 And charCode <= 90) Or (charCode >= 97 And charCode <= 122) Then
            result = result & Chr(charCode)
        Else
            result = result & "%" & Right("00" & Hex(charCode), 2)
        End If
    Next i
    URLEncode = result
End Function

' Helper function to extract a JSON field value
Function ExtractJsonField(json As String, fieldName As String) As String
    Dim startPos As Long, endPos As Long, fieldValue As String
    Dim searchPattern As String
    searchPattern = """" & fieldName & """:" & """"
    startPos = InStr(json, searchPattern)
    If startPos > 0 Then
        startPos = startPos + Len(searchPattern)
        endPos = InStr(startPos, json, """")
        If endPos > 0 Then
            fieldValue = Mid(json, startPos, endPos - startPos)
            ExtractJsonField = fieldValue
        Else
            ExtractJsonField = ""
        End If
    Else
        ExtractJsonField = ""
    End If

End Function

