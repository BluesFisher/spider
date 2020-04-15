#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

PROFESSION_UA_PATH = {
    'default': ROOT + '/common/',
    'static': ROOT + '/static/'
}

SQL_CREATE_TABLE = {
    't_college_info':
    "create table if not exists t_college_info(\
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        `url` VARCHAR(255) NOT NULL COMMENT '资讯链接',\
        `date` VARCHAR(30) NOT NULL COMMENT '资讯日期',\
        `title` VARCHAR(255) NOT NULL COMMENT '资讯标题',\
        `content` VARCHAR(10000) NOT NULL COMMENT '资讯内容',\
        `desc` VARCHAR(1000) NOT NULL COMMENT '资讯描述', \
        UNIQUE INDEX idx_title (title)\
    );",
    't_college_dynamic':
    "create table if not exists t_college_dynamic(\
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        `url` VARCHAR(255) NOT NULL COMMENT '资讯链接',\
        `date` VARCHAR(30) NOT NULL COMMENT '资讯日期',\
        `title` VARCHAR(255) NOT NULL COMMENT '资讯标题',\
        `content` VARCHAR(10000) NOT NULL COMMENT '资讯内容',\
        `desc` VARCHAR(1000) NOT NULL COMMENT '资讯描述', \
        UNIQUE INDEX idx_title (title)\
    );",
    't_student_guide':
    "create table if not exists t_student_guide(\
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        `college` VARCHAR(255) NOT NULL COMMENT '院校名称',\
        `url` VARCHAR(255) NOT NULL COMMENT '章程链接',\
        `content` VARCHAR(10000) NOT NULL COMMENT '章程内容',\
        UNIQUE INDEX idx_college (college)\
    );",
}
