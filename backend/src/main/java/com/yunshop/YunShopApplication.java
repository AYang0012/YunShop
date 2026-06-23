package com.yunshop;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.yunshop.mapper")
public class YunShopApplication {

    public static void main(String[] args) {
        SpringApplication.run(YunShopApplication.class, args);
        System.out.println("========================================");
        System.out.println("  云集优选 B2C 电商平台 启动成功！");
        System.out.println("  前台地址: http://localhost:8080/");
        System.out.println("  后台地址: http://localhost:8080/admin/login");
        System.out.println("========================================");
    }
}
