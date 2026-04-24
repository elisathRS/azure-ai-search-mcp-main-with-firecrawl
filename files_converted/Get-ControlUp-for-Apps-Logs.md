# Get ControlUp for Apps Logs

This article explains how to capture ControlUp for Apps Logs. Specifically, what the `AppDXHelper.exe` process does.

---

## Instructions

### 1 - Run the PowerShell Commands

Run these PowerShell commands to enable logging:

```powershell
[System.Environment]::SetEnvironmentVariable("EdgeDXLoggingEnabled", "true", "Machine")
Get-Process AppDXHelper,sipagent | Stop-Process -Force
```

### 2 - Locate the Log Files

The logs should be generated within a few minutes and will be located at:

```
C:\Program Files\ControlUp\Modules\appdx\logs
```

> **[Image: Log File Location in File Explorer]** Screenshot of a Windows File Explorer window navigated to `C:\Program Files\ControlUp\Modules\appdx\logs`, showing the generated log files in the directory listing.

See file generated:

> **[Image: Generated Log File]** Screenshot showing the generated log file in the logs directory with a filename following the pattern `<MACHINE_NAME>$AppDX_Logging_PID_<PID>_<DATE>_<TIME>.log` -- in this example: `OSMANIPC$AppDX_Logging_PID_42996_2025-10-04_21-21-31.log`.

---

### 3 - Log File Example

Below is an example of a generated log file:

```log
=== Opened file ===================================================================
[04/10/2025 21:21:31.8129][1] INFO  : ========================================================================
[04/10/2025 21:21:31.8392][1] INFO  : User: 'OSMANIPC$'.
[04/10/2025 21:21:31.8405][1] INFO  : Generated On: '10/4/2025 9:21:31 PM'.
[04/10/2025 21:21:31.8437][1] INFO  : Version: '1.1.318.0'.
[04/10/2025 21:21:31.8440][1] INFO  : Machine Name: 'OSMANIPC'.
[04/10/2025 21:21:31.8528][1] INFO  : Operating System: 'Windows 11 Professional (Build: 10.0.26100) (Microsoft Windows NT 10.0.26100.0)'.
[04/10/2025 21:21:31.8528][1] INFO  : ========================================================================
[04/10/2025 21:21:31.8532][1] INFO  : AppDX Env Log path: 'C:\Program Files\ControlUp\Modules\AppDX\logs'.
[04/10/2025 21:21:31.8533][1] INFO  : EdgeDX Env Dll path: 'C:\Program Files\Avacee\sip_agent\EdgeSdk.dll'.
```

The log continues with debug entries showing the following startup sequence:

1. **Argument Parsing & Windows Loading** - Parses command-line arguments and loads Windows-specific modules.

2. **SIPAgent Validation** - Validates that `SIPAgent.exe` exists at `C:\Program Files\Avacee\sip_agent\SIPAgent.exe` and checks its version (e.g., `2.17.5.6846`).

3. **EdgeSdk.dll Validation** - Validates that `EdgeSdk.dll` exists and checks its version (e.g., `1.0.0.5`).

4. **EdgeSDK Function Loading** - Loads SDK functions: `sdkVersion`, `fetchConfig`, `sendInfo`, `registerEvent`, `waitForEvent`.

5. **Configuration Fetch** - Fetches URL configuration from EdgeSDK (e.g., `["docs.google.com","google.com","youtube.com"]`) and settings including:
   - `installBrowserExtension`: true
   - `port`: 6071
   - `saveLogs`: 0
   - `showExtensionUI`: true
   - `enableScreenCapture`: true

6. **Browser Extension Registry Configuration** - Sets registry keys for Chrome, Edge, and Island browser extensions:
   - Chrome extension ID: `fbmmpaeakganhhofacjdciocgnbclbcl`
   - Edge extension ID: `jmnkfnngldhhdkggfgemlkckmphhnojp`
   - Island extension ID: `jmnkfnngldhhdkggfgemlkckmphhnojp`

   Registry values configured per browser:
   - `PortNumber`: 6071
   - `Url`: localhost
   - `TabDataCollectionEnabled`: False
   - `TabDataCollectionPeriod`: 10
   - `PageLoadDataCollectionEnabled`: True
   - `ErrorDataCollectionEnabled`: True
   - `ErrorDataCollection`: CollectAllErrors
   - `ShowExtensionUI`: True
   - `EnableScreenCapture`: True
   - `ReloadFirstPageEnabled`: False
   - `PublicKey`: (RSA public key for secure communication)

7. **WebSocket Server Startup** - Starts a web socket server on `127.0.0.1:6071` for browser extension communication.

8. **User Event Registration** - Registers for logon, logoff, config change, and request stop events via EdgeSDK.

9. **User Session Processing** - Processes user logon sessions and sets per-user browser extension registry keys with the `UserId`.

10. **Browser Extension Connection** - Processes incoming WebSocket connections from Chrome and Edge browser extensions, receiving `CONFIG` messages containing browser name, version, extension version, and user ID.

```log
[04/10/2025 21:21:32.2040][6] INFO  : Started web socket server on IP '127.0.0.1' for port '6071'.
[04/10/2025 21:21:32.2040][6] INFO  : The SDK has successfully been started.
[04/10/2025 21:21:32.2040][1] INFO  : Launched AppDX SDK.
[04/10/2025 21:21:32.2128][1] INFO  : Found parent process '39492'.
[04/10/2025 21:21:32.2174][1] INFO  : Waiting for exit request for AppDX Helper.
```

**Note:** In this example log, an error occurs when the browser extensions connect:

```log
[04/10/2025 21:21:33.8145][13] ERROR : Received user 'b01e4660-d015-40d4-9193-29f4ba3464a3'. Unable to determine Session Id.
```

This results in a failed connection response:

```json
{"ReplyDataString": "Failed to process connection.", "ErrorNumber": 300}
```
