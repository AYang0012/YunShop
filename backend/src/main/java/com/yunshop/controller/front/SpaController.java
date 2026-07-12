package com.yunshop.controller.front;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * SPA 路由转发 — 将非 API/upload 的请求转发到前端 index.html
 * 使 Vue Router history 模式在生产环境正常工作
 */
@Controller
public class SpaController {

    @GetMapping(value = {
        "/",
        "/login", "/register",
        "/goods/**",
        "/cart",
        "/order/**",
        "/user/**",
        "/admin", "/admin/**"
    })
    public String forward() {
        return "forward:/frontend/index.html";
    }
}
