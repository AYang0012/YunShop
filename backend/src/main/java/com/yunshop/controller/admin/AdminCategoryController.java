package com.yunshop.controller.admin;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.entity.GoodsCategory;
import com.yunshop.mapper.GoodsCategoryMapper;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 后台分类管理控制器
 */
@RestController
@RequestMapping("/api/admin/category")
public class AdminCategoryController {

    @Autowired
    private GoodsCategoryMapper categoryMapper;

    /** 验证管理员登录 */
    private void checkAdmin(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) throw new RuntimeException("请先登录后台");
    }

    /** 获取分类树形列表（全部，含隐藏） */
    @GetMapping("/list")
    public Result<?> list(HttpSession session) {
        try {
            checkAdmin(session);
            List<GoodsCategory> allCategories = categoryMapper.selectList(null);
            return Result.ok(allCategories);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 添加分类 */
    @PostMapping("/add")
    public Result<?> add(@RequestBody GoodsCategory category, HttpSession session) {
        try {
            checkAdmin(session);
            // 如果是一级分类，parentId 设为 0
            if (category.getParentId() == null) {
                category.setParentId(0L);
            }
            // 根据 parentId 自动计算 level
            if (category.getParentId() == 0) {
                category.setLevel(1);
            } else {
                GoodsCategory parent = categoryMapper.selectById(category.getParentId());
                if (parent == null) return Result.fail("父分类不存在");
                category.setLevel(parent.getLevel() + 1);
            }
            if (category.getSortOrder() == null) {
                category.setSortOrder(0);
            }
            if (category.getIsShow() == null) {
                category.setIsShow(1);
            }
            if (category.getIsHot() == null) {
                category.setIsHot(0);
            }
            categoryMapper.insert(category);
            return Result.ok("添加成功", category);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 更新分类 */
    @PutMapping("/update")
    public Result<?> update(@RequestBody GoodsCategory category, HttpSession session) {
        try {
            checkAdmin(session);
            GoodsCategory exist = categoryMapper.selectById(category.getId());
            if (exist == null) return Result.fail("分类不存在");
            categoryMapper.updateById(category);
            return Result.ok("更新成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 删除分类（软删除） */
    @DeleteMapping("/delete/{id}")
    public Result<?> delete(@PathVariable Long id, HttpSession session) {
        try {
            checkAdmin(session);
            GoodsCategory exist = categoryMapper.selectById(id);
            if (exist == null) return Result.fail("分类不存在");
            categoryMapper.deleteById(id);
            return Result.ok("已删除");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 切换显示状态 */
    @PutMapping("/toggle/{id}")
    public Result<?> toggleShow(@PathVariable Long id, HttpSession session) {
        try {
            checkAdmin(session);
            GoodsCategory category = categoryMapper.selectById(id);
            if (category == null) return Result.fail("分类不存在");
            category.setIsShow(category.getIsShow() == 1 ? 0 : 1);
            categoryMapper.updateById(category);
            return Result.ok(category.getIsShow() == 1 ? "已显示" : "已隐藏");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
