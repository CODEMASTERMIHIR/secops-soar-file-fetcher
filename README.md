# Google SecOps Ephemeral Payload Bridge

## Overview
A custom Python action for Google SecOps (Chronicle SOAR) designed to interact directly with the platform's ephemeral backend disk (`/opt/siemplify/...`). 

When files are fetched via vendor APIs, they are temporarily written to the backend server before routine storage cleanup purges them. Native marketplace utilities often fail to handle these raw paths properly—especially when dealing with encrypted headers or unsupported file types. 

This script bridges the architectural gap by dynamically grabbing the temporary backend file path and converting the raw ephemeral file into a persistent Case Wall attachment entity before the server deletes it.

---

## Real-World Example 1: FireEye HX Triage Pipeline
When executing a **Get File** or **Acquire Triage** action via the FireEye HX integration, the payload is downloaded to the SecOps server as an encrypted ZIP archive (default password: `unzip-me`). 

**The Architectural Gap:** 
* Native **Extract Archive** uses `shutil` which crashes on encrypted headers.
* Native **Extract Zip Files** handles passwords but requires a pre-existing UI entity, not a backend server path.
* The `/opt/siemplify/...` directory is routinely purged, causing "No such file" errors if extraction is delayed.

**The Automated Workflow Solution:**
1. **FireEyeHX - Get File:** Downloads the archive to a temporary backend path.
2. **Ephemeral Payload Bridge (This Script):** Dynamically grabs the temporary path from the action result and attaches the raw `.zip` directly to the Case Wall.
3. **FileUtilities - Extract Zip Files:** Targets the newly attached UI entity, applies the `unzip-me` passphrase, and successfully extracts the triage logs directly into the case.

---

## Example 2: Universal File Retrieval (Any File on SOAR Server)
The architecture is not limited to `.zip` files. Vendor APIs frequently drop varying formats (e.g., `.pcap`, raw JSON telemetry, `.exe` malware samples, `.mans` memory dumps) onto the ephemeral backend disk.

**The Automated Workflow Solution:**
1. **Vendor API - Download File:** Fetches the arbitrary file type to the backend server.
2. **Ephemeral Payload Bridge (This Script):** Retrieves the dynamic file path and secures the raw file to the Case Wall UI. Once attached, it is safe from routine server purges and ready for subsequent playbook analysis (e.g., sending the `.exe` to a sandbox or parsing the JSON).

---

## Installation & Configuration
1. Navigate to the **IDE** in Google SecOps.
2. Create a new Custom Action (e.g., `Attach Ephemeral Payload`).
3. Paste the provided Python script into the editor.
4. Navigate to the **Parameters** tab in the right-hand panel.
5. Click **+ Add Parameter**.
6. Name the parameter exactly **`File Path`** (String).
7. Mark the parameter as **Mandatory**.
8. Save and Publish the action.

## Playbook Usage
1. Add the custom action to your playbook immediately following your file download step.
2. In the action settings, click the dynamic variable icon `[ ]` next to the `File Path` parameter.
3. Map this parameter to the **Action Result** of the preceding download step. 
4. The script will securely bridge the file to the UI.

---
