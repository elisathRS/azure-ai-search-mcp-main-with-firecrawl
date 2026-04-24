# AppDX App Web Launch Steps

Keep in mind that all requests come with a `cu-request-id`. You could search in Splunk to see what data is returned on each call. The Splunk query would be something like this:

```
index=* 45f058c3-5b0d-44d4-b8b7-ca33a4ac4565
```

Where `45f058c3-5b0d-44d4-b8b7-ca33a4ac4565` is the `cu-request-id` for this call.

> **[Image: AppDX Web App Dashboard]** Screenshot of the ControlUp AppDX web application interface showing the App Groups page at `https://prod-appdx-dal-us.controlup.com/app-groups` with sort parameters `sortDir=asc`, `sortField=score`, and a time range filter. The dashboard displays monitored application groups with their scores, employee counts, and performance metrics.

---

## 1 - Check Pre-Reqs

**Endpoint:** `https://prod-appdx-dal-us.controlup.com/edge/checkPrerequisites`

```python
import requests

cookies = {
    '_mkto_trk': 'id:191-KTT-691&token:_mch-controlup.com-...',
    'dex_session': 'true',
    'dex_env': 'prod',
    'dex_region': 'US',
    'connect.sid': 's%3Ao-YIHyfXaGdMHP6ZKC2MlIW-YcszzWXA...',
    # ... additional session/auth cookies omitted for brevity
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8,it;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cu-request-id': 'ac08219f-c490-4b1b-842b-3b426024e7d1',
    'origin': 'https://app.controlup.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.controlup.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://prod-appdx-dal-us.controlup.com/edge/checkPrerequisites',
    cookies=cookies,
    headers=headers
)
```

**Response:**

```json
{"data": {"status": 0}}
```

---

## 2 - Check Features

**Endpoint:** `https://prod-appdx-dal-us.controlup.com/license/features`

```python
import requests

cookies = {
    # Same session/auth cookies as above
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8,it;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cu-request-id': '7987c606-01cb-4120-8f93-816dfe26efda',
    'origin': 'https://app.controlup.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.controlup.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://prod-appdx-dal-us.controlup.com/license/features',
    cookies=cookies,
    headers=headers
)
```

**Response:**

```json
{"app_dx": true}
```

---

## 3 - Check Status

**Endpoint:** `https://prod-appdx-dal-us.controlup.com/initial-configuration/status`

```python
import requests

cookies = {
    # Same session/auth cookies as above
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8,it;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cu-request-id': '3767d411-c242-4b8a-9459-e79787c3841d',
    'origin': 'https://app.controlup.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.controlup.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://prod-appdx-dal-us.controlup.com/initial-configuration/status',
    cookies=cookies,
    headers=headers,
)
```

**Response:**

```json
{
    "appDXWizardCompleted": true,
    "isEndUserActivityEnabled": true,
    "shouldShowDomainAlert": false,
    "appGroupsExist": true
}
```

---

## 4 - Check App Groups (Final Data)

This is the final data we want to see!

**Endpoint:** `https://prod-appdx-dal-us.controlup.com/app-groups?sortDir=asc&sortField=score&from=2025-09-10T12%3A14%3A02.186Z&to=2025-09-10T12%3A24%3A02.186Z`

```python
import requests

cookies = {
    # Same session/auth cookies as above
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8,it;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cu-request-id': '45f058c3-5b0d-44d4-b8b7-ca33a4ac4565',
    'origin': 'https://app.controlup.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.controlup.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

params = {
    'sortDir': 'asc',
    'sortField': 'score',
    'from': '2025-09-10T12:14:02.186Z',
    'to': '2025-09-10T12:24:02.186Z',
}

response = requests.get(
    'https://prod-appdx-dal-us.controlup.com/app-groups',
    params=params,
    cookies=cookies,
    headers=headers
)
```

**Response:**

```json
[
    {
        "name": "Salesforce",
        "score": 0.2,
        "employees": 1,
        "cost": 0,
        "web": true,
        "urls": [
            "controlup.my.salesforce.com"
        ],
        "platform": [
            "Windows"
        ],
        "pageloadTime": 8.09,
        "ttfbTime": 0.91,
        "hardErrors": 0,
        "softErrors": 0
    },
    {
        "name": "IT Tools",
        "score": 0.2,
        "employees": 1,
        "cost": 0,
        "web": true,
        "urls": [
            "service-now.com",
            "techtoday.lenovo.com",
            "salesforce.com",
            "hubspot.com",
            "dev194317.service-now.com",
            "app-na2.hubspot.com"
        ],
        "platform": [
            "Windows"
        ],
        "pageloadTime": 8.09,
        "ttfbTime": 0.91,
        "hardErrors": 0,
        "softErrors": 0
    },
    {
        "name": "Google Workspace",
        "score": 0.8,
        "employees": 1,
        "cost": 0,
        "web": true,
        "urls": [
            "calendar.google.com",
            "docs.google.com",
            "drive.google.com",
            "mail.google.com",
            "meet.google.com",
            "sites.google.com"
        ],
        "platform": [
            "Windows"
        ],
        "pageloadTime": 0.91,
        "ttfbTime": 0.28,
        "hardErrors": 0,
        "softErrors": 2
    }
]
```

---

## 5 - Get Environment Config

Not sure of the exact order of this call.

**Endpoint:** `https://prod-appdx-k8s.controlup.com/env-config/config.json`

```python
import requests

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8,it;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://app.controlup.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.controlup.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://prod-appdx-k8s.controlup.com/env-config/config.json',
    headers=headers
)
```

**Response:**

```json
{
    "isDevMode": false,
    "dalBaseUrl": "https://prod-appdx-dal-us.controlup.com",
    "mapApiKey": "AIzaSyB3GOl2dqtnYeb4sTk4LpJH_f3XJoFa3pk",
    "baseUrl": {
        "canadacentral": "https://prod-appdx-dal-ca.controlup.com",
        "eu": "https://prod-appdx-dal-eu.controlup.com",
        "us": "https://prod-appdx-dal-us.controlup.com"
    }
}
```
