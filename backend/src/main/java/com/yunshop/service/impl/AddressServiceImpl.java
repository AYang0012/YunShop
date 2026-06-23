package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.common.Constants;
import com.yunshop.entity.Address;
import com.yunshop.mapper.AddressMapper;
import com.yunshop.service.AddressService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AddressServiceImpl implements AddressService {

    @Autowired
    private AddressMapper addressMapper;

    @Override
    public List<Address> findByUserId(Long userId) {
        return addressMapper.selectList(new LambdaQueryWrapper<Address>()
                .eq(Address::getUserId, userId)
                .orderByDesc(Address::getIsDefault)
                .orderByDesc(Address::getAddressId));
    }

    @Override
    public Address findById(Long addressId) {
        return addressMapper.selectById(addressId);
    }

    @Override
    public void save(Address address, Long userId) {
        long count = addressMapper.selectCount(new LambdaQueryWrapper<Address>()
                .eq(Address::getUserId, userId));
        if (count >= Constants.ADDRESS_MAX_COUNT) {
            throw new RuntimeException("收货地址已达上限(" + Constants.ADDRESS_MAX_COUNT + "个)");
        }
        address.setUserId(userId);
        // 如果这是第一个地址，自动设为默认
        if (count == 0) {
            address.setIsDefault(1);
        } else {
            address.setIsDefault(address.getIsDefault() != null ? address.getIsDefault() : 0);
        }
        // 如果设为默认，取消其他默认
        if (address.getIsDefault() == 1) {
            cancelOtherDefaults(userId, null);
        }
        addressMapper.insert(address);
    }

    @Override
    public void update(Address address, Long userId) {
        Address exist = addressMapper.selectById(address.getAddressId());
        if (exist == null || !exist.getUserId().equals(userId)) {
            throw new RuntimeException("地址不存在");
        }
        address.setUserId(userId);
        if (address.getIsDefault() == 1) {
            cancelOtherDefaults(userId, address.getAddressId());
        }
        addressMapper.updateById(address);
    }

    @Override
    public void delete(Long userId, Long addressId) {
        Address exist = addressMapper.selectById(addressId);
        if (exist == null || !exist.getUserId().equals(userId)) {
            throw new RuntimeException("地址不存在");
        }
        addressMapper.deleteById(addressId);
    }

    @Override
    public void setDefault(Long userId, Long addressId) {
        Address exist = addressMapper.selectById(addressId);
        if (exist == null || !exist.getUserId().equals(userId)) {
            throw new RuntimeException("地址不存在");
        }
        cancelOtherDefaults(userId, addressId);
        exist.setIsDefault(1);
        addressMapper.updateById(exist);
    }

    private void cancelOtherDefaults(Long userId, Long excludeId) {
        List<Address> list = addressMapper.selectList(new LambdaQueryWrapper<Address>()
                .eq(Address::getUserId, userId)
                .eq(Address::getIsDefault, 1));
        for (Address addr : list) {
            if (excludeId == null || !addr.getAddressId().equals(excludeId)) {
                addr.setIsDefault(0);
                addressMapper.updateById(addr);
            }
        }
    }
}
