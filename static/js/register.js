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
        
        this.wechatBtn = document.querySelector('.btn-wechat');
        this.qqBtn = document.querySelector('.btn-qq');
        
        this.isSubmitting = false;
        this.socialLoginCooldown = false;
        
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
        
        if (this.wechatBtn) {
            this.wechatBtn.addEventListener('click', () => this.handleWechatRegister());
        }
        
        if (this.qqBtn) {
            this.qqBtn.addEventListener('click', () => this.handleQQRegister());
        }
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
    
    setSocialButtonLoading(btn, isLoading, originalText) {
        const socialIcon = btn.querySelector('.social-icon');
        const textSpan = btn.querySelector('span:last-child');
        
        if (isLoading) {
            btn.disabled = true;
            btn.classList.add('btn-loading');
            textSpan.textContent = '正在跳转...';
            socialIcon.innerHTML = '<span class="spinner-small"></span>';
        } else {
            btn.disabled = false;
            btn.classList.remove('btn-loading');
            textSpan.textContent = originalText;
            socialIcon.textContent = btn.classList.contains('btn-wechat') ? '💬' : '🐧';
        }
    }
    
    checkCooldown() {
        if (this.socialLoginCooldown) {
            this.showFormMessage('error', '请稍后再试，操作过于频繁');
            return true;
        }
        return false;
    }
    
    startCooldown(duration = 3000) {
        this.socialLoginCooldown = true;
        setTimeout(() => {
            this.socialLoginCooldown = false;
        }, duration);
    }
    
    async handleWechatRegister() {
        if (this.checkCooldown()) {
            return;
        }
        
        const btn = this.wechatBtn;
        const originalText = '微信注册';
        
        try {
            this.setSocialButtonLoading(btn, true, originalText);
            this.startCooldown();
            
            const response = await fetch('/api/auth/wechat/authorize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'register',
                    timestamp: Date.now()
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                if (data.auth_url) {
                    this.showFormMessage('success', '正在跳转到微信授权页面...');
                    setTimeout(() => {
                        window.location.href = data.auth_url;
                    }, 1000);
                } else if (data.qrcode_url) {
                    this.showWechatQRCode(data.qrcode_url, data.expires_in);
                } else {
                    this.showFormMessage('success', '微信注册流程已启动，请按提示操作');
                }
            } else {
                if (data.error_code === 'WECHAT_NOT_CONFIGURED') {
                    this.showConfigGuideModal('微信登录配置指南', data.config_guide, 'wechat');
                } else {
                    throw new Error(data.message || '微信注册失败');
                }
            }
        } catch (error) {
            console.error('WeChat register error:', error);
            this.showFormMessage('error', error.message || '网络错误，请检查网络连接后重试');
        } finally {
            this.setSocialButtonLoading(btn, false, originalText);
        }
    }
    
    async handleQQRegister() {
        if (this.checkCooldown()) {
            return;
        }
        
        const btn = this.qqBtn;
        const originalText = 'QQ注册';
        
        try {
            this.setSocialButtonLoading(btn, true, originalText);
            this.startCooldown();
            
            const response = await fetch('/api/auth/qq/authorize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'register',
                    timestamp: Date.now()
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                if (data.auth_url) {
                    this.showFormMessage('success', '正在跳转到QQ授权页面...');
                    setTimeout(() => {
                        window.location.href = data.auth_url;
                    }, 1000);
                } else if (data.qrcode_url) {
                    this.showQQQRCode(data.qrcode_url, data.expires_in);
                } else {
                    this.showFormMessage('success', 'QQ注册流程已启动，请按提示操作');
                }
            } else {
                if (data.error_code === 'QQ_NOT_CONFIGURED') {
                    this.showConfigGuideModal('QQ登录配置指南', data.config_guide, 'qq');
                } else {
                    throw new Error(data.message || 'QQ注册失败');
                }
            }
        } catch (error) {
            console.error('QQ register error:', error);
            this.showFormMessage('error', error.message || '网络错误，请检查网络连接后重试');
        } finally {
            this.setSocialButtonLoading(btn, false, originalText);
        }
    }
    
    showConfigGuideModal(title, guide, type) {
        const existingModal = document.querySelector('.config-guide-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        const platformUrl = type === 'wechat' 
            ? 'https://open.weixin.qq.com/' 
            : 'https://connect.qq.com/';
        
        const modalHtml = `
            <div class="config-guide-modal" id="config-guide-modal">
                <div class="modal-overlay" id="config-guide-overlay"></div>
                <div class="modal-content config-guide-content">
                    <div class="modal-header">
                        <h3>⚠️ ${title}</h3>
                        <button class="modal-close" id="close-config-guide-modal">×</button>
                    </div>
                    <div class="modal-body">
                        <div class="config-guide-message">
                            <p>第三方登录功能尚未配置，请按以下步骤完成配置：</p>
                        </div>
                        <div class="config-steps">
                            <div class="config-step">
                                <span class="step-number">1</span>
                                <span class="step-text">${guide.step1}</span>
                            </div>
                            <div class="config-step">
                                <span class="step-number">2</span>
                                <span class="step-text">${guide.step2}</span>
                            </div>
                            <div class="config-step">
                                <span class="step-number">3</span>
                                <span class="step-text">${guide.step3}</span>
                            </div>
                            <div class="config-step">
                                <span class="step-number">4</span>
                                <span class="step-text">${guide.step4}</span>
                            </div>
                        </div>
                        <div class="config-guide-actions">
                            <a href="${platformUrl}" target="_blank" class="btn btn-primary config-link">
                                前往${type === 'wechat' ? '微信开放平台' : 'QQ互联平台'}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const modal = document.getElementById('config-guide-modal');
        const closeBtn = document.getElementById('close-config-guide-modal');
        const overlay = document.getElementById('config-guide-overlay');
        
        const closeModal = () => {
            modal.remove();
        };
        
        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);
    }
    
    showWechatQRCode(qrcodeUrl, expiresIn) {
        this.showQRCodeModal('微信扫码注册', qrcodeUrl, expiresIn, '请使用微信扫描二维码完成注册');
    }
    
    showQQQRCode(qrcodeUrl, expiresIn) {
        this.showQRCodeModal('QQ扫码注册', qrcodeUrl, expiresIn, '请使用QQ扫描二维码完成注册');
    }
    
    showQRCodeModal(title, qrcodeUrl, expiresIn, description) {
        const existingModal = document.querySelector('.qrcode-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        const modalHtml = `
            <div class="qrcode-modal" id="qrcode-modal">
                <div class="modal-overlay" id="qrcode-overlay"></div>
                <div class="modal-content qrcode-content">
                    <div class="modal-header">
                        <h3>${title}</h3>
                        <button class="modal-close" id="close-qrcode-modal">×</button>
                    </div>
                    <div class="modal-body">
                        <div class="qrcode-container">
                            <img src="${qrcodeUrl}" alt="注册二维码" class="qrcode-image">
                        </div>
                        <p class="qrcode-description">${description}</p>
                        <div class="qrcode-timer">
                            <span>二维码有效期：</span>
                            <span id="qrcode-countdown">${expiresIn || 300}</span>
                            <span>秒</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const modal = document.getElementById('qrcode-modal');
        const closeBtn = document.getElementById('close-qrcode-modal');
        const overlay = document.getElementById('qrcode-overlay');
        const countdownEl = document.getElementById('qrcode-countdown');
        
        let countdown = expiresIn || 300;
        const timer = setInterval(() => {
            countdown--;
            if (countdownEl) {
                countdownEl.textContent = countdown;
            }
            if (countdown <= 0) {
                clearInterval(timer);
                modal.remove();
                this.showFormMessage('error', '二维码已过期，请重新获取');
            }
        }, 1000);
        
        const closeModal = () => {
            clearInterval(timer);
            modal.remove();
        };
        
        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);
        
        this.pollSocialLoginStatus();
    }
    
    async pollSocialLoginStatus() {
        let attempts = 0;
        const maxAttempts = 60;
        
        const poll = async () => {
            if (attempts >= maxAttempts) {
                return;
            }
            
            attempts++;
            
            try {
                const response = await fetch('/api/auth/social/status', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success && data.registered) {
                    const modal = document.querySelector('.qrcode-modal');
                    if (modal) {
                        modal.remove();
                    }
                    this.showFormMessage('success', '注册成功！正在跳转到登录页面...');
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                    return;
                }
            } catch (error) {
                console.error('Poll status error:', error);
            }
            
            setTimeout(poll, 3000);
        };
        
        poll();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new RegisterManager();
});
