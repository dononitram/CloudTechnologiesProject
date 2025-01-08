Attribute VB_Name = "Train"
' Helper function to extract a JSON field value
Function ExtractJsonField(json As String, fieldName As String) As String
    Dim startPos As Long, endPos As Long, fieldValue As String
    Dim searchPattern As String
    searchPattern = """" & fieldName & """:" & """" ' e.g., "model_hash":
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

' Main Train macro
Sub Train()
    Dim xhr As Object
    Dim url As String
    Dim response As String
    Dim row As Long, col As Long
    Dim jsonData As String
    Dim cell As Range
    Dim modelHash As String
    Dim configFilePath As String
    Dim jsonContent As String
    Dim jsonObject As Object
    
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
    url = "http://" & host & ":" & port & "/train"
   
    ' Initialize the JSON data array
    jsonData = "{""cells"":["

    rowStart = 8
    colStart = 3
    ' Loop through all cells starting from C8 onwards
    For row = rowStart To ThisWorkbook.Sheets(1).UsedRange.Rows.Count
        For col = colStart To ThisWorkbook.Sheets(1).UsedRange.Columns.Count
            Set cell = ThisWorkbook.Sheets(1).Cells(row, col)
            If cell.Value <> "" Then
                ' Append cell value as a JSON object to the array
                If Len(jsonData) > Len("{""cells"":[") Then
                    jsonData = jsonData & ","
                End If
                jsonData = jsonData & "{""row"":" & row & ",""col"":" & col & ",""value"":""" & cell.Value & """}"
            End If
        Next col
    Next row
    
    ' Close the JSON array
    jsonData = jsonData & "]}"
    
    ' Debug print the generated JSON data
    ' Debug.Print jsonData
    
    ' Open the request (POST method)
    xhr.Open "POST", url, False
    
    ' Set necessary headers
    xhr.setRequestHeader "Content-Type", "application/json"
    
    ' Send the request with the JSON data in the body
    xhr.Send jsonData
    
    ' Process the response
    If xhr.Status = 200 Then
        response = xhr.responseText
        ' Extract the model hash from the response
        modelHash = ExtractJsonField(response, "model_hash")
        
        ' Store the model hash in a specific cell (e.g., A1)
        ThisWorkbook.Sheets(1).Range("A1").Value = modelHash
        
        ' Notify the user
        MsgBox "Training successful. Model hash: " & modelHash, vbInformation
    Else
        ' Handle errors
        MsgBox "Error during training: " & xhr.Status & " - " & xhr.statusText, vbCritical
    End If
    
    ' Clear the XMLHttpRequest object
    Set xhr = Nothing
End Sub
