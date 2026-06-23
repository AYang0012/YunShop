package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.entity.Navigation;
import com.yunshop.mapper.NavigationMapper;
import com.yunshop.service.NavigationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NavigationServiceImpl implements NavigationService {

    @Autowired
    private NavigationMapper navigationMapper;

    @Override
    public List<Navigation> findFrontNav(int limit) {
        return navigationMapper.selectList(new LambdaQueryWrapper<Navigation>()
                .eq(Navigation::getIsShow, 1)
                .eq(Navigation::getPosition, "top")
                .orderByAsc(Navigation::getSortOrder)
                .last("LIMIT " + limit));
    }
}
