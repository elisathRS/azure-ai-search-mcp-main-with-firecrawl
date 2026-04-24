# Uninstall AppDX

This article explains how to uninstall ControlUp for Apps.

---

## Instructions

### 1 - Verify AppDXHelper.exe is Running

Verify the `AppDXHelper.exe` process is running on the machine you want to uninstall.

> **[Image: Task Manager showing AppDXHelper.exe]** Screenshot of Windows Task Manager with the Processes or Details tab open, showing the `AppDXHelper.exe` process currently running on the target machine. This confirms that ControlUp for Apps is active and needs to be uninstalled.

---

### 2 - Assign Machine to a Tag or Device Group

In ControlUp for Desktops, make sure the machine is assigned to a specific **Tag** or **Device Group**. This group will include the machines you **don't** want ControlUp for Apps to be installed on.

In this example, the tag `"noappdxforev"` was used.

> **[Image: ControlUp for Desktops - Device Tag Assignment]** Screenshot of the ControlUp for Desktops console showing a machine being assigned to a tag. In this example, the machine is tagged with `"noappdxforev"` to designate it as a device that should not have ControlUp for Apps installed.

---

### 3 - Exclude the Tag from Targeted Devices

Make sure under the **ControlUp for Apps Settings**, you **don't** have the tag (created to group machines you don't want ControlUp for Apps to run on) listed under the **"Targeted device tags"**.

> **[Image: ControlUp for Apps Settings - Targeted Device Tags]** Screenshot of the ControlUp for Apps deployment settings page showing the "Targeted device tags" dropdown. The `"noappdxforev"` tag is **not** included in the targeted tags list, ensuring machines with that tag will not receive the ControlUp for Apps deployment.

---

### 4 - Restart and Verify

Restart the **ControlUp for Desktop Service** or the machine, and verify that the `AppDXHelper.exe` process **no longer appears** in the Task Manager.

> **[Image: Task Manager after Uninstall]** Screenshot of Windows Task Manager after restarting the ControlUp for Desktop Service or the machine, confirming that the `AppDXHelper.exe` process is no longer listed among running processes -- verifying that ControlUp for Apps has been successfully uninstalled.
