#!/bin/bash
declare -A urls=(
[22]="https://images.unsplash.com/photo-1604503468506-8da9d0b4b7e6?w=500"
[33]="https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=500"
[36]="https://images.unsplash.com/photo-1529653762956-b5ede71b1b6e?w=500"
[39]="https://images.unsplash.com/photo-1598965402089-897ce52e2b12?w=500"
[40]="https://images.unsplash.com/photo-1545566241-0b2909e2c681?w=500"
[55]="https://images.unsplash.com/photo-1661961112951-f5bfd1f6530f?w=500"
[61]="https://images.unsplash.com/photo-1534707403098-056b1a8da58b?w=500"
[63]="https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=500"
[72]="https://images.unsplash.com/photo-1562155955-1cb2d73488d7?w=500"
[86]="https://images.unsplash.com/photo-1598033129183-c4f50c736c10?w=500"
[92]="https://images.unsplash.com/photo-1583496661160-fb5886a0afe0?w=500"
[118]="https://images.unsplash.com/photo-1602473811325-930e7170e071?w=500"
)
for id in "${!urls[@]}"; do
  curl -s -L -o "$id.jpg" "${urls[$id]}" --proxy http://127.0.0.1:7897 &
done
wait
echo "修复完成"
