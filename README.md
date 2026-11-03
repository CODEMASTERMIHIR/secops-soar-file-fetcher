# Google SecOps Ephemeral Payload Bridge

## Overview
A custom Python action for Google SecOps (Chronicle SOAR) designed to dynamically fetch ephemeral file payloads from backend server directories (`/opt/siemplify/...`) and attach them as persistent, native entities to the Case Wall. 

This utility was engineered to bridge architectural gaps in the native FileUtilities integration, ensuring that vendor API downloads—specifically password-protected archives like those from FireEye HX—are preserved in the UI before routine backend storage cleanup occurs.

## Architectural Problem
When pulling files from vendor APIs to the Google SecOps backend, security engineers encounter two conflicting limitations within the native marketplace `FileUtilities`:
1. **Extract Archive:** Accepts a backend server path but utilizes Python's `shutil` library, which lacks password support and crashes upon encountering encrypted headers.
2. **Extract Zip Files:** Supports password decryption but interacts strictly with the platform's front-end UI layer. It requires a pre-existing `FILENAME` entity (Case Wall attachment) and cannot route to a raw disk path.

Furthermore, the ephemeral `/opt/siemplify/...` directories where these files land are routinely purged by the platform to conserve disk space, resulting in `[Errno 2] No such file or directory` execution failures if extraction is delayed.

## Solution
This script extracts the dynamic file path immediately after the vendor API download step, reads the raw file from the backend disk, and utilizes `SiemplifyAction.add_attachment()` to bridge the file directly to the Case Wall. This converts the ephemeral disk file into a persistent UI entity, enabling native password-capable extraction workflows in subsequent playbook steps.

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

1. Add the custom action to your playbook immediately following your file download step (e.g., `FireEyeHX - Get File`).
2. In the action settings, click the dynamic variable icon `[ ]` next to the `File Path` parameter.
3. Map this parameter to the **Action Result** of the preceding download step.
4. *(Optional)* To extract encrypted archives, add the marketplace **Extract Zip Files** action immediately after this script. Set Entities to **Specific**, select the newly created attachment entity, and provide the required passphrase.
