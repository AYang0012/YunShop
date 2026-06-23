package com.yunshop.config;

import com.yunshop.entity.Admin;
import com.yunshop.mapper.AdminMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * 数据初始化：确保管理员密码正确
 */
@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private AdminMapper adminMapper;

    @Override
    public void run(String... args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        Admin admin = adminMapper.selectById(1L);
        if (admin != null) {
            // 重置管理员密码为 admin123
            admin.setPassword(encoder.encode("admin123"));
            adminMapper.updateById(admin);
            System.out.println("[初始化] 管理员密码已重置为: admin123");
        }
    }
}
