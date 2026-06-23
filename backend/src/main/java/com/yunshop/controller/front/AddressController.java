package com.yunshop.controller.front;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.Address;
import com.yunshop.entity.User;
import com.yunshop.service.AddressService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 前台收货地址控制器
 */
@RestController
@RequestMapping("/api/address")
public class AddressController {

    @Autowired
    private AddressService addressService;

    private Long getUserId(HttpSession session) {
        User user = (User) session.getAttribute(Constants.SESSION_USER);
        if (user == null) throw new RuntimeException("请先登录");
        return user.getUserId();
    }

    /** 地址列表 */
    @GetMapping("/list")
    public Result<List<Address>> list(HttpSession session) {
        try {
            return Result.ok(addressService.findByUserId(getUserId(session)));
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 获取单个地址 */
    @GetMapping("/{addressId}")
    public Result<Address> getOne(@PathVariable Long addressId, HttpSession session) {
        try {
            Address addr = addressService.findById(addressId);
            if (addr == null || !addr.getUserId().equals(getUserId(session))) {
                return Result.fail("地址不存在");
            }
            return Result.ok(addr);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 新增地址 */
    @PostMapping("/add")
    public Result<?> add(@RequestBody Address address, HttpSession session) {
        try {
            addressService.save(address, getUserId(session));
            return Result.ok("添加成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 编辑地址 */
    @PutMapping("/update")
    public Result<?> update(@RequestBody Address address, HttpSession session) {
        try {
            addressService.update(address, getUserId(session));
            return Result.ok("更新成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 删除地址 */
    @DeleteMapping("/delete/{addressId}")
    public Result<?> delete(@PathVariable Long addressId, HttpSession session) {
        try {
            addressService.delete(getUserId(session), addressId);
            return Result.ok("删除成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 设为默认 */
    @PutMapping("/default/{addressId}")
    public Result<?> setDefault(@PathVariable Long addressId, HttpSession session) {
        try {
            addressService.setDefault(getUserId(session), addressId);
            return Result.ok("已设为默认地址");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
