# WorkHub Bot - Complete Flow Diagram

## 📱 Bot Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      TELEGRAM BOT INTERFACE                      │
│                         (bot.py)                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     HANDLER LAYER                                │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │  Start   │ Provider │  Taker   │  Wallet  │  Admin   │      │
│  │ Handlers │ Handlers │ Handlers │ Handlers │ Handlers │      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│                   (database.py)                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Supabase Client - CRUD Operations                    │      │
│  └──────────────────────────────────────────────────────┘      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SUPABASE BACKEND                            │
│  ┌─────────────────────┬──────────────────────────────┐        │
│  │  PostgreSQL DB      │  Storage (Files)              │        │
│  │  • users            │  • task-documents             │        │
│  │  • tasks            │  • task-videos                │        │
│  │  • assignments      │                               │        │
│  │  • transactions     │                               │        │
│  │  • referrals        │                               │        │
│  │  • categories       │                               │        │
│  │  • support          │                               │        │
│  │  • payment_info     │                               │        │
│  └─────────────────────┴──────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 User Journey Flows

### 1. First-Time User Flow

```
/start
  │
  ├──> Welcome Message
  │     └──> "Join Channel" Button
  │     └──> "Verify Join" Button  
  │     └──> "Read Terms" Button
  │
  ├──> User Clicks "Join Channel"
  │     └──> Opens Telegram Channel
  │     └──> User Joins
  │
  ├──> User Clicks "Verify Join"
  │     └──> Bot Checks Membership
  │          ├──> ✅ Joined → Set is_verified = true
  │          └──> ❌ Not Joined → Show Error
  │
  └──> Show Main Menu
        ├──> Provider Dashboard (if no name/email)
        │     └──> "Register as Provider" Button
        │
        └──> Taker Dashboard (if no name)
              └──> "Complete Registration" Button
```

### 2. Provider Registration Flow

```
Click "Register as Provider"
  │
  ├──> Enter Name
  ├──> Enter Mobile (with validation)
  ├──> Enter Email (with validation)
  ├──> Select Gender (Male/Female/Other)
  ├──> Enter DOB (YYYY-MM-DD)
  ├──> Enter Location
  ├──> Enter Password (min 6 chars)
  ├──> Confirm Password
  └──> Enter Referral Code (optional)
       │
       ├──> If Referral Valid:
       │     ├──> Link to referrer
       │     ├──> Give ₹50 bonus to referrer
       │     └──> Update referrals table
       │
       └──> Registration Complete
            └──> Show Provider Dashboard
```

### 3. Worker/Taker Registration Flow

```
Click "Complete Registration"
  │
  ├──> Enter Name
  ├──> Enter Mobile (with validation)
  ├──> Enter DOB (YYYY-MM-DD)
  ├──> Enter Password (min 6 chars)
  ├──> Confirm Password
  └──> Enter Referral Code (optional)
       │
       ├──> If Referral Valid:
       │     ├──> Link to referrer
       │     ├──> Give ₹50 bonus to referrer
       │     └──> Update referrals table
       │
       └──> Registration Complete
            └──> Show Worker Dashboard
```

### 4. Task Creation Flow (Provider)

```
Provider Dashboard → "Create New Task"
  │
  ├──> Enter Task Title
  ├──> Enter Task Description
  ├──> Select Category
  ├──> Enter Reward Amount (₹)
  ├──> Enter Number of Workers
  └──> Enter Requirements
       │
       ├──> Calculate Total Cost = Reward × Workers
       │
       ├──> Check Wallet Balance
       │     ├──> ✅ Sufficient → Proceed
       │     └──> ❌ Insufficient → Show Error
       │
       ├──> Deduct Amount from Wallet
       ├──> Create Transaction Record
       │     └──> type = 'task_deduction'
       │
       ├──> Create Task in Database
       │     └──> status = 'available'
       │
       └──> Show Success Message
            └──> Display New Balance
```

### 5. Task Completion Flow (Worker)

```
Worker Dashboard → "Get New Task"
  │
  ├──> Show Categories
  │     └──> "All Tasks" / "Category 1" / "Category 2"...
  │
  ├──> User Selects Category
  │     └──> Show Available Tasks
  │          ├──> Task Title
  │          ├──> Reward Amount
  │          ├──> Provider Name
  │          ├──> Available Slots
  │          └──> Description
  │
  ├──> User Clicks "Take Task"
  │     ├──> Create Assignment Record
  │     │     └──> status = 'accepted'
  │     ├──> Increment filled_slots
  │     └──> Show Success + Requirements
  │
  └──> Worker Dashboard → "My Tasks"
       │
       ├──> Show All Tasks
       │     ├──> 🆕 Accepted (not submitted)
       │     ├──> ⏳ Submitted (pending review)
       │     ├──> ✅ Approved (paid)
       │     └──> ❌ Rejected
       │
       └──> Click "Submit Task"
            │
            ├──> Upload Document (optional)
            │     ├──> Max 300 KB
            │     ├──> Download from Telegram
            │     ├──> Upload to Supabase Storage
            │     └──> Save URL
            │
            ├──> Upload Video (optional)
            │     ├──> Max 10 MB
            │     ├──> Download from Telegram
            │     ├──> Upload to Supabase Storage
            │     └──> Save URL
            │
            ├──> At Least One File Required
            │
            ├──> Update Assignment
            │     ├──> status = 'submitted'
            │     ├──> submitted_at = now()
            │     ├──> proof_file_url = ...
            │     └──> proof_video_url = ...
            │
            └──> Send Notification to Provider
                 └──> "Worker [Name] submitted proof for [Task]"
```

### 6. Wallet Deposit Flow

```
Dashboard → "Wallet" → "Add Balance"
  │
  ├──> Enter Amount
  │     ├──> Min: ₹1
  │     └──> Max: ₹10,000
  │
  ├──> Select Payment Method
  │     ├──> UPI
  │     │     ├──> Show UPI ID from admin
  │     │     ├──> Generate/Show QR Code
  │     │     └──> "Scan & Pay"
  │     │
  │     └──> Crypto
  │           ├──> Show Wallet Address from admin
  │           ├──> Show Network (USDT-TRC20)
  │           └──> "Transfer & Submit"
  │
  ├──> Wait 2 Minutes
  │     └──> Show countdown/message
  │
  ├──> Prompt for UTR/Transaction ID
  │     └──> User enters UTR
  │
  ├──> Create Transaction Record
  │     ├──> type = 'deposit'
  │     ├──> status = 'pending'
  │     ├──> amount = ...
  │     ├──> payment_method = ...
  │     └──> utr_transaction_id = ...
  │
  └──> Show Pending Message
       └──> "Admin will verify within 24-48 hours"
```

### 7. Admin Approval Flow (Transaction)

```
Admin Dashboard → "Approve Transactions"
  │
  ├──> Show All Pending Transactions
  │     ├──> User Name
  │     ├──> Type (Deposit/Withdrawal)
  │     ├──> Amount
  │     ├──> Payment Method
  │     ├──> UTR
  │     └──> Date
  │
  ├──> Admin Clicks "Approve"
  │     ├──> Update Transaction
  │     │     └──> status = 'approved'
  │     │
  │     ├──> If Deposit:
  │     │     └──> Add to User Wallet Balance
  │     │
  │     └──> If Withdrawal:
  │           └──> Keep Balance (already deducted)
  │
  └──> Admin Clicks "Reject"
        ├──> Update Transaction
        │     └──> status = 'rejected'
        │
        └──> If Withdrawal:
              └──> Refund to User Wallet Balance
```

### 8. Admin Approval Flow (Task Proof)

```
Admin Dashboard → "Approve Task Proofs"
  │
  ├──> Show All Pending Submissions
  │     ├──> Worker Name
  │     ├──> Task Title
  │     ├──> Reward Amount
  │     ├──> Submission Date
  │     ├──> Document Status (✅/❌)
  │     └──> Video Status (✅/❌)
  │
  ├──> Admin Clicks "Approve"
  │     ├──> Update Assignment
  │     │     ├──> status = 'approved'
  │     │     └──> reviewed_at = now()
  │     │
  │     ├──> Add Reward to Worker Wallet
  │     │
  │     ├──> Create Transaction Record
  │     │     ├──> type = 'task_payment'
  │     │     ├──> status = 'approved'
  │     │     └──> amount = reward
  │     │
  │     └──> Send Notification to Worker
  │          └──> "🎉 Task approved! ₹[reward] added to wallet"
  │
  └──> Admin Clicks "Reject"
        ├──> Prompt for Rejection Reason
        │     └──> Admin enters reason
        │
        ├──> Update Assignment
        │     ├──> status = 'rejected'
        │     ├──> reviewed_at = now()
        │     └──> rejection_reason = ...
        │
        └──> Send Notification to Worker
             └──> "❌ Task rejected. Reason: [reason]"
```

### 9. Referral System Flow

```
User Registration (Provider or Taker)
  │
  ├──> User Enters Referral Code
  │     └──> If code is valid:
  │
  ├──> Find Referrer by Code
  │     ├──> referrer = get_user_by_referral_code(code)
  │     └──> If found:
  │
  ├──> Create Referral Record
  │     ├──> referrer_id = referrer.id
  │     ├──> referred_id = new_user.id
  │     ├──> bonus_amount = ₹50
  │     └──> status = 'rewarded'
  │
  ├──> Add ₹50 to Referrer Wallet
  │     └──> Update referrer.wallet_balance
  │
  ├──> Create Transaction Record
  │     ├──> type = 'referral_bonus'
  │     ├──> status = 'approved'
  │     └──> amount = ₹50
  │
  └──> Link New User to Referrer
       └──> new_user.referred_by = referrer.id
```

## 🔔 Notification Flow

```
┌─────────────────────────────────────────────────────────┐
│                    NOTIFICATION TRIGGERS                 │
└─────────────────────────────────────────────────────────┘
            │
            ├──> Worker Submits Proof
            │     └──> Send to Provider:
            │          └──> "Worker [Name] submitted proof for [Task]"
            │
            ├──> Admin Approves Task
            │     └──> Send to Worker:
            │          └──> "🎉 Task approved! ₹[reward] added"
            │
            └──> Admin Rejects Task
                  └──> Send to Worker:
                       └──> "❌ Task rejected. Reason: [reason]"
```

## 📊 Dashboard Structure

### Provider Dashboard
```
┌─────────────────────────────────────────┐
│     👔 PROVIDER DASHBOARD                │
│  Welcome, [Name]!                        │
│  💰 Balance: ₹[amount]                   │
│                                          │
│  [➕ Create New Task]                    │
│  [📋 View My Tasks]                      │
│  [💰 Wallet]                             │
│  [🎁 Refer & Earn]                       │
│  [📢 Run Campaign]                       │
│  [📊 Lifetime Earn]                      │
│  [💬 Support]                            │
└─────────────────────────────────────────┘
```

### Worker/Taker Dashboard
```
┌─────────────────────────────────────────┐
│     🎯 WORK TAKER DASHBOARD              │
│  Welcome, [Name]!                        │
│  💰 Balance: ₹[amount]                   │
│                                          │
│  [🎯 Get New Task]                       │
│  [📝 My Tasks]                           │
│  [💰 Wallet]                             │
│  [🎁 Refer & Earn]                       │
│  [💬 Support]                            │
│  [👔 Register as Provider]               │
└─────────────────────────────────────────┘
```

### Admin Dashboard
```
┌─────────────────────────────────────────┐
│     🔧 ADMIN DASHBOARD                   │
│  Welcome back, Admin!                    │
│                                          │
│  [👥 View All Users]                     │
│  [📋 View All Tasks]                     │
│  [✅ Approve Transactions]               │
│  [💬 Support Messages]                   │
│  [⚙️ Manage Payment Info]                │
│  [📂 Manage Categories]                  │
│  [📊 View Referrals]                     │
│  [✔️ Approve Task Proofs]                │
└─────────────────────────────────────────┘
```

## 💾 Data Flow

### Task Creation
```
Provider → Bot → Database → Wallet
   │         │       │         │
   │         │       ├─> Create task record
   │         │       └─> Create transaction
   │         │
   │         └─> Validate balance
   │
   └─> Enter task details
```

### Task Submission
```
Worker → Bot → Telegram → Supabase Storage → Database → Provider
  │       │       │           │                 │          │
  │       │       │           ├─> Save document │          │
  │       │       │           └─> Save video    │          │
  │       │       │                             │          │
  │       │       └─> Download files            │          │
  │       │                                     │          │
  │       └─> Handle upload                     └─> Update │
  │                                                   assignment
  │                                                         │
  └─> Upload files                                         │
                                                            │
                                                  Send notification
```

### Payment Flow
```
User → Bot → Database → Admin → Database → User
  │      │       │        │        │         │
  │      │       │        │        └─> Update balance
  │      │       │        │
  │      │       │        └─> Approve/Reject
  │      │       │
  │      │       └─> Create transaction
  │      │
  │      └─> Show payment details
  │
  └─> Initiate deposit/withdrawal
```

## 🔄 State Management

### ConversationHandler States

#### Provider Registration
```
PROVIDER_NAME
  → PROVIDER_MOBILE
    → PROVIDER_EMAIL
      → PROVIDER_GENDER
        → PROVIDER_DOB
          → PROVIDER_LOCATION
            → PROVIDER_PASSWORD
              → PROVIDER_CONFIRM_PASSWORD
                → PROVIDER_REFERRAL
                  → END
```

#### Worker Registration
```
TAKER_NAME
  → TAKER_MOBILE
    → TAKER_DOB
      → TAKER_PASSWORD
        → TAKER_CONFIRM_PASSWORD
          → TAKER_REFERRAL
            → END
```

#### Task Creation
```
TASK_TITLE
  → TASK_DESCRIPTION
    → TASK_CATEGORY
      → TASK_REWARD
        → TASK_SLOTS
          → TASK_REQUIREMENTS
            → END
```

#### Task Submission
```
SUBMIT_PROOF_DOC
  → SUBMIT_PROOF_VIDEO
    → END
```

#### Wallet Deposit
```
DEPOSIT_AMOUNT
  → DEPOSIT_METHOD
    → DEPOSIT_UTR
      → END
```

#### Wallet Withdrawal
```
WITHDRAW_METHOD
  → WITHDRAW_DETAILS
    → WITHDRAW_AMOUNT
      → END
```

---

**This flow diagram provides a complete visual representation of how the WorkHub bot operates.**
