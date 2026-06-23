package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.entity.Ad;
import com.yunshop.mapper.AdMapper;
import com.yunshop.service.AdService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AdServiceImpl implements AdService {

    @Autowired
    private AdMapper adMapper;

    @Override
    public List<Ad> findEnabledBanners(int limit) {
        return adMapper.selectList(new LambdaQueryWrapper<Ad>()
                .eq(Ad::getType, "banner")
                .eq(Ad::getEnabled, 1)
                .orderByAsc(Ad::getSortOrder)
                .last("LIMIT " + limit));
    }
}
