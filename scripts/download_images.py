"""
从 Unsplash / Picsum 下载商品占位图片
为云集优选10个商品生成对应的图片文件
"""
import urllib.request
import os
import sys

# 目标目录
output_dir = "G:/TestProject/backend/src/main/resources/static/upload/goods"
os.makedirs(output_dir, exist_ok=True)

# 商品ID -> Unsplash 搜索词（高质量免费图片）
# Unsplash Source API: https://source.unsplash.com/400x400/?keyword
products = {
    1: "smartphone-huawei",
    2: "iphone-apple",
    3: "xiaomi-phone",
    4: "thinkpad-laptop",
    5: "macbook-pro",
    6: "air-conditioner",
    7: "refrigerator-kitchen",
    8: "tablet-xiaomi",
    9: "tablet-huawei",
    10: "charger-gadget",
}

# 通用备选搜索词
fallback = {
    1: "phone",
    2: "iphone",
    3: "smartphone",
    4: "laptop",
    5: "macbook",
    6: "ac-unit",
    7: "fridge",
    8: "ipad",
    9: "tablet",
    10: "electronics",
}

print("开始下载商品图片...")
for goods_id, keyword in products.items():
    filename = f"{goods_id}.jpg"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print(f"  [{goods_id}] 已存在，跳过")
        continue

    # 尝试主关键词
    url = f"https://source.unsplash.com/400x400/?{keyword}"
    try:
        print(f"  [{goods_id}] 下载: {keyword} ...", end=" ")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 2000:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"OK ({len(data)} bytes)")
                continue
    except Exception as e:
        print(f"失败: {e}")

    # 使用备选关键词
    fb = fallback.get(goods_id, "product")
    url2 = f"https://source.unsplash.com/400x400/?{fb}"
    try:
        print(f"  [{goods_id}] 备选下载: {fb} ...", end=" ")
        req = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 2000:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"OK ({len(data)} bytes)")
    except Exception as e:
        print(f"备选也失败: {e}")

print("下载完成!")

# 验证
print("\n文件列表:")
for goods_id in products:
    filepath = os.path.join(output_dir, f"{goods_id}.jpg")
    if os.path.exists(filepath):
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  goods/{goods_id}.jpg - {size_kb:.1f} KB")
    else:
        print(f"  goods/{goods_id}.jpg - 缺失!")
