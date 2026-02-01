# Testing Checklist

Use this checklist to thoroughly test WorkHub Bot before production deployment.

## Pre-Testing Setup

- [ ] Bot is running without errors
- [ ] Supabase connection working
- [ ] Test channel created and bot is admin
- [ ] Test environment variables configured
- [ ] Test admin account set up

## Start & Verification Tests

### New User Registration
- [ ] Send `/start` command
- [ ] Welcome message appears with proper formatting
- [ ] Join Channel button works
- [ ] Channel link is correct
- [ ] Verify Join button works after joining
- [ ] Verification succeeds when user is member
- [ ] Verification fails when user is not member
- [ ] Error message is clear when verification fails
- [ ] User is saved to database with correct role
- [ ] Default role is 'taker'

### Existing User
- [ ] Send `/start` as existing user
- [ ] Bot recognizes returning user
- [ ] Shows appropriate dashboard based on role
- [ ] No duplicate user entries in database

### Admin Detection
- [ ] Admin UID is set in config
- [ ] Admin user gets admin dashboard
- [ ] Admin role is set correctly in database

## Provider Registration Tests

### Registration Flow
- [ ] Click "Register as Provider"
- [ ] Name input prompt appears
- [ ] Accepts valid names
- [ ] Mobile number validation works
- [ ] Rejects invalid mobile numbers
- [ ] Email validation works
- [ ] Rejects invalid emails
- [ ] Gender selection works (Male/Female/Other)
- [ ] DOB accepts valid format (YYYY-MM-DD)
- [ ] Rejects invalid date formats
- [ ] Location input works
- [ ] Password validation works (min 6 chars)
- [ ] Password confirmation works
- [ ] Rejects mismatched passwords
- [ ] Referral code validation works
- [ ] Can skip referral code
- [ ] Registration success message shows
- [ ] User role updates to 'provider'
- [ ] Data saved correctly in database
- [ ] Referral bonus awarded if valid code used

### After Registration
- [ ] Provider dashboard shows
- [ ] All provider buttons appear
- [ ] Wallet balance shows (0.00)

## Task Creation Tests (Provider)

### Task Creation Flow
- [ ] "Create New Task" button works
- [ ] Task title input accepted
- [ ] Task description input accepted
- [ ] Categories load correctly
- [ ] Category selection works
- [ ] Reward amount accepts numbers
- [ ] Rejects invalid amounts (negative, text)
- [ ] Worker slots accepts numbers
- [ ] Rejects invalid slots
- [ ] Requirements input accepted

### Task Creation with Balance
- [ ] Creates task when balance sufficient
- [ ] Shows task details after creation
- [ ] Amount deducted from wallet
- [ ] Transaction recorded in database
- [ ] Task appears in database with correct data

### Task Creation without Balance
- [ ] Shows error when balance insufficient
- [ ] Error message shows required amount
- [ ] No task created
- [ ] No money deducted

### View Tasks
- [ ] "View My Tasks" shows created tasks
- [ ] Task details display correctly
- [ ] Category names show
- [ ] Filled/total slots show
- [ ] Task status shows
- [ ] Shows "no tasks" when none exist

## Worker/Taker Tests

### Browse Tasks
- [ ] "Get New Task" shows categories
- [ ] "All Tasks" option works
- [ ] Category buttons work
- [ ] Available tasks display correctly
- [ ] Task details are complete
- [ ] Provider name shows
- [ ] Reward amount shows
- [ ] Available slots show
- [ ] Shows "no tasks" when none available

### Accept Task
- [ ] "Take Task" button works
- [ ] Task accepted successfully
- [ ] Confirmation message shows
- [ ] Task requirements displayed
- [ ] Assignment saved to database
- [ ] Task filled_slots incremented
- [ ] Cannot accept same task twice
- [ ] Cannot accept full tasks

### View My Tasks
- [ ] "My Tasks" shows accepted tasks
- [ ] Task status shows correctly (accepted/submitted/approved/rejected)
- [ ] Status emojis display
- [ ] Can submit tasks with "accepted" status
- [ ] Shows "no tasks" when none

### Submit Task Proof
- [ ] "Submit" button works
- [ ] Document upload prompt shows
- [ ] Can upload valid documents (PDF, DOCX, PNG, JPG)
- [ ] Rejects oversized documents (>300KB)
- [ ] Can skip document
- [ ] Video upload prompt shows
- [ ] Can upload valid videos (MP4)
- [ ] Rejects oversized videos (>10MB)
- [ ] Can skip video
- [ ] Requires at least one file (doc or video)
- [ ] Shows error if both skipped
- [ ] Success message shows after submission
- [ ] Status updates to "submitted"
- [ ] Files saved to Supabase storage
- [ ] URLs saved in database
- [ ] Provider receives notification

## Wallet Tests

### View Wallet
- [ ] "Wallet" button works
- [ ] Balance displays correctly
- [ ] Recent transactions show
- [ ] Transaction types show correct emoji
- [ ] Transaction amounts show with +/-
- [ ] Dates formatted correctly
- [ ] "All Transactions" button works
- [ ] Shows all transactions with details

### Add Balance
- [ ] "Add Balance" button works
- [ ] Amount input prompt shows
- [ ] Accepts valid amounts (1-10000)
- [ ] Rejects amounts outside range
- [ ] Payment method selection shows
- [ ] UPI option works
- [ ] Shows UPI ID
- [ ] Shows QR code (if configured)
- [ ] Crypto option works
- [ ] Shows wallet address
- [ ] 2-minute delay works
- [ ] UTR input prompt shows after delay
- [ ] Transaction saved with status "pending"
- [ ] Transaction appears in wallet history

### Withdraw
- [ ] "Withdraw" button works
- [ ] Checks minimum balance (150)
- [ ] Shows error if balance insufficient
- [ ] Method selection works (UPI/Bank/Crypto)
- [ ] Details input accepted for each method
- [ ] Amount input accepted
- [ ] Validates amount against balance
- [ ] Amount deducted immediately
- [ ] Transaction saved as "pending"
- [ ] Shows success message

## Referral Tests

### Referral System
- [ ] "Refer & Earn" shows referral code
- [ ] Referral code is unique per user
- [ ] Share message formatted correctly
- [ ] New user can use referral code
- [ ] Referrer gets bonus (50)
- [ ] Referral transaction created
- [ ] Referral record saved
- [ ] Bonus shows in wallet
- [ ] Cannot refer self
- [ ] Cannot use invalid codes

## Admin Dashboard Tests

### View Users
- [ ] "View All Users" works
- [ ] Shows user count statistics
- [ ] Shows role breakdown
- [ ] Lists recent users
- [ ] Shows verification status
- [ ] Shows wallet balance
- [ ] Data matches database

### View Tasks
- [ ] "View All Tasks" works
- [ ] Shows total task count
- [ ] Lists tasks with details
- [ ] Shows provider names
- [ ] Shows categories
- [ ] Shows slots and status
- [ ] Data matches database

### Approve Transactions
- [ ] "Approve Transactions" shows pending only
- [ ] Shows transaction details
- [ ] Approve button works
- [ ] Balance updated on approval
- [ ] Status changes to "approved"
- [ ] User notified (if applicable)
- [ ] Reject button works
- [ ] Balance refunded on withdrawal rejection
- [ ] Status changes to "rejected"

### Approve Task Proofs
- [ ] "Approve Task Proofs" shows submitted tasks
- [ ] Shows task details
- [ ] Shows worker name
- [ ] Shows file indicators (doc/video)
- [ ] Approve button works
- [ ] Worker receives payment
- [ ] Status changes to "approved"
- [ ] Reject button prompts for reason
- [ ] Rejection reason saved
- [ ] Status changes to "rejected"
- [ ] Worker notified (if applicable)

### Payment Info Management
- [ ] "Manage Payment Info" shows current info
- [ ] Displays UPI details
- [ ] Displays Crypto details
- [ ] Update buttons work (basic check)

### Categories
- [ ] "Manage Categories" shows all categories
- [ ] Shows active/inactive status
- [ ] Shows category count

### Referrals
- [ ] "View Referrals" shows all referrals
- [ ] Shows total count
- [ ] Shows total bonuses paid
- [ ] Lists recent referrals
- [ ] Shows referrer names
- [ ] Shows status

### Support Messages
- [ ] "Support Messages" shows all messages
- [ ] Shows user names
- [ ] Shows message preview
- [ ] Shows status
- [ ] Shows dates

## Support Tests

### Submit Support Message
- [ ] "Support" button works
- [ ] Message input prompt shows
- [ ] Message submitted successfully
- [ ] Saved to database
- [ ] Status is "open"
- [ ] Success message shows
- [ ] Appears in admin dashboard

## Error Handling Tests

### Invalid Inputs
- [ ] Handles text where numbers expected
- [ ] Handles negative numbers
- [ ] Handles empty inputs
- [ ] Handles special characters
- [ ] Shows clear error messages

### Database Errors
- [ ] Handles connection failures gracefully
- [ ] Shows user-friendly error messages
- [ ] Logs errors for debugging

### File Upload Errors
- [ ] Handles invalid file types
- [ ] Handles oversized files
- [ ] Shows clear error messages

### Network Errors
- [ ] Handles Telegram API errors
- [ ] Handles Supabase errors
- [ ] Recovers gracefully

## Security Tests

### Authentication
- [ ] Non-verified users can't access features
- [ ] Admin features only for admin
- [ ] Cannot access other users' data

### Data Validation
- [ ] SQL injection attempts fail
- [ ] XSS attempts fail
- [ ] Password is hashed
- [ ] Sensitive data not logged

### Transaction Security
- [ ] Cannot manipulate wallet balance directly
- [ ] Cannot approve own transactions (as user)
- [ ] Amount validations work
- [ ] Double-spending prevented

## Performance Tests

### Response Time
- [ ] Commands respond within 2 seconds
- [ ] Database queries are fast
- [ ] File uploads complete reasonably
- [ ] No timeout errors under normal load

### Concurrent Users
- [ ] Multiple users can use bot simultaneously
- [ ] No race conditions in wallet operations
- [ ] Database handles concurrent requests

## Edge Cases

### Special Scenarios
- [ ] User stops bot and restarts
- [ ] User sends random text during conversation
- [ ] User sends /cancel during registration
- [ ] Task becomes full while user is viewing
- [ ] Provider deletes task (N/A - requires implementation)
- [ ] Multiple referrals at same time
- [ ] Zero balance operations
- [ ] Maximum values for amounts

## Production Readiness

### Configuration
- [ ] All environment variables set
- [ ] Production Supabase project used
- [ ] Real payment information configured
- [ ] Admin UID is correct
- [ ] Channel is production channel

### Documentation
- [ ] README is complete
- [ ] All credentials documented
- [ ] Backup procedures documented
- [ ] Recovery procedures documented

### Monitoring
- [ ] Logging is working
- [ ] Error tracking configured
- [ ] Uptime monitoring set up
- [ ] Database backups enabled

### Deployment
- [ ] Deployed to stable server
- [ ] Auto-restart configured
- [ ] HTTPS (if using webhooks)
- [ ] Firewall configured
- [ ] Backup server ready

## Post-Launch Monitoring

### Week 1
- [ ] Monitor error logs daily
- [ ] Check transaction approvals daily
- [ ] Review support messages
- [ ] Monitor wallet operations
- [ ] Check database size

### Ongoing
- [ ] Weekly backup verification
- [ ] Monthly security review
- [ ] User feedback collection
- [ ] Performance monitoring
- [ ] Feature requests tracking

## Test Summary

After completing all tests:

- Total tests: ___
- Passed: ___
- Failed: ___
- Skipped: ___

### Critical Issues Found:
1. 
2. 
3. 

### Non-Critical Issues:
1. 
2. 
3. 

### Recommendations:
1. 
2. 
3. 

---

**Tester Name**: ________________
**Test Date**: ________________
**Environment**: ☐ Development ☐ Staging ☐ Production
**Status**: ☐ Ready for Production ☐ Needs Work ☐ Blocked

