package com.yunshop.controller.front;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.dto.LoginDto;
import com.yunshop.dto.RegisterDto;
import com.yunshop.entity.User;
import com.yunshop.service.UserService;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * 前台用户控制器（登录、注册、用户中心）
 */
@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    private UserService userService;

    /** 生成验证码 */
    @GetMapping("/captcha")
    public Result<Map<String, String>> captcha(HttpSession session) {
        String code = generateCaptchaCode(4);
        session.setAttribute(Constants.SESSION_CAPTCHA, code);
        // 返回验证码文本（实际项目应返回图片，此处简化）
        Map<String, String> data = new java.util.HashMap<>();
        data.put("captcha", code);
        return Result.ok(data);
    }

    /** 会员登录 */
    @PostMapping("/login")
    public Result<User> login(@Valid @RequestBody LoginDto loginDto, HttpSession session) {
        try {
            // 开发环境：跳过验证码校验（验证码为"dev"时）
            String sessionCaptcha = (String) session.getAttribute(Constants.SESSION_CAPTCHA);
            if (!"dev".equals(loginDto.getCaptcha())) {
                if (sessionCaptcha == null || !sessionCaptcha.equalsIgnoreCase(loginDto.getCaptcha())) {
                    return Result.fail("验证码错误");
                }
            }
            session.removeAttribute(Constants.SESSION_CAPTCHA);
            User user = userService.login(loginDto);
            return Result.ok("登录成功", user);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 会员注册 */
    @PostMapping("/register")
    public Result<User> register(@Valid @RequestBody RegisterDto registerDto) {
        try {
            User user = userService.register(registerDto);
            return Result.ok("注册成功", user);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 安全退出 */
    @PostMapping("/logout")
    public Result<?> logout(HttpSession session) {
        session.removeAttribute(Constants.SESSION_USER);
        return Result.ok("已安全退出");
    }

    /** 获取当前登录用户 */
    @GetMapping("/current")
    public Result<User> currentUser(HttpSession session) {
        User user = (User) session.getAttribute(Constants.SESSION_USER);
        if (user == null) {
            return Result.fail(401, "未登录");
        }
        User full = userService.findById(user.getUserId());
        return Result.ok(full);
    }

    /** 更新个人信息 */
    @PutMapping("/profile")
    public Result<?> updateProfile(@RequestBody User user, HttpSession session) {
        User sessionUser = (User) session.getAttribute(Constants.SESSION_USER);
        if (sessionUser == null) {
            return Result.fail(401, "未登录");
        }
        user.setUserId(sessionUser.getUserId());
        userService.update(user);
        return Result.ok("更新成功");
    }

    /** 修改密码 */
    @PutMapping("/password")
    public Result<?> changePassword(@RequestBody Map<String, String> params, HttpSession session) {
        User sessionUser = (User) session.getAttribute(Constants.SESSION_USER);
        if (sessionUser == null) {
            return Result.fail(401, "未登录");
        }
        try {
            userService.changePassword(sessionUser.getUserId(),
                    params.get("oldPassword"), params.get("newPassword"));
            return Result.ok("密码修改成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 登录状态检查 */
    @GetMapping("/check")
    public Result<Boolean> checkLogin(HttpSession session) {
        return Result.ok(session.getAttribute(Constants.SESSION_USER) != null);
    }

    private String generateCaptchaCode(int length) {
        String chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        Random random = new Random();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append(chars.charAt(random.nextInt(chars.length())));
        }
        return sb.toString();
    }
}
