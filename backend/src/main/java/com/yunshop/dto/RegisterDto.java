package com.yunshop.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

/**
 * 注册表单 DTO
 */
public class RegisterDto {

    @NotBlank(message = "手机号/邮箱不能为空")
    private String account;         // 手机号或邮箱

    private String registerType;    // mobile / email

    @NotBlank(message = "密码不能为空")
    private String password;

    @NotBlank(message = "确认密码不能为空")
    private String confirmPassword;

    private String referrerMobile;  // 推荐人手机（选填）

    private String avatar;          // 头像URL（选填）

    private boolean agreeProtocol;  // 是否同意协议

    public String getAccount() { return account; }
    public void setAccount(String account) { this.account = account; }
    public String getRegisterType() { return registerType; }
    public void setRegisterType(String registerType) { this.registerType = registerType; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getConfirmPassword() { return confirmPassword; }
    public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }
    public String getReferrerMobile() { return referrerMobile; }
    public void setReferrerMobile(String referrerMobile) { this.referrerMobile = referrerMobile; }
    public String getAvatar() { return avatar; }
    public void setAvatar(String avatar) { this.avatar = avatar; }
    public boolean isAgreeProtocol() { return agreeProtocol; }
    public void setAgreeProtocol(boolean agreeProtocol) { this.agreeProtocol = agreeProtocol; }
}
