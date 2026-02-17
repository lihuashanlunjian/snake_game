/**
 * @file    login.js
 * @brief   登录页面交互逻辑
 * @details 实现表单验证、密码强度检测、防暴力破解等功能
 * @author  AI Assistant
 * @date    2026-02-17
 * @version V1.0.0
 */

class LoginManager {
    constructor() {
        this.form = document.getElementById('login-form');
        this.usernameInput = document.getElementById('username');
        this.passwordInput = document.getElementById('password');
        this.loginBtn = document.getElementById('login-btn');
        this.togglePasswordBtn = document.getElementById('toggle-password');
        this.eyeIcon = document.getElementById('eye-icon');
        this.clearUsernameBtn = document.getElementById('clear-username');
        this.rememberMeCheckbox = document.getElementById('remember-me');
        this.forgotPasswordLink = document.getElementById('forgot-password-link');
        this.registerLink = document.getElementById('register-link');
        this.forgotModal = document.getElementById('forgot-modal');
        this.closeModalBtn = document.getElementById('close-modal');
        this.forgotForm = document.getElementById('forgot-form');
        this.rateLimitWarning = document.getElementById('rate-limit-warning');
        this.retryCountdown = document.getElementById('retry-countdown');
        this.passwordStrength = document.getElementById('password-strength');
        this.strengthFill = document.getElementById('strength-fill');
        this.strengthText = document.getElementById('strength-text');
        this.formMessage = document.getElementById('form-message');
        
        this.loginAttempts = this.getLoginAttempts();
        this.isRateLimited = false;
        this.rateLimitTimer = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadRememberedCredentials();
        this.checkRateLimit();
    }
    
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        this.usernameInput.addEventListener('input', () => this.handleUsernameInput());
        this.usernameInput.addEventListener('blur', () => this.validateUsername());
        
        this.passwordInput.addEventListener('input', () => this.handlePasswordInput());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        
        this.togglePasswordBtn.addEventListener('click', () => this.togglePasswordVisibility());
        
        this.clearUsernameBtn.addEventListener('click', () => this.clearUsername());
        
        this.forgotPasswordLink.addEventListener('click', (e) => this.showForgotModal(e));
        this.closeModalBtn.addEventListener('click', () => this.hideForgotModal());
        
        document.querySelector('.modal-overlay').addEventListener('click', () => this.hideForgotModal());
        
        this.forgotForm.addEventListener('submit', (e) => this.handleForgotPassword(e));
        
        this.registerLink.addEventListener('click', (e) => this.handleRegister(e));
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.forgotModal.classList.contains('hidden')) {
                this.hideForgotModal();
            }
        });
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
    
    handlePasswordInput() {
        const value = this.passwordInput.value;
        
        if (value.length > 0) {
            this.passwordStrength.classList.remove('hidden');
            this.updatePasswordStrength(value);
        } else {
            this.passwordStrength.classList.add('hidden');
        }
        
        this.clearFieldError('password');
    }
    
    validateUsername() {
        const value = this.usernameInput.value.trim();
        const errorElement = document.getElementById('username-error');
        
        if (!value) {
            this.showFieldError('username', '请输入用户名或邮箱');
            return false;
        }
        
        if (value.includes('@')) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                this.showFieldError('username', '请输入有效的邮箱地址');
                return false;
            }
        } else {
            if (value.length < 3) {
                this.showFieldError('username', '用户名至少需要3个字符');
                return false;
            }
            
            const usernameRegex = /^[a-zA-Z0-9_]+$/;
            if (!usernameRegex.test(value)) {
                this.showFieldError('username', '用户名只能包含字母、数字和下划线');
                return false;
            }
        }
        
        this.showFieldSuccess('username');
        return true;
    }
    
    validatePassword() {
        const value = this.passwordInput.value;
        const errorElement = document.getElementById('password-error');
        
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
    
    togglePasswordVisibility() {
        const type = this.passwordInput.type === 'password' ? 'text' : 'password';
        this.passwordInput.type = type;
        this.eyeIcon.textContent = type === 'password' ? '👁️' : '🙈';
    }
    
    clearUsername() {
        this.usernameInput.value = '';
        this.clearUsernameBtn.classList.add('hidden');
        this.usernameInput.focus();
        this.clearFieldError('username');
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
        
        if (this.isRateLimited) {
            this.showFormMessage('error', '登录尝试次数过多，请稍后再试');
            return;
        }
        
        const isUsernameValid = this.validateUsername();
        const isPasswordValid = this.validatePassword();
        
        if (!isUsernameValid || !isPasswordValid) {
            return;
        }
        
        this.setLoadingState(true);
        
        const formData = {
            username: this.usernameInput.value.trim(),
            password: this.passwordInput.value,
            remember: this.rememberMeCheckbox.checked
        };
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showFormMessage('success', '登录成功！正在跳转...');
                
                if (formData.remember) {
                    this.saveCredentials(formData.username);
                } else {
                    this.clearSavedCredentials();
                }
                
                this.resetLoginAttempts();
                
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            } else {
                this.handleLoginError(data);
            }
        } catch (error) {
            this.showFormMessage('error', '网络错误，请检查网络连接后重试');
        } finally {
            this.setLoadingState(false);
        }
    }
    
    handleLoginError(data) {
        this.incrementLoginAttempts();
        
        const remainingAttempts = this.getRemainingAttempts();
        
        if (remainingAttempts <= 0) {
            this.activateRateLimit();
            this.showFormMessage('error', '登录尝试次数过多，账户已被临时锁定');
        } else {
            this.showFormMessage('error', `${data.message || '登录失败'}，剩余尝试次数: ${remainingAttempts}`);
        }
    }
    
    setLoadingState(isLoading) {
        const btnText = this.loginBtn.querySelector('.btn-text');
        const btnLoader = this.loginBtn.querySelector('.btn-loader');
        
        if (isLoading) {
            btnText.classList.add('hidden');
            btnLoader.classList.remove('hidden');
            this.loginBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            this.loginBtn.disabled = false;
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
    
    getLoginAttempts() {
        const attempts = localStorage.getItem('loginAttempts');
        if (attempts) {
            const data = JSON.parse(attempts);
            if (Date.now() - data.timestamp > 15 * 60 * 1000) {
                localStorage.removeItem('loginAttempts');
                return { count: 0, timestamp: Date.now() };
            }
            return data;
        }
        return { count: 0, timestamp: Date.now() };
    }
    
    incrementLoginAttempts() {
        this.loginAttempts.count++;
        this.loginAttempts.timestamp = Date.now();
        localStorage.setItem('loginAttempts', JSON.stringify(this.loginAttempts));
    }
    
    resetLoginAttempts() {
        this.loginAttempts = { count: 0, timestamp: Date.now() };
        localStorage.removeItem('loginAttempts');
    }
    
    getRemainingAttempts() {
        const maxAttempts = 5;
        return Math.max(0, maxAttempts - this.loginAttempts.count);
    }
    
    checkRateLimit() {
        if (this.loginAttempts.count >= 5) {
            const timePassed = Date.now() - this.loginAttempts.timestamp;
            const lockoutDuration = 15 * 60 * 1000;
            
            if (timePassed < lockoutDuration) {
                this.activateRateLimit();
            } else {
                this.resetLoginAttempts();
            }
        }
    }
    
    activateRateLimit() {
        this.isRateLimited = true;
        this.rateLimitWarning.classList.remove('hidden');
        
        const lockoutDuration = 15 * 60 * 1000;
        const endTime = this.loginAttempts.timestamp + lockoutDuration;
        
        this.updateCountdown(endTime);
        
        this.rateLimitTimer = setInterval(() => {
            this.updateCountdown(endTime);
        }, 1000);
    }
    
    updateCountdown(endTime) {
        const remaining = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
        
        if (remaining <= 0) {
            this.deactivateRateLimit();
            return;
        }
        
        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;
        this.retryCountdown.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
    
    deactivateRateLimit() {
        this.isRateLimited = false;
        this.rateLimitWarning.classList.add('hidden');
        
        if (this.rateLimitTimer) {
            clearInterval(this.rateLimitTimer);
            this.rateLimitTimer = null;
        }
        
        this.resetLoginAttempts();
    }
    
    saveCredentials(username) {
        localStorage.setItem('rememberedUsername', username);
    }
    
    loadRememberedCredentials() {
        const savedUsername = localStorage.getItem('rememberedUsername');
        if (savedUsername) {
            this.usernameInput.value = savedUsername;
            this.clearUsernameBtn.classList.remove('hidden');
            this.rememberMeCheckbox.checked = true;
        }
    }
    
    clearSavedCredentials() {
        localStorage.removeItem('rememberedUsername');
    }
    
    showForgotModal(e) {
        e.preventDefault();
        this.forgotModal.classList.remove('hidden');
        document.getElementById('reset-email').focus();
    }
    
    hideForgotModal() {
        this.forgotModal.classList.add('hidden');
        this.forgotForm.reset();
        document.getElementById('reset-email-error').textContent = '';
    }
    
    async handleForgotPassword(e) {
        e.preventDefault();
        
        const emailInput = document.getElementById('reset-email');
        const email = emailInput.value.trim();
        const errorElement = document.getElementById('reset-email-error');
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            errorElement.textContent = '⚠️ 请输入邮箱地址';
            return;
        }
        
        if (!emailRegex.test(email)) {
            errorElement.textContent = '⚠️ 请输入有效的邮箱地址';
            return;
        }
        
        errorElement.textContent = '';
        
        try {
            const response = await fetch('/api/auth/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                alert('重置密码链接已发送到您的邮箱，请查收。');
                this.hideForgotModal();
            } else {
                errorElement.textContent = `⚠️ ${data.message || '发送失败，请稍后重试'}`;
            }
        } catch (error) {
            errorElement.textContent = '⚠️ 网络错误，请稍后重试';
        }
    }
    
    handleRegister(e) {
        e.preventDefault();
        window.location.href = '/register';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});
