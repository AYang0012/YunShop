"""
生成商品 SVG 图片 — 每个商品有不同的配色和图标
直接写入 static/upload/goods/ 目录
"""
import os

output_dir = "G:/TestProject/backend/src/main/resources/static/upload/goods"
os.makedirs(output_dir, exist_ok=True)

# 商品信息: goods_id -> (名称, 主色, 图标类型)
goods = [
    (1, "华为Mate 60 Pro", "#1A6B7A", "phone", "智能手机"),
    (2, "iPhone 15 Pro Max", "#2D2D2F", "phone", "旗舰手机"),
    (3, "小米14 Ultra", "#FF6900", "phone", "影像旗舰"),
    (4, "联想ThinkPad X1", "#E31D1A", "laptop", "商务笔记本"),
    (5, "Apple MacBook Pro", "#C0C0C0", "laptop", "专业笔记本"),
    (6, "格力空调 1.5匹", "#00A0E9", "appliance", "变频冷暖"),
    (7, "海尔双门冰箱", "#0096D6", "appliance", "风冷无霜"),
    (8, "小米平板6 Pro", "#FF6900", "tablet", "平板电脑"),
    (9, "华为MatePad Pro", "#1A6B7A", "tablet", "旗舰平板"),
    (10, "65W氮化镓充电器", "#333333", "accessory", "快充配件"),
]

# 图标 SVG 路径
icons = {
    "phone": '<rect x="140" y="60" width="120" height="260" rx="18" fill="none" stroke="white" stroke-width="6"/><rect x="155" y="80" width="90" height="200" rx="2" fill="white" opacity="0.5"/><circle cx="200" cy="315" r="8" fill="white" opacity="0.7"/>',
    "laptop": '<rect x="80" y="80" width="240" height="160" rx="12" fill="none" stroke="white" stroke-width="6"/><rect x="100" y="100" width="200" height="120" rx="4" fill="white" opacity="0.4"/><rect x="60" y="240" width="280" height="14" rx="7" fill="white" opacity="0.6"/><rect x="120" y="258" width="160" height="6" rx="3" fill="white" opacity="0.4"/>',
    "tablet": '<rect x="130" y="70" width="140" height="240" rx="16" fill="none" stroke="white" stroke-width="5"/><rect x="145" y="90" width="110" height="180" rx="4" fill="white" opacity="0.4"/><circle cx="200" cy="305" r="5" fill="white" opacity="0.6"/>',
    "appliance": '<rect x="110" y="40" width="180" height="300" rx="16" fill="none" stroke="white" stroke-width="6"/><rect x="130" y="70" width="140" height="140" rx="8" fill="white" opacity="0.35"/><rect x="130" y="230" width="140" height="80" rx="6" fill="white" opacity="0.25"/><circle cx="280" cy="60" r="8" fill="white" opacity="0.5"/>',
    "accessory": '<rect x="130" y="100" width="140" height="140" rx="24" fill="none" stroke="white" stroke-width="6"/><rect x="155" y="130" width="90" height="80" rx="8" fill="white" opacity="0.4"/><rect x="175" y="80" width="50" height="28" rx="6" fill="white" opacity="0.5"/><path d="M175 80 L175 60 Q200 50 225 60 L225 80" fill="none" stroke="white" stroke-width="5" opacity="0.6"/>',
}

svg_template = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color_light};stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.15"/>
    </filter>
  </defs>
  <!-- 背景 -->
  <rect width="400" height="400" rx="20" fill="url(#bg)"/>
  <!-- 装饰圆 -->
  <circle cx="350" cy="50" r="120" fill="white" opacity="0.08"/>
  <circle cx="50" cy="350" r="80" fill="white" opacity="0.06"/>
  <!-- 图标 -->
  <g filter="url(#shadow)" opacity="0.9">
    {icon}
  </g>
  <!-- 商品名 -->
  <text x="200" y="360" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" font-weight="600" fill="white" opacity="0.9">{name}</text>
  <!-- 标签 -->
  <text x="200" y="382" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="white" opacity="0.55">{tag}</text>
</svg>'''

# 生成浅色版本的函数
def lighten(hex_color, amount=0.3):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r + (255-r) * amount))
    g = min(255, int(g + (255-g) * amount))
    b = min(255, int(b + (255-b) * amount))
    return f"#{r:02x}{g:02x}{b:02x}"

print("生成商品 SVG 图片...")
for gid, name, color, icon_key, tag in goods:
    icon = icons.get(icon_key, icons["phone"])
    color_light = lighten(color, 0.35)
    svg = svg_template.format(color=color, color_light=color_light, icon=icon, name=name, tag=tag)

    filepath = os.path.join(output_dir, f"{gid}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  [{gid:2d}] {name} -> {gid}.svg")

print(f"\n完成! 共生成 {len(goods)} 张 SVG 图片")
print(f"目录: {output_dir}")
