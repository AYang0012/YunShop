package com.yunshop.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yunshop.common.Constants;
import com.yunshop.common.PageResult;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.entity.User;
import com.yunshop.mapper.UserMapper;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 后台会员管理控制器
 */
@RestController
@RequestMapping("/api/admin/user")
public class AdminUserController {

    @Autowired
    private UserMapper userMapper;

    /** 验证管理员登录 */
    private void checkAdmin(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) throw new RuntimeException("请先登录后台");
    }

    /** 会员列表（分页+筛选） */
    @GetMapping("/list")
    public Result<?> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int pageSize,
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) Integer status,
            HttpSession session) {
        try {
            checkAdmin(session);

            LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
            if (keyword != null && !keyword.isEmpty()) {
                wrapper.and(w -> w
                        .like(User::getNickname, keyword)
                        .or().like(User::getMobile, keyword)
                        .or().like(User::getEmail, keyword));
            }
            if (status != null) {
                wrapper.eq(User::getStatus, status);
            }
            wrapper.orderByDesc(User::getRegTime);

            Page<User> pageObj = new Page<>(page, pageSize);
            Page<User> result = userMapper.selectPage(pageObj, wrapper);

            // 清除密码字段
            List<User> users = result.getRecords().stream()
                    .peek(u -> u.setPassword(null))
                    .toList();

            return Result.ok(PageResult.of(result.getTotal(), page, pageSize, users));
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 会员详情 */
    @GetMapping("/detail/{userId}")
    public Result<?> detail(@PathVariable Long userId, HttpSession session) {
        try {
            checkAdmin(session);
            User user = userMapper.selectById(userId);
            if (user == null) return Result.fail("会员不存在");
            user.setPassword(null);
            return Result.ok(user);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 启用/禁用会员 */
    @PutMapping("/toggle/{userId}")
    public Result<?> toggleStatus(@PathVariable Long userId, HttpSession session) {
        try {
            checkAdmin(session);
            User user = userMapper.selectById(userId);
            if (user == null) return Result.fail("会员不存在");
            user.setStatus(user.getStatus() == 1 ? 0 : 1);
            userMapper.updateById(user);
            return Result.ok(user.getStatus() == 1 ? "已启用" : "已禁用");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
