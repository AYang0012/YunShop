package com.yunshop.service;

import com.yunshop.entity.Ad;
import java.util.List;

public interface AdService {

    /** 获取启用的 Banner 广告 */
    List<Ad> findEnabledBanners(int limit);
}
