package com.yunshop.service;

import com.yunshop.entity.Navigation;
import java.util.List;

public interface NavigationService {

    /** 获取前台显示的导航（前8条） */
    List<Navigation> findFrontNav(int limit);
}
