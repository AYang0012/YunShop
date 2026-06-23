package com.yunshop.controller.front;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import javax.imageio.ImageIO;

/**
 * 商品图片生成控制器（生成 SVG/PNG 占位图）
 */
@RestController
@RequestMapping("/api/images")
public class ImageController {

    /** 商品占位图（根据 goodsId 生成不同颜色） */
    @GetMapping(value = "/goods/{goodsId}", produces = MediaType.IMAGE_PNG_VALUE)
    public byte[] goodsImage(@PathVariable Long goodsId) throws Exception {
        int w = 400, h = 400;
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // 基于 goodsId 选配色
        Color[] colors = {
            new Color(59, 130, 246),  // 蓝
            new Color(16, 185, 129),  // 绿
            new Color(245, 158, 11),  // 橙
            new Color(239, 68, 68),   // 红
            new Color(139, 92, 246),  // 紫
            new Color(236, 72, 153),  // 粉
            new Color(20, 184, 166),  // 青
            new Color(99, 102, 241),  // 靛
        };
        Color c1 = colors[(int)(goodsId % colors.length)];
        Color c2 = new Color(
                Math.min(255, c1.getRed() + 40),
                Math.min(255, c1.getGreen() + 30),
                Math.min(255, c1.getBlue() + 50));

        // 渐变背景
        GradientPaint gp = new GradientPaint(0, 0, c1, w, h, c2);
        g.setPaint(gp);
        g.fillRoundRect(0, 0, w, h, 20, 20);

        // 购物袋图标（圆形）
        g.setColor(new Color(255, 255, 255, 180));
        g.fillOval(w/2 - 60, h/2 - 80, 120, 120);

        // 购物袋图标线条
        g.setColor(Color.WHITE);
        g.setStroke(new BasicStroke(6, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        // 袋身
        g.drawRoundRect(w/2 - 35, h/2 - 45, 70, 70, 12, 12);
        // 手提
        g.drawArc(w/2 - 20, h/2 - 65, 40, 35, 0, -180);

        // 商品编号文字
        g.setFont(new Font("Arial", Font.BOLD, 18));
        g.setColor(new Color(255, 255, 255, 160));
        String text = "GOODS #" + goodsId;
        FontMetrics fm = g.getFontMetrics();
        int tw = fm.stringWidth(text);
        g.drawString(text, (w - tw)/2, h - 40);

        g.dispose();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(img, "png", baos);
        return baos.toByteArray();
    }

    /** Banner 占位图 */
    @GetMapping(value = "/banner/{adId}", produces = MediaType.IMAGE_PNG_VALUE)
    public byte[] bannerImage(@PathVariable Long adId) throws Exception {
        int w = 800, h = 400;
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        Color[] colors = {
            new Color(26, 107, 122), new Color(232, 115, 74),
            new Color(59, 130, 246), new Color(139, 92, 246)
        };
        Color c1 = colors[(int)(adId % colors.length)];

        GradientPaint gp = new GradientPaint(0, 0, c1, w, h, c1.brighter().brighter());
        g.setPaint(gp);
        g.fillRect(0, 0, w, h);

        // 装饰圆形
        g.setColor(new Color(255, 255, 255, 40));
        g.fillOval(w - 200, -100, 400, 400);
        g.fillOval(-100, h - 200, 300, 300);

        // 标题占位
        g.setColor(Color.WHITE);
        g.setFont(new Font("Microsoft YaHei", Font.BOLD, 48));
        String text = "BANNER " + adId;
        FontMetrics fm = g.getFontMetrics();
        int tw = fm.stringWidth(text);
        g.drawString(text, (w - tw)/2, h/2 + 16);

        g.dispose();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(img, "png", baos);
        return baos.toByteArray();
    }
}
