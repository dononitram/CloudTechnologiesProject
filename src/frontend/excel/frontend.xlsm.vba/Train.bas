Sub Train()
    Dim xhr As Object
    Dim url As String
    Dim response As String
    Dim row As Long, col As Long
    Dim jsonData As String
    Dim cell As Range
    
    ' Create the XMLHttpRequest object
    Set xhr = CreateObject("MSXML2.XMLHTTP")
    
    ' Initialize base URL for the API
    url = "http://158.101.170.44:8000/train" ' Replace with your API endpoint
    
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
                    jsonData = jsonData & ", "
                End If
                jsonData = jsonData & "{""row"":" & row & ", ""col"":" & col & ", ""value"":""" & cell.Value & """}"
            End If
        Next col
    Next row
    
    ' Close the JSON array
    jsonData = jsonData & "]}"
    
    ' Debug print the generated JSON data
    ' Debug.Print jsonData
    
    ' Open the request (POST method in this case)
    xhr.Open "POST", url, False
    
    ' Set any necessary headers (optional)
    xhr.setRequestHeader "Content-Type", "application/json"
    
    ' Send the request with the JSON data in the body
    xhr.Send jsonData
    
    ' Get the response
    response = xhr.responseText
    
    ' Display the response in the Immediate Window (Ctrl+G to see it)
    Debug.Print response
    
    ' You can also store the response in a worksheet cell
    ' ThisWorkbook.Sheets(1).Range("A1").Value = response
    
End Sub