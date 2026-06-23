package com.yunshop.service;

import com.yunshop.entity.Address;
import java.util.List;

public interface AddressService {

    List<Address> findByUserId(Long userId);

    Address findById(Long addressId);

    void save(Address address, Long userId);

    void update(Address address, Long userId);

    void delete(Long userId, Long addressId);

    void setDefault(Long userId, Long addressId);
}
