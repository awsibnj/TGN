from supabase import create_client, Client
import config
import hashlib
import random
import string

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def generate_referral_code(telegram_uid):
    base = f"{telegram_uid}{random.randint(1000, 9999)}"
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_telegram_uid(telegram_uid):
    try:
        response = supabase.table('users').select('*').eq('telegram_uid', telegram_uid).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def create_user(telegram_uid, username, role='taker', is_verified=False):
    try:
        referral_code = generate_referral_code(telegram_uid)
        data = {
            'telegram_uid': telegram_uid,
            'username': username,
            'role': role,
            'is_verified': is_verified,
            'referral_code': referral_code
        }
        response = supabase.table('users').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def update_user(user_id, updates):
    try:
        response = supabase.table('users').update(updates).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating user: {e}")
        return None

def verify_user(telegram_uid):
    try:
        response = supabase.table('users').update({'is_verified': True}).eq('telegram_uid', telegram_uid).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

def get_all_categories():
    try:
        response = supabase.table('categories').select('*').eq('is_active', True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

def create_task(provider_id, title, description, category_id, reward, total_slots, requirements, deadline=None):
    try:
        data = {
            'provider_id': provider_id,
            'title': title,
            'description': description,
            'category_id': category_id,
            'reward': reward,
            'total_slots': total_slots,
            'requirements': requirements,
            'deadline': deadline
        }
        response = supabase.table('tasks').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating task: {e}")
        return None

def get_tasks_by_provider(provider_id):
    try:
        response = supabase.table('tasks').select('*, categories(name)').eq('provider_id', provider_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting provider tasks: {e}")
        return []

def get_available_tasks(category_id=None):
    try:
        query = supabase.table('tasks').select('*, categories(name), users!tasks_provider_id_fkey(name)').eq('status', 'available')
        if category_id:
            query = query.eq('category_id', category_id)
        response = query.order('created_at', desc=True).execute()
        return [task for task in (response.data if response.data else []) if task['filled_slots'] < task['total_slots']]
    except Exception as e:
        print(f"Error getting available tasks: {e}")
        return []

def create_task_assignment(task_id, taker_id):
    try:
        data = {
            'task_id': task_id,
            'taker_id': taker_id,
            'status': 'accepted'
        }
        response = supabase.table('task_assignments').insert(data).execute()
        
        if response.data:
            supabase.table('tasks').update({
                'filled_slots': supabase.table('tasks').select('filled_slots').eq('id', task_id).execute().data[0]['filled_slots'] + 1
            }).eq('id', task_id).execute()
            
            task = supabase.table('tasks').select('filled_slots, total_slots').eq('id', task_id).execute().data[0]
            if task['filled_slots'] >= task['total_slots']:
                supabase.table('tasks').update({'status': 'completed'}).eq('id', task_id).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating task assignment: {e}")
        return None

def get_task_assignments_by_taker(taker_id):
    try:
        response = supabase.table('task_assignments').select('*, tasks(title, description, reward, categories(name))').eq('taker_id', taker_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting taker assignments: {e}")
        return []

def update_task_assignment(assignment_id, updates):
    try:
        response = supabase.table('task_assignments').update(updates).eq('id', assignment_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating task assignment: {e}")
        return None

def create_wallet_transaction(user_id, transaction_type, amount, payment_method=None, payment_details=None, utr_transaction_id=None):
    try:
        data = {
            'user_id': user_id,
            'transaction_type': transaction_type,
            'amount': amount,
            'payment_method': payment_method,
            'payment_details': payment_details,
            'utr_transaction_id': utr_transaction_id,
            'status': 'pending'
        }
        response = supabase.table('wallet_transactions').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating wallet transaction: {e}")
        return None

def get_wallet_transactions(user_id):
    try:
        response = supabase.table('wallet_transactions').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting wallet transactions: {e}")
        return []

def update_wallet_balance(user_id, amount):
    try:
        user = supabase.table('users').select('wallet_balance').eq('id', user_id).execute().data[0]
        new_balance = float(user['wallet_balance']) + float(amount)
        response = supabase.table('users').update({'wallet_balance': new_balance}).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating wallet balance: {e}")
        return None

def create_referral(referrer_id, referred_id):
    try:
        data = {
            'referrer_id': referrer_id,
            'referred_id': referred_id,
            'bonus_amount': config.REFERRAL_BONUS,
            'status': 'rewarded'
        }
        response = supabase.table('referrals').insert(data).execute()
        
        if response.data:
            update_wallet_balance(referrer_id, config.REFERRAL_BONUS)
            create_wallet_transaction(
                referrer_id,
                'referral_bonus',
                config.REFERRAL_BONUS,
                payment_method='referral',
                payment_details={'referred_user_id': referred_id}
            )
            supabase.table('wallet_transactions').update({'status': 'approved'}).eq('user_id', referrer_id).eq('transaction_type', 'referral_bonus').eq('amount', config.REFERRAL_BONUS).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating referral: {e}")
        return None

def get_user_by_referral_code(referral_code):
    try:
        response = supabase.table('users').select('*').eq('referral_code', referral_code).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user by referral code: {e}")
        return None

def create_support_message(user_id, message):
    try:
        data = {
            'user_id': user_id,
            'message': message,
            'status': 'open'
        }
        response = supabase.table('support_messages').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating support message: {e}")
        return None

def get_payment_info(payment_type):
    try:
        response = supabase.table('payment_info').select('*').eq('payment_type', payment_type).eq('is_active', True).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting payment info: {e}")
        return None

def get_all_users(role=None):
    try:
        query = supabase.table('users').select('*')
        if role:
            query = query.eq('role', role)
        response = query.order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []

def get_all_tasks():
    try:
        response = supabase.table('tasks').select('*, categories(name), users!tasks_provider_id_fkey(name, telegram_uid)').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting all tasks: {e}")
        return []

def get_all_task_assignments():
    try:
        response = supabase.table('task_assignments').select('*, tasks(title, reward), users!task_assignments_taker_id_fkey(name, telegram_uid)').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting all task assignments: {e}")
        return []

def get_pending_wallet_transactions():
    try:
        response = supabase.table('wallet_transactions').select('*, users(name, telegram_uid)').eq('status', 'pending').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting pending transactions: {e}")
        return []

def approve_wallet_transaction(transaction_id, admin_note=None):
    try:
        transaction = supabase.table('wallet_transactions').select('*').eq('id', transaction_id).execute().data[0]
        
        updates = {'status': 'approved', 'admin_note': admin_note}
        response = supabase.table('wallet_transactions').update(updates).eq('id', transaction_id).execute()
        
        if response.data:
            if transaction['transaction_type'] == 'deposit':
                update_wallet_balance(transaction['user_id'], transaction['amount'])
            elif transaction['transaction_type'] == 'withdrawal':
                pass
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error approving transaction: {e}")
        return None

def reject_wallet_transaction(transaction_id, admin_note=None):
    try:
        transaction = supabase.table('wallet_transactions').select('*').eq('id', transaction_id).execute().data[0]
        
        updates = {'status': 'rejected', 'admin_note': admin_note}
        response = supabase.table('wallet_transactions').update(updates).eq('id', transaction_id).execute()
        
        if response.data and transaction['transaction_type'] == 'withdrawal':
            update_wallet_balance(transaction['user_id'], transaction['amount'])
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error rejecting transaction: {e}")
        return None

def get_all_support_messages():
    try:
        response = supabase.table('support_messages').select('*, users(name, telegram_uid)').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting support messages: {e}")
        return []

def update_support_message(message_id, admin_reply):
    try:
        updates = {'admin_reply': admin_reply, 'status': 'replied'}
        response = supabase.table('support_messages').update(updates).eq('id', message_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating support message: {e}")
        return None

def update_payment_info(payment_type, details):
    try:
        response = supabase.table('payment_info').update({'details': details}).eq('payment_type', payment_type).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating payment info: {e}")
        return None

def create_category(name, description):
    try:
        data = {'name': name, 'description': description}
        response = supabase.table('categories').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating category: {e}")
        return None

def get_task_by_id(task_id):
    try:
        response = supabase.table('tasks').select('*, users!tasks_provider_id_fkey(name, telegram_uid)').eq('id', task_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting task: {e}")
        return None

def approve_task_submission(assignment_id):
    try:
        assignment = supabase.table('task_assignments').select('*, tasks(reward, provider_id, title), users!task_assignments_taker_id_fkey(telegram_uid)').eq('id', assignment_id).execute().data[0]
        
        updates = {'status': 'approved', 'reviewed_at': 'now()'}
        response = supabase.table('task_assignments').update(updates).eq('id', assignment_id).execute()
        
        if response.data:
            reward = float(assignment['tasks']['reward'])
            update_wallet_balance(assignment['taker_id'], reward)
            create_wallet_transaction(
                assignment['taker_id'],
                'task_payment',
                reward,
                payment_method='task_completion',
                payment_details={'assignment_id': assignment_id}
            )
            supabase.table('wallet_transactions').update({'status': 'approved'}).eq('user_id', assignment['taker_id']).eq('transaction_type', 'task_payment').eq('amount', reward).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error approving task submission: {e}")
        return None

def reject_task_submission(assignment_id, rejection_reason):
    try:
        updates = {'status': 'rejected', 'reviewed_at': 'now()', 'rejection_reason': rejection_reason}
        response = supabase.table('task_assignments').update(updates).eq('id', assignment_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error rejecting task submission: {e}")
        return None

def get_referrals_by_referrer(referrer_id):
    try:
        response = supabase.table('referrals').select('*, users!referrals_referred_id_fkey(name, telegram_uid)').eq('referrer_id', referrer_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting referrals: {e}")
        return []

def get_all_referrals():
    try:
        response = supabase.table('referrals').select('*, users!referrals_referrer_id_fkey(name, telegram_uid)').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting all referrals: {e}")
        return []

def upload_file_to_storage(file_bytes, bucket_name, file_path):
    try:
        response = supabase.storage.from_(bucket_name).upload(file_path, file_bytes)
        
        if response:
            public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
            return public_url
        return None
    except Exception as e:
        print(f"Error uploading file to storage: {e}")
        return None

def get_assignment_by_id(assignment_id):
    try:
        response = supabase.table('task_assignments').select('*, tasks(title, reward), users!task_assignments_taker_id_fkey(name, telegram_uid)').eq('id', assignment_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting assignment: {e}")
        return None
