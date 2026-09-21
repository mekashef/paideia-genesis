# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Paideia Genesis, please report it responsibly.

**Do NOT open a public GitHub Issue for security vulnerabilities.**

Instead, please report security issues by emailing the repository owner or by using [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) feature on this repository.

### What to Include

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgement**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix or mitigation**: As soon as reasonably possible

## Security Best Practices for Users

1. **Never commit API keys**: Use environment variables or a `.env` file (which is gitignored)
2. **Use the mock provider for testing**: Set `LLM_PROVIDER=mock` to avoid external API calls
3. **Bind to localhost in development**: Set `HOST=127.0.0.1` instead of `0.0.0.0` when not deploying
4. **Keep dependencies updated**: Regularly run `pip install --upgrade -r requirements.txt`

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.3.x   | ✅ Current |
| < 0.3   | ❌ No longer supported |
