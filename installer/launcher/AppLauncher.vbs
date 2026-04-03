' AppLauncher.vbs - Interactive launcher for Cashew Inventory (process mode)
Set WshShell = CreateObject("WScript.Shell")
AppDir = "C:\Program Files\CashewInventory"

choice = MsgBox("Do you want to START Cashew Inventory?" & vbCrLf & _
                "Click YES to start, NO to stop.", vbYesNo + vbQuestion, "Cashew Inventory")

If choice = vbYes Then
    Launcher = Chr(34) & AppDir & "\bin\AppLauncher.bat" & Chr(34) & " " & Chr(34) & AppDir & Chr(34)
    WshShell.Run Launcher, 0, False
Else
    Stopper = Chr(34) & AppDir & "\bin\StopLauncher.bat" & Chr(34)
    WshShell.Run Stopper, 0, False
End If