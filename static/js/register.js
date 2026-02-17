/**
 * @file    register.js
 * @brief   注册页面交互逻辑
 * @details 实现表单验证、密码强度检测等功能
 * @author  AI Assistant
 * @date    2026-02-17
 * @version V1.0.0
 */

class RegisterManager {
    constructor() {
        this.form = document.getElementById('register-form');
        this.usernameInput = document.getElementById('username');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.confirmPasswordInput = document.getElementById('confirm-password');
        this.registerBtn = document.getElementById('register-btn');
        this.togglePasswordBtn = document.getElementById('toggle-password');
        this.toggleConfirmPasswordBtn = document.getElementById('toggle-confirm-password');
        this.eyeIcon = document.getElementById('eye-icon');
        this.eyeIconConfirm = document.getElementById('eye-icon-confirm');
        this.clearUsernameBtn = document.getElementById('clear-username');
        this.clearEmailBtn = document.getElementById('clear-email');
        this.agreeTermsCheckbox = document.getElementById('agree-terms');
        this.passwordStrength = document.getElementById('password-strength');
        this.strengthFill = document.getElementById('strength-fill');
        this.strengthText = document.getElementById('strength-text');
        this.formMessage = document.getElementById('form-message');
        
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        this.usernameInput.addEventListener('input', () => this.handleUsernameInput());
        this.usernameInput.addEventListener('blur', () => this.validateUsername());
        
        this.emailInput.addEventListener('input', () => this.handleEmailInput());
        this.emailInput.addEventListener('blur', () => this.validateEmail());
        
        this.passwordInput.addEventListener('input', () => this.handlePasswordInput());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        
        this.confirmPasswordInput.addEventListener('input', () => this.handleConfirmPasswordInput());
        this.confirmPasswordInput.addEventListener('blur', () => this.validateConfirmPassword());
        
        this.togglePasswordBtn.addEventListener('click', () => this.togglePasswordVisibility('password', this.eyeIcon));
        this.toggleConfirmPasswordBtn.addEventListener('click', () => this.togglePasswordVisibility('confirm-password', this.eyeIconConfirm));
        
        this.clearUsernameBtn.addEventListener('click', () => this.clearInput('username', this.clearUsernameBtn));
        this.clearEmailBtn.addEventListener('click', () => this.clearInput('email', this.clearEmailBtn));
    }
    
    handleUsernameInput() {
        const value = this.usernameInput.value;
        if (value.length > 0) {
            this.clearUsernameBtn.classList.remove('hidden');
        } else {
            this.clearUsernameBtn.classList.add('hidden');
        }
        this.clearFieldError('username');
    }
    
    handleEmailInput() {
        const value = this.emailInput.value;
        if (value.length > 0) {
            this.clearEmailBtn.classList.remove('hidden');
        } else {
            this.clearEmailBtn.classList.add('hidden');
        }
        this.clearFieldError('email');
    }
    
    handlePasswordInput() {
        const value = this.passwordInput.value;
        if (value.length > 0) {
            this.passwordStrength.classList.remove('hidden');
            this.updatePasswordStrength(value);
        } else {
            this.passwordStrength.classList.add('hidden');
        }
        this.clearFieldError('password');
        
        if (this.confirmPasswordInput.value) {
            this.validateConfirmPassword();
        }
    }
    
    handleConfirmPasswordInput() {
        this.clearFieldError('confirm-password');
    }
    
    validateUsername() {
        const value = this.usernameInput.value.trim();
        
        if (!value) {
            this.showFieldError('username', '请输入用户名');
            return false;
        }
        
        if (value.length < 3) {
            this.showFieldError('username', '用户名至少需要3个字符');
            return false;
        }
        
        if (value.length > 20) {
            this.showFieldError('username', '用户名不能超过20个字符');
            return false;
        }
        
        const usernameRegex = /^[a-zA-Z0-9_]+$/;
        if (!usernameRegex.test(value)) {
            this.showFieldError('username', '用户名只能包含字母、数字和下划线');
            return false;
        }
        
        this.showFieldSuccess('username');
        return true;
    }
    
    validateEmail() {
        const value = this.emailInput.value.trim();
        
        if (!value) {
            this.showFieldError('email', '请输入邮箱地址');
            return false;
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            this.showFieldError('email', '请输入有效的邮箱地址');
            return false;
        }
        
        this.showFieldSuccess('email');
        return true;
    }
    
    validatePassword() {
        const value = this.passwordInput.value;
        
        if (!value) {
            this.showFieldError('password', '请输入密码');
            return false;
        }
        
        if (value.length < 6) {
            this.showFieldError('password', '密码至少需要6个字符');
            return false;
        }
        
        this.showFieldSuccess('password');
        return true;
    }
    
    validateConfirmPassword() {
        const password = this.passwordInput.value;
        const confirmPassword = this.confirmPasswordInput.value;
        
        if (!confirmPassword) {
            this.showFieldError('confirm-password', '请再次输入密码');
            return false;
        }
        
        if (password !== confirmPassword) {
            this.showFieldError('confirm-password', '两次输入的密码不一致');
            return false;
        }
        
        this.showFieldSuccess('confirm-password');
        return true;
    }
    
    showFieldError(fieldName, message) {
        const input = document.getElementById(fieldName);
        const errorElement = document.getElementById(`${fieldName}-error`);
        
        input.classList.add('error');
        input.classList.remove('success');
        errorElement.textContent = `⚠️ ${message}`;
    }
    
    showFieldSuccess(fieldName) {
        const input = document.getElementById(fieldName);
        const errorElement = document.getElementById(`${fieldName}-error`);
        
        input.classList.remove('error');
        input.classList.add('success');
        errorElement.textContent = '';
    }
    
    clearFieldError(fieldName) {
        const input = document.getElementById(fieldName);
        const errorElement = document.getElementById(`${fieldName}-error`);
        
        input.classList.remove('error');
        errorElement.textContent = '';
    }
    
    togglePasswordVisibility(inputId, eyeIcon) {
        const input = document.getElementById(inputId);
        const type = input.type === 'password' ? 'text' : 'password';
        input.type = type;
        eyeIcon.textContent = type === 'password' ? '👁️' : '🙈';
    }
    
    clearInput(inputId, clearBtn) {
        const input = document.getElementById(inputId);
        input.value = '';
        clearBtn.classList.add('hidden');
        input.focus();
        this.clearFieldError(inputId);
    }
    
    updatePasswordStrength(password) {
        let strength = 0;
        let text = '';
        let className = '';
        
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        
        if (strength <= 2) {
            text = '弱';
            className = 'weak';
        } else if (strength <= 3) {
            text = '中等';
            className = 'medium';
        } else {
            text = '强';
            className = 'strong';
        }
        
        this.strengthFill.className = `strength-fill ${className}`;
        this.strengthText.textContent = `密码强度: ${text}`;
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const isUsernameValid = this.validateUsername();
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        const isConfirmPasswordValid = this.validateConfirmPassword();
        
        if (!isUsernameValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
            return;
        }
        
        if (!this.agreeTermsCheckbox.checked) {
            this.showFormMessage('error', '请阅读并同意服务条款');
            return;
        }
        
        this.setLoadingState(true);
        
        const formData = {
            username: this.usernameInput.value.trim(),
            email: this.emailInput.value.trim(),
            password: this.passwordInput.value
        };
        
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showFormMessage('success', '注册成功！正在跳转到登录页面...');
                
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                this.showFormMessage('error', data.message || '注册失败，请稍后重试');
            }
        } catch (error) {
            this.showFormMessage('error', '网络错误，请检查网络连接后重试');
        } finally {
            this.setLoadingState(false);
        }
    }
    
    setLoadingState(isLoading) {
        const btnText = this.registerBtn.querySelector('.btn-text');
        const btnLoader = this.registerBtn.querySelector('.btn-loader');
        
        if (isLoading) {
            btnText.classList.add('hidden');
            btnLoader.classList.remove('hidden');
            this.registerBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            this.registerBtn.disabled = false;
        }
    }
    
    showFormMessage(type, message) {
        this.formMessage.className = `form-message ${type}`;
        this.formMessage.classList.remove('hidden');
        
        const icon = type === 'success' ? '✅' : '❌';
        this.formMessage.innerHTML = `
            <span class="message-icon">${icon}</span>
            <span class="message-text">${message}</span>
        `;
        
        if (type === 'success') {
            setTimeout(() => {
                this.formMessage.classList.add('hidden');
            }, 3000);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new RegisterManager();
});
