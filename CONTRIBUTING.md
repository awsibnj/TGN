# Contributing to WorkHub Bot

Thank you for considering contributing to WorkHub Bot! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use case / benefits
   - Possible implementation approach

### Code Contributions

#### Setup Development Environment

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/yourusername/workhub-bot.git
cd workhub-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your test credentials
```

#### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. Make your changes:
   - Follow existing code style
   - Add comments for complex logic
   - Keep functions focused and small
   - Update documentation if needed

3. Test your changes:
```bash
# Run the bot
python bot.py

# Test affected features thoroughly
# Test edge cases
```

4. Commit your changes:
```bash
git add .
git commit -m "feat: add amazing feature"
# or
git commit -m "fix: resolve issue with wallet"
```

#### Commit Message Guidelines

Use conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Examples:
```
feat: add crypto withdrawal support
fix: correct wallet balance calculation
docs: update README with new features
refactor: simplify database queries
```

#### Pull Request Process

1. Push to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create Pull Request:
   - Go to original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template:
     - Description of changes
     - Related issues
     - Testing done
     - Screenshots (if UI changes)

3. Wait for review:
   - Address reviewer comments
   - Make requested changes
   - Update PR as needed

4. Merge:
   - Once approved, PR will be merged
   - Delete your branch after merge

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep line length under 120 characters
- Use type hints where appropriate

Example:
```python
async def create_task(
    provider_id: str, 
    title: str, 
    description: str, 
    reward: float
) -> dict:
    """
    Create a new task for workers.
    
    Args:
        provider_id: UUID of the provider
        title: Task title
        description: Task description
        reward: Reward amount in rupees
        
    Returns:
        Created task object or None if failed
    """
    # Implementation
    pass
```

### Database Operations

- Always use try-except blocks
- Log errors appropriately
- Return None on failure
- Use parameterized queries

### Handler Structure

```python
async def handler_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler description."""
    query = update.callback_query
    await query.answer()
    
    # Your logic here
    
    await query.edit_message_text(
        "Response message",
        parse_mode='Markdown'
    )
```

## Testing Guidelines

### Manual Testing

Test these scenarios for new features:

1. **Happy Path**: Normal usage flow
2. **Edge Cases**: Empty inputs, max values, special characters
3. **Error Handling**: Invalid inputs, network errors
4. **User Experience**: Clear messages, intuitive flow

### Testing Checklist

- [ ] Feature works as expected
- [ ] Error messages are clear
- [ ] No console errors
- [ ] Database operations successful
- [ ] UI is responsive
- [ ] Works for all user roles (if applicable)
- [ ] Doesn't break existing features

## Documentation

### Code Comments

```python
# Good: Explains why, not what
# Calculate total cost including platform fee
total = amount * 1.05

# Bad: States the obvious
# Set x to 5
x = 5
```

### README Updates

Update README.md if you:
- Add new features
- Change configuration
- Update dependencies
- Modify setup process

### API Documentation

Document new database functions:
```python
def get_user_by_id(user_id: str) -> dict:
    """
    Retrieve user by ID.
    
    Args:
        user_id: User's UUID
        
    Returns:
        User object or None if not found
        
    Example:
        >>> user = get_user_by_id("123-456-789")
        >>> print(user['name'])
        'John Doe'
    """
```

## Project Structure

```
handlers/
├── __init__.py       # Package initialization
├── start.py          # Start command and verification
├── provider.py       # Provider-specific features
├── taker.py          # Worker-specific features
├── wallet.py         # Wallet operations
├── admin.py          # Admin dashboard
└── support.py        # Support system

Root files:
├── bot.py            # Main application
├── config.py         # Configuration
├── database.py       # Database operations
├── utils.py          # Utility functions
└── requirements.txt  # Dependencies
```

## Need Help?

- Join our community chat: [Link]
- Read the documentation: README.md
- Check existing issues and PRs
- Ask questions in discussions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help newcomers
- Follow community guidelines

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for making WorkHub Bot better! 🚀
