# Installing ControlUp for Apps

This article explains how to install ControlUp for Apps.

---

## Pre-requisites

- Windows devices have **ControlUp for Desktops Agent version 2.16 or higher**, or IGEL OS 12 devices with version 2.17.2 or higher
- Remember, you will be monitoring web applications accessed through **Microsoft Edge**, **Google Chrome**, or **Island**
- **End User Activity monitoring** is enabled in Edge DX
- Your license supports ControlUp for Apps
- Devices can access the CDN URLs for browser extensions
- Under **Employees / Privacy configuration**, you have user Domains defined

---

## Instructions

### Step 1: Deploy the ControlUp for Apps Module

1. Sign into [app.controlup.com](https://app.controlup.com)
2. Go to **Settings > ControlUp for Apps**
3. Under the **Deployment** tab:
   - Select which version to deploy (recommended: **Latest GA version** - this auto-updates)
   - Choose target devices using the **Targeted device groups** and **Targeted device tags** dropdowns
   - Or, select **All device groups** and **All device tags** to deploy on all devices with the ControlUp for Desktops Agent
4. Click **Apply**

> **[Image: ControlUp for Apps Deployment Settings]** Screenshot of the ControlUp web console at `app.controlup.com` showing the **Settings > ControlUp for Apps** page with the **Deployment** tab selected. The interface displays a version selector dropdown (set to "Latest GA version"), along with dropdown menus for "Targeted device groups" and "Targeted device tags" to select which devices receive the deployment. An "Apply" button is visible at the bottom.

---

### Step 2: Deploy the Browser Extension

1. Under the **Extensions** tab
2. Set **Browser extension deployment** to: **Automatically install on all devices where ControlUp for Apps has been deployed** (recommended)
3. Configure whether to **Allow end users to open the extension UI**:
   - Allow on all devices
   - Allow only on certain devices
   - Do not allow

> **[Image: ControlUp for Apps Initial Setup Wizard]** Screenshot of the ControlUp for Apps first-use setup wizard. When you first use ControlUp for Apps, you are presented with this wizard that asks if you want to deploy ControlUp for Apps for all devices, automatically deploy extensions, and select pre-defined App Groups.

> **[Image: Browser Extension Deployment Settings]** Screenshot of the **Extensions** tab within the ControlUp for Apps settings, showing the browser extension deployment options and the end-user extension UI access configuration with three radio button options: "Allow on all devices", "Allow only on certain devices", and "Do not allow".

---

### Step 3: Create Monitored App Groups

1. Go to **Settings > Employees > App groups**
2. Click **Add App Group**
3. Provide a name and optional description
4. Select the **URLs** tab and add the URLs you want to monitor
5. **Important:** Check the box for **Use with ControlUp for Apps**
6. Click **Submit**

> **[Image: App Groups Configuration]** Screenshot of the **Settings > Employees > App groups** page showing the "Add App Group" dialog. The form includes fields for the app group name and description, a URLs tab for adding monitored URLs, a checkbox labeled "Use with ControlUp for Apps", and a "Submit" button to save the configuration.
