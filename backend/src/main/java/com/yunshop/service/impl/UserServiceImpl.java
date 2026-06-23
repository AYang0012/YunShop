package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.common.Constants;
import com.yunshop.dto.LoginDto;
import com.yunshop.dto.RegisterDto;
import com.yunshop.entity.User;
import com.yunshop.mapper.UserMapper;
import com.yunshop.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private HttpSession session;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User login(LoginDto loginDto) {
        // 按手机号或邮箱查询用户
        String username = loginDto.getUsername();
        User user = userMapper.selectOne(new LambdaQueryWrapper<User>()
                .eq(User::getMobile, username)
                .or()
                .eq(User::getEmail, username));

        if (user == null) {
            throw new RuntimeException("用户名或密码错误");
        }
        if (user.getStatus() == 0) {
            throw new RuntimeException("账号已被禁用");
        }
        if (!passwordEncoder.matches(loginDto.getPassword(), user.getPassword())) {
            throw new RuntimeException("用户名或密码错误");
        }

        // 更新最后登录时间
        user.setLastLogin(LocalDateTime.now());
        userMapper.updateById(user);

        // 存入 Session
        user.setPassword(null); // 不暴露密码
        session.setAttribute(Constants.SESSION_USER, user);
        return user;
    }

    @Override
    public User register(RegisterDto registerDto) {
        // 校验协议
        if (!registerDto.isAgreeProtocol()) {
            throw new RuntimeException("请先阅读并同意用户协议");
        }
        // 校验密码一致性
        if (!registerDto.getPassword().equals(registerDto.getConfirmPassword())) {
            throw new RuntimeException("两次输入的密码不一致");
        }

        String account = registerDto.getAccount();
        User user = new User();
        user.setPassword(passwordEncoder.encode(registerDto.getPassword()));
        user.setNickname(account); // 默认昵称
        user.setLevel(0);
        user.setPoints(0);
        user.setStatus(1);
        user.setRegTime(LocalDateTime.now());
        user.setLastLogin(LocalDateTime.now());

        // 判断注册方式
        if ("email".equals(registerDto.getRegisterType())) {
            // 邮箱注册
            if (userMapper.selectCount(new LambdaQueryWrapper<User>().eq(User::getEmail, account)) > 0) {
                throw new RuntimeException("该邮箱已被注册");
            }
            user.setEmail(account);
        } else {
            // 手机号注册（默认）
            if (userMapper.selectCount(new LambdaQueryWrapper<User>().eq(User::getMobile, account)) > 0) {
                throw new RuntimeException("该手机号已被注册");
            }
            user.setMobile(account);
        }

        userMapper.insert(user);

        // 注册成功自动登录
        user.setPassword(null);
        session.setAttribute(Constants.SESSION_USER, user);
        return user;
    }

    @Override
    public User findById(Long userId) {
        User user = userMapper.selectById(userId);
        if (user != null) {
            user.setPassword(null);
        }
        return user;
    }

    @Override
    public void update(User user) {
        // 不允许修改手机号、邮箱（需要单独验证）
        User exist = userMapper.selectById(user.getUserId());
        if (exist == null) {
            throw new RuntimeException("用户不存在");
        }
        user.setMobile(null);
        user.setEmail(null);
        user.setPassword(null);
        user.setLevel(null);
        user.setPoints(null);
        userMapper.updateById(user);

        // 更新 Session 中的用户信息
        User updated = findById(user.getUserId());
        session.setAttribute(Constants.SESSION_USER, updated);
    }

    @Override
    public boolean changePassword(Long userId, String oldPassword, String newPassword) {
        User user = userMapper.selectById(userId);
        if (user == null) {
            throw new RuntimeException("用户不存在");
        }
        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw new RuntimeException("原密码错误");
        }
        user.setPassword(passwordEncoder.encode(newPassword));
        userMapper.updateById(user);
        return true;
    }
}
