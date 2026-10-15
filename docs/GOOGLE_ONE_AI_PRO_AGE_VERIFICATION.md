# Google One 5TB / AI Pro Ineligible Quota & Age Verification Fix

[![Language](https://img.shields.io/badge/Language-فارسی-purple.svg)](GOOGLE_ONE_AI_PRO_AGE_VERIFICATION_FA.md)
[![Status](https://img.shields.io/badge/Status-Verified%20100%25-brightgreen.svg)](#)

![Visual Troubleshooting Guide](../assets/age_verification_guide.png)

## 📌 The Problem

Developers subscribing to the **Google One 5TB AI Pro Plan** (including special provider bundles like Jio or direct subscriptions) often find that their Antigravity IDE or local AI model router (e.g. 9router) fails to detect the paid plan, remaining stuck on `free-tier` (Starter Quota):

```json
HTTP 403 Forbidden: #3501 SUBSCRIPTION_REQUIRED
{
  "error": {
    "code": 403,
    "message": "This account is ineligible for higher rate limits through a Google AI plan at this time.",
    "status": "PERMISSION_DENIED"
  }
}
```

Or when inspecting the internal `loadCodeAssist` RPC response:

```json
"paidTier": {
  "id": "free-tier",
  "name": "Antigravity Starter Quota",
  "upgradeSubscriptionUri": "https://antigravity.google/docs/faq#why-am-i-ineligible-for-google-one-ai-quotas-even-though-i-am-a-subscribed-to-a-plan"
}
```

---

## 🔍 Root Cause Analysis

Google enforces strict separation between consumer storage quotas (**Google Drive**) and developer AI model endpoints (**Cloud Code / Antigravity**):

1. **Storage Tier:** 5TB storage activates instantly upon payment without requiring age verification.
2. **Developer AI Quotas (Gemini Pro & Claude):** International AI safety regulations (such as COPPA and emerging AI governance standards) legally mandate **verified adult status (18+ years)** for access to advanced developer code-generation tiers.
3. **Automatic Fallback to Free-Tier:** If an account has an unverified date of birth, a birth year indicating <18 years of age, or an unverified payment profile, Google Cloud Code servers (`cloudcode-pa.googleapis.com`) flag the account as **Ineligible** and lock developer quotas to `free-tier`, completely ignoring the active 5TB subscription.

---

## 🛠️ Direct Diagnostic Check

You can verify the exact tier Google's backend assigns to your OAuth access token using a direct API query:

```bash
curl -X POST https://cloudcode-pa.googleapis.com/v1internal:loadCodeAssist \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: antigravity/ide/2.11.0 darwin/arm64" \
  -d "{}"
```

* If `paidTier.id` is `free-tier` and `upgradeSubscriptionUri` points to the `ineligible-for-google-one-ai-quotas` FAQ, age verification is the blocking factor.

---

## ⚠️ Bypassing Google Multi-Account Redirects

Clicking standard Google account security links will frequently redirect your browser to your primary logged-in profile (`/u/0/`), preventing changes to the target account.

### Workarounds:
1. **Incognito Mode (Fastest):** Press `Ctrl + Shift + N` (or `Cmd + Shift + N` on macOS) to open a private window and sign in exclusively with the target account.
2. **Direct `authuser` Parameter:** Append `?authuser=YOUR_EMAIL` directly to the URL:
   * `https://myaccount.google.com/birthday?authuser=your_email@gmail.com`
   * `https://myaccount.google.com/age-verification?authuser=your_email@gmail.com`
3. **Dedicated Browser Profile:** Create a separate Google Chrome profile for that specific account.

---

## 🚀 Step-by-Step Resolution

### Step 1: Set Date of Birth (18+ Years)
1. Open Google Birthday settings:  
   `https://myaccount.google.com/birthday?authuser=YOUR_EMAIL`
2. Ensure the birth year is set before 2006 (e.g. **1995**) and save.

### Step 2: Complete Age Verification
1. Navigate to Google's official Age Verification page:  
   `https://myaccount.google.com/age-verification?authuser=YOUR_EMAIL`
2. Complete verification via credit card or government ID if prompted until confirmed.

### Step 3: Refresh Antigravity Session
Once age verification is completed:
* **Antigravity IDE:** Press `Ctrl + Shift + P` -> run `Antigravity: Reset Onboarding`, sign in again, and launch a new chat session.
* **Local Router / Proxy:** Re-authenticate or trigger an access token refresh.

---

## ✅ Verified Post-Fix Result

Google's internal backend updates in real-time. Immediately following age verification:

```json
"paidTier": {
  "id": "g1-pro-tier",
  "name": "Google AI Pro",
  "description": "Google AI Pro",
  "availableCredits": [
    {
      "creditType": "GOOGLE_ONE_AI",
      "minimumCreditAmountForUsage": "50"
    }
  ]
}
```

Queries to `retrieveUserQuotaSummary` immediately return **`HTTP 200 OK`**, fully unlocking 100% of weekly and 5-hour quotas for Gemini Pro and Claude.
