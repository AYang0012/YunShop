package com.yunshop.service;

import com.yunshop.dto.LoginDto;
import com.yunshop.dto.RegisterDto;
import com.yunshop.entity.User;

/**
 * 用户服务接口
 */
public interface UserService {

    /** 会员登录，返回登录成功的用户 */
    User login(LoginDto loginDto);

    /** 会员注册 */
    User register(RegisterDto registerDto);

    /** 根据ID查询用户 */
    User findById(Long userId);

    /** 更新用户信息 */
    void update(User user);

    /** 修改密码 */
    boolean changePassword(Long userId, String oldPassword, String newPassword);
}
