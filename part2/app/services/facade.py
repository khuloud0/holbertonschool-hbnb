def get_all_users(self):
    """Get all users"""
    return self.user_repo.find_all()

def update_user(self, user_id, update_data):
    """Update user data"""
    user = self.user_repo.find_by_id(user_id)
    if not user:
        return None
    
    # Check if new email is not already used
    if 'email' in update_data and update_data['email'] != user.email:
        existing_user = self.user_repo.find_by_email(update_data['email'])
        if existing_user:
            return None
    
    # Update allowed fields
    allowed_fields = ['email', 'first_name', 'last_name']
    for field in allowed_fields:
        if field in update_data:
            setattr(user, field, update_data[field])
    
    # Save the updated user
    self.user_repo.save(user)
    return user
