package com.yunshop.controller.front;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpSession;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

/**
 * 文件上传控制器
 */
@RestController
@RequestMapping("/api/upload")
public class UploadController {

    @Value("${upload.path:./src/main/resources/static/upload/}")
    private String uploadPath;

    private static final Set<String> ALLOWED_EXTENSIONS = Set.of(".png", ".jpg", ".jpeg");
    private static final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

    /** 上传头像 */
    @PostMapping("/avatar")
    public Result<Map<String, Object>> uploadAvatar(
            @RequestParam("file") MultipartFile file,
            HttpSession session) {

        // 登录检查
        User sessionUser = (User) session.getAttribute(Constants.SESSION_USER);
        if (sessionUser == null) {
            return Result.fail(401, "请先登录");
        }

        // 空文件检查
        if (file == null || file.isEmpty()) {
            return Result.fail(500, "请选择文件");
        }

        // 扩展名校验
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null || originalFilename.isEmpty()) {
            return Result.fail(500, "文件名不能为空");
        }
        String ext = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex >= 0) {
            ext = originalFilename.substring(dotIndex).toLowerCase();
        }
        if (!ALLOWED_EXTENSIONS.contains(ext)) {
            return Result.fail(500, "仅支持 .png、.jpg、.jpeg 格式");
        }

        // 文件大小校验
        if (file.getSize() > MAX_FILE_SIZE) {
            return Result.fail(500, "文件大小不能超过 5MB");
        }

        try {
            // 确保上传目录存在
            File dir = new File(uploadPath, "avatars");
            if (!dir.exists()) {
                dir.mkdirs();
            }

            // 生成唯一文件名
            Long userId = sessionUser.getUserId();
            String uuid = UUID.randomUUID().toString().replace("-", "");
            String savedName = "avatar_" + userId + "_" + uuid + ext;

            // 保存文件
            Path targetPath = Paths.get(dir.getAbsolutePath(), savedName);
            file.transferTo(targetPath.toFile());

            // 返回访问 URL
            String url = "/upload/avatars/" + savedName;
            Map<String, Object> data = new LinkedHashMap<>();
            data.put("url", url);
            data.put("filename", savedName);
            return Result.ok(data);

        } catch (IOException e) {
            return Result.fail(500, "文件上传失败: " + e.getMessage());
        }
    }
}
