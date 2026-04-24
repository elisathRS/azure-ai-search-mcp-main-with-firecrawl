# First Steps for ControlUp for VDI

- Updated on Apr 22, 2026
- Published on Mar 17, 2024

- 3 minute(s) read
- Listen

Follow

Export PDF  Print

[Prev](https://support.controlup.com/docs/getting-started-with-controlup-hybrid-cloud "ControlUp ONE Overview and Architecture")[Next](https://support.controlup.com/docs/get-started-with-controlup-for-desktops "First Steps for ControlUp for Desktops")

After you’ve signed up for your ControlUp organization, follow this article to set up your ControlUp for VDI environment.

## Download and sign into the Real-Time DX Console

Most of your day-to-day work with ControlUp can be done from our web interface. But the Real-Time DX Console is required to connect ControlUp to your virtual infrastructure and configure important features. Signing into the Console requires:

- Your ControlUp account must have the permission **Access Real-Time DX Console**. If you created your ControlUp organization, then you are an Admin and already have this permission.

- Microsoft Edge or Google Chrome must be installed.


**To sign into Console:**

1. Download the Console from our [Download Center](https://www.controlup.com/products/controlup/download-center/).

2. Unzip the file.

3. Run **ControlUpConsole.exe**. A login page is opened in either Microsoft Edge or Google Chrome.

4. In your browser, enter the email address of your ControlUp account and enter the OTP sent to your email address.

5. Select your organization and sign in to your account.


After you sign in, the Console opens. For more details, read [Sign in to the Real-Time Console](https://support.controlup.com/v1/docs/sign-in-to-the-real-time-console)

## Activate Your License

If you have purchased a ControlUp license, activate it according to your organization’s needs:

- For single-tenant and direct customers, see [here](https://support.controlup.com/v1/docs/what-is-the-new-subscription-feature#activate-your-license).

- For MSPs and multi-tenant customers, see [here](https://support.controlup.com/v1/docs/subscription-for-tenant-manager).


## Configure your environment

You can now connect your resources to ControlUp. To configure your environment, perform the following steps:

### Prerequisites

Verify that your environment is ready for ControlUp according to the following prerequisites:

- [Hardware / Software Prerequisites](https://support.controlup.com/tim-reorg/docs/controlup-hybrid-cloud-implementation-requirements)

- [Network requirements (US Region)](https://support.controlup.com/tim-reorg/docs/communication-ports-used-by-controlup-hybrid-cloud-us-customers)

- [Network requirements (EU Region)](https://support.controlup.com/tim-reorg/docs/communication-ports-used-by-controlup-hybrid-cloud-eu-customers)

- [Sizing Guidelines](https://support.controlup.com/tim-reorg/docs/sizing-guidelines-for-controlup-v8-x)


### 1\. Add Machines

Connect physical and virtual machines to ControlUp by installing the ControlUp Agent on the machines. To learn how to add machines, see [Connect to Your Machines](https://support.controlup.com/tim-reorg/docs/connect-to-your-machines).

Tip

You can create folders in your ControlUp organization tree to organize the machines that you add. To learn how to create folders, see [Create Folders](https://support.controlup.com/tim-reorg/docs/create-folders).

### 2\. Create Shared Credentials

When any ControlUp component connects to a resource that requires authentication, such as hypervisors, EUC environments, or cloud environments, the same set of credentials must be used by each ControlUp component. We recommend that you add credentials to ControlUp and share them so that all ControlUp users in your organization can use the same credentials.

To learn how to add shared credentials, see [Configuring Shared Credentials](https://support.controlup.com/tim-reorg/docs/configuring-shared-credentials).

**Service Account Permissions**

The credentials you use to connect resources to ControlUp require specific permissions depending on the resource. You should create a service account for each resource with the permissions listed in [User Permissions in ControlUp](https://support.controlup.com/tim-reorg/docs/user-permissions-in-controlup).

### 3\. Add a Monitor

Setting up a monitor allows you to continously monitor your ControlUp environment. You need at least one monitor to be able to access the VDI App and reports in ControlUp's [DEX platform](https://support.controlup.com/tim-reorg/docs/get-started-with-the-new-dex-platform).

To learn how to install and configure your monitor machines, see [ControlUp Monitor](https://support.controlup.com/tim-reorg/docs/controlup-monitor).

**Note**

Make sure you install the ControlUp Agent on each monitor machine.

### 4\. Configure a Dedicated Data Collector

A Data Collector increases the performance capabilities of both your console and monitor when collecting metrics from external sources such as VMware vCenter, Citrix Delivery Controllers, XenServer Pool Masters, AHV Clusters, and ADC appliances.

A Data Collector can be any machine that has the ControlUp Agent installed. To learn more about Data Collectors, see [ControlUp Data Collector](https://support.controlup.com/tim-reorg/docs/controlup-data-collector#data-collector-configuration).

### 5\. Add Hypervisors

Monitor and manage your virtualization infrastructure by connecting to VMware vSphere, Citrix Hypervisor, Nutanix AHV, or Microsoft Hyper-V.

To learn how to add add hypervisors, see [Connect to Your Hypervisors](https://support.controlup.com/tim-reorg/docs/connect-to-your-hypervisors).

### 6\. Add EUC Environments

For details on how to add a connection for each type of EUC environment, and what you can monitor, see the following articles:

- [Citrix Virtual Apps and Desktops](https://support.controlup.com/tim-reorg/docs/add-cvad-integration)

- [Omnissa Horizon](https://support.controlup.com/tim-reorg/docs/add-horizon-integration)

- [Citrix Cloud](https://support.controlup.com/tim-reorg/docs/add-citrix-cloud-integration)


### 7\. Add Cloud Environments

ControlUp comes with built-in support for [Azure](https://support.controlup.com/tim-reorg/docs/azure-integration-getting-started) and [AWS](https://support.controlup.com/tim-reorg/docs/add-cloud-infrastructure) monitoring.

### 8\. Add an ADC Appliance

To learn how to add Citrix ADC to your ControlUp environment, see  [Add an Application Delivery Controller](https://support.controlup.com/tim-reorg/docs/add-netscaler-appliance).

## Next Steps

After you set up your ControlUp environment and connect all your resources, follow the next steps to effectively use ControlUp:

- [Add the rest of your team to your ControlUp organization](https://support.controlup.com/v1/docs/add-dex-platform-users).

- [Set up proactive EUC and network tests to identify issues before they become problems.](https://support.controlup.com/tim-reorg/docs/getting-started-with-scoutbees)

- [Set up Triggers to record incidents and automatically remediate issues as soon as they occur.](https://support.controlup.com/tim-reorg/docs/setting-up-triggers)

- [Use ControlUp VDI App to create custom dashboards, see historical reports, and manage your environment, all from a browser.](https://support.controlup.com/tim-reorg/docs/web-ui)


Was this article helpful?

Yes  No

Previous article

ControlUp ONE Overview and Architecture

Next article

First Steps for ControlUp for Desktops