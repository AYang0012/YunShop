package com.yunshop.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.mapper.AdminMapper;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 后台管理控制器
 */
@RestController
@RequestMapping("/api/admin")
public class AdminIndexController {

    @Autowired
    private AdminMapper adminMapper;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /** 后台登录 */
    @PostMapping("/login")
    public Result<?> login(@RequestBody Map<String, String> params, HttpSession session) {
        String username = params.get("username");
        String password = params.get("password");

        Admin admin = adminMapper.selectOne(new LambdaQueryWrapper<Admin>()
                .eq(Admin::getUsername, username));

        if (admin == null || admin.getStatus() == 0) {
            return Result.fail("用户名或密码错误");
        }
        if (!passwordEncoder.matches(password, admin.getPassword())) {
            return Result.fail("用户名或密码错误");
        }

        admin.setPassword(null);
        session.setAttribute(Constants.SESSION_ADMIN, admin);
        return Result.ok("登录成功", admin);
    }

    /** 退出登录 */
    @PostMapping("/logout")
    public Result<?> logout(HttpSession session) {
        session.removeAttribute(Constants.SESSION_ADMIN);
        return Result.ok("已退出");
    }

    /** 获取当前管理员 */
    @GetMapping("/current")
    public Result<?> currentAdmin(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) return Result.fail(401, "未登录");
        return Result.ok(admin);
    }
}
