/*
Navicat MySQL Data Transfer

Source Server         : cheertt
Source Server Version : 50725
Source Host           : localhost:3306
Source Database       : reprojectred

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-03-01 22:34:18
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add content type', '4', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('11', 'Can change content type', '4', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete content type', '4', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('13', 'Can add session', '5', 'add_session');
INSERT INTO `auth_permission` VALUES ('14', 'Can change session', '5', 'change_session');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete session', '5', 'delete_session');
INSERT INTO `auth_permission` VALUES ('16', 'Can add 商家信息', '6', 'add_userprofile');
INSERT INTO `auth_permission` VALUES ('17', 'Can change 商家信息', '6', 'change_userprofile');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete 商家信息', '6', 'delete_userprofile');
INSERT INTO `auth_permission` VALUES ('19', 'Can add 销售信息', '7', 'add_workorder');
INSERT INTO `auth_permission` VALUES ('20', 'Can change 销售信息', '7', 'change_workorder');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete 销售信息', '7', 'delete_workorder');

-- ----------------------------
-- Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_userprofile_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('7', 'personal', 'workorder');
INSERT INTO `django_content_type` VALUES ('5', 'sessions', 'session');
INSERT INTO `django_content_type` VALUES ('6', 'users', 'userprofile');

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2019-03-01 14:39:47.445460');
INSERT INTO `django_migrations` VALUES ('2', 'contenttypes', '0002_remove_content_type_name', '2019-03-01 14:39:47.601842');
INSERT INTO `django_migrations` VALUES ('3', 'auth', '0001_initial', '2019-03-01 14:39:47.981098');
INSERT INTO `django_migrations` VALUES ('4', 'auth', '0002_alter_permission_name_max_length', '2019-03-01 14:39:48.055223');
INSERT INTO `django_migrations` VALUES ('5', 'auth', '0003_alter_user_email_max_length', '2019-03-01 14:39:48.061236');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0004_alter_user_username_opts', '2019-03-01 14:39:48.067226');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0005_alter_user_last_login_null', '2019-03-01 14:39:48.075190');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0006_require_contenttypes_0002', '2019-03-01 14:39:48.081209');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0007_alter_validators_add_error_messages', '2019-03-01 14:39:48.087203');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0008_alter_user_username_max_length', '2019-03-01 14:39:48.093123');
INSERT INTO `django_migrations` VALUES ('11', 'users', '0001_initial', '2019-03-01 14:39:48.503403');
INSERT INTO `django_migrations` VALUES ('12', 'admin', '0001_initial', '2019-03-01 14:39:48.690081');
INSERT INTO `django_migrations` VALUES ('13', 'admin', '0002_logentry_remove_auto_add', '2019-03-01 14:39:48.698059');
INSERT INTO `django_migrations` VALUES ('14', 'sessions', '0001_initial', '2019-03-01 14:39:48.759633');
INSERT INTO `django_migrations` VALUES ('15', 'personal', '0001_initial', '2019-03-01 15:11:56.752217');
INSERT INTO `django_migrations` VALUES ('16', 'users', '0002_auto_20190301_1710', '2019-03-01 17:10:21.056611');
INSERT INTO `django_migrations` VALUES ('17', 'users', '0003_userprofile_url', '2019-03-01 20:43:20.630683');

-- ----------------------------
-- Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('05ycmjf472in6ax13fd70ygbb4r2rabg', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 17:41:28.992786');
INSERT INTO `django_session` VALUES ('1593w4px2zgvv70c6m0kt0f7w8dsyezh', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 16:41:59.941513');
INSERT INTO `django_session` VALUES ('2x1nqesj8gfreephb4o2kb9hylte9tik', 'YWU1NTI2YjJlMmM5ZDZkODM1YmVlNTYwN2MwMDNmNGQ0Mjk5ZDFmMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZTVjYmYwOTNhNTAyODlkNzRmYTM5Y2NjMmI0YWRhN2VlOGMzZmNmIn0=', '2019-03-01 21:32:20.514303');
INSERT INTO `django_session` VALUES ('5gy4gu78l1qbo9qmh0eoslw4l6yydxgm', 'YWU1NTI2YjJlMmM5ZDZkODM1YmVlNTYwN2MwMDNmNGQ0Mjk5ZDFmMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZTVjYmYwOTNhNTAyODlkNzRmYTM5Y2NjMmI0YWRhN2VlOGMzZmNmIn0=', '2019-03-01 20:43:02.511730');
INSERT INTO `django_session` VALUES ('6x3ogd25snaj03a1ookry5wjizqt4hb7', 'MTJkM2MyMmE2MDFiMGJmOGU2YzQyNWM5NGE3MjQyYzczODAzN2ExMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 15:23:54.447452');
INSERT INTO `django_session` VALUES ('gq2az1mvdkc3bvgu4bs1056mgxmjmawu', 'NTI2NGI5MjkxOTRhYmFkMDFjMDk0ZWYzMWVhMDUxYzhjMTAzZGQ1Mjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkYmJmNjcyNjgyOTlhYjI4YWJjYzBiMWY4ODE1NzJkODk1YzE4ZWE4In0=', '2019-03-01 22:34:28.323595');
INSERT INTO `django_session` VALUES ('jqg93apf6yrlukg0sj2rzmb0ny4r3is9', 'YWU1NTI2YjJlMmM5ZDZkODM1YmVlNTYwN2MwMDNmNGQ0Mjk5ZDFmMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZTVjYmYwOTNhNTAyODlkNzRmYTM5Y2NjMmI0YWRhN2VlOGMzZmNmIn0=', '2019-03-01 21:14:02.178644');
INSERT INTO `django_session` VALUES ('kydjj2ih3zt9q94fd8gxul175uvatj93', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 16:28:24.573554');
INSERT INTO `django_session` VALUES ('ounck730uc0hqr3pw1fxzapcmw690tmg', 'NTI2NGI5MjkxOTRhYmFkMDFjMDk0ZWYzMWVhMDUxYzhjMTAzZGQ1Mjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkYmJmNjcyNjgyOTlhYjI4YWJjYzBiMWY4ODE1NzJkODk1YzE4ZWE4In0=', '2019-03-01 22:39:45.835143');
INSERT INTO `django_session` VALUES ('scjkg1cubslqd2ckzf0ny2l785714kzx', 'YWU1NTI2YjJlMmM5ZDZkODM1YmVlNTYwN2MwMDNmNGQ0Mjk5ZDFmMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZTVjYmYwOTNhNTAyODlkNzRmYTM5Y2NjMmI0YWRhN2VlOGMzZmNmIn0=', '2019-03-01 20:21:10.111932');
INSERT INTO `django_session` VALUES ('sdwpfl0fqoznm0f1fohedd54791bbc6a', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 16:51:54.769034');
INSERT INTO `django_session` VALUES ('skqx911k3kke714d48a13kgximfr4q4t', 'YWU1NTI2YjJlMmM5ZDZkODM1YmVlNTYwN2MwMDNmNGQ0Mjk5ZDFmMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZTVjYmYwOTNhNTAyODlkNzRmYTM5Y2NjMmI0YWRhN2VlOGMzZmNmIn0=', '2019-03-01 21:39:15.759925');
INSERT INTO `django_session` VALUES ('td0xtixdbphwwh2alumldx8zr8elw1ku', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 19:39:25.696223');
INSERT INTO `django_session` VALUES ('tyzqykfaza1t2ell975cucowy0p35zt2', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 16:44:36.832669');
INSERT INTO `django_session` VALUES ('uzfse3l6vlf5wwemecz3fidvb6nlii45', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 15:52:54.071267');
INSERT INTO `django_session` VALUES ('xczu5q9b3jz1160v530yqer1fg9fthwt', 'NmIwM2M2OTQ4NmRiZTZiNDA4YjFhZDg4MWFkY2U5YmUyYjFmYWViMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuVXNlckJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzQ5YmFhMzk3NDM5NTUwZTRjOWNmYjQ5ZTc4OTcyYjNkOTQxNjAyIn0=', '2019-03-01 17:17:30.103634');

-- ----------------------------
-- Table structure for `personal_workorder`
-- ----------------------------
DROP TABLE IF EXISTS `personal_workorder`;
CREATE TABLE `personal_workorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `content` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of personal_workorder
-- ----------------------------

-- ----------------------------
-- Table structure for `users_userprofile`
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile`;
CREATE TABLE `users_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(100) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `type` varchar(20) NOT NULL,
  `joined_date` date DEFAULT NULL,
  `url` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users_userprofile
-- ----------------------------
INSERT INTO `users_userprofile` VALUES ('1', 'pbkdf2_sha256$36000$4cg1SAMlOhxd$ONEWDCYTR/kbWBuwpMIo1GUJvMsC+cHZgFUl9YF6KC0=', '2019-03-01 21:20:46.346118', '1', 'cheertt', 'cheertt', '油炸皮卡丘', '1913278504@163.com', '1', '1', '2019-03-01 14:56:48.298648', 'python1234', '15189939239', 'image/2019/03/timg01.jpg', '2', null, 'http://www/userlist/info1');
INSERT INTO `users_userprofile` VALUES ('2', 'pbkdf2_sha256$36000$9H74LKgjmfH1$vrDQCkKW6QP8iIlG2NtLnMI1q2jxPfzTiedPkOCxbQA=', '2019-03-01 22:18:53.028803', '0', 'xieliangcai', '', '', '1913278504@qq.com', '0', '1', '2019-03-01 21:49:12.681480', '谢良才', '123213213', 'image/default.jpg', '2', '2018-03-01', '123123');
INSERT INTO `users_userprofile` VALUES ('6', 'pbkdf2_sha256$36000$vdDsX0LS9QWZ$nU99HmCmNicscu7p+zmUXinBXeiB42SBB/CcQloJhD8=', null, '0', 'jinxiaoxiao', '', '', '123213@qq.com', '0', '1', '2019-03-01 22:05:59.613337', '金晓骁', '12321321123', 'image/default.jpg', '2', '2018-03-01', '12321321');
INSERT INTO `users_userprofile` VALUES ('7', 'pbkdf2_sha256$36000$9NMMLMHjrrYw$Xa5mVlGFI+eRR9l82Pg1sa9vEbTZZ6gVf1rIBqqq1vY=', null, '0', 'wenting', '', '', '123213213@163.com', '0', '1', '2019-03-01 22:06:47.126149', '闻婷', '31234123312', 'image/default.jpg', '2', '2018-03-01', '12321321');
INSERT INTO `users_userprofile` VALUES ('8', 'pbkdf2_sha256$36000$2kFSpds3N2R1$7dWbWAHZtLcEfhTK6EcC7NacAIPOko7Cd/T3fgOopRA=', null, '0', 'liyuming', '', '', '213213@qq.com', '0', '1', '2019-03-01 22:08:06.364512', '李玉明', '12321321312', 'image/default.jpg', '2', '2018-03-01', '12321321');
INSERT INTO `users_userprofile` VALUES ('9', 'pbkdf2_sha256$36000$ZD7aSifMVKnT$pw7La9lrynJRZSdW8nxMoeJoyM8akGUdrRHUcxYcmIk=', null, '0', 'xiaohongjian', '', '', '21312@qq.com', '0', '1', '2019-03-01 22:08:47.230323', '肖鸿健', '21312', 'image/default.jpg', '2', '2018-03-01', '13221');
INSERT INTO `users_userprofile` VALUES ('10', 'pbkdf2_sha256$36000$UPVytfwO0Ouf$pVpiswFy3nERFJL8RVQT2WUKgC7BG7XSE5UeuEigLxA=', null, '0', 'litaotao', '', '', 'wqe@qq.com', '0', '1', '2019-03-01 22:09:26.266046', '李逃跑他', '12321321312', 'image/default.jpg', '2', '2018-03-01', '1212312');
INSERT INTO `users_userprofile` VALUES ('11', 'pbkdf2_sha256$36000$SDJV5zaWVJuS$dyVl1H4GwwZfQiK96Hw9uo2+c0/L+4v77CyhaiGughY=', null, '0', 'test1', '', '', '21312@qq.com', '0', '1', '2019-03-01 22:09:47.816733', 'test1', '21312', 'image/default.jpg', '2', '2018-03-01', '12231');
INSERT INTO `users_userprofile` VALUES ('12', 'pbkdf2_sha256$36000$tRgxYxHNonVr$pF3e+Z1c7BO9AbgE6ttSvme6nnHdbXJPUF5OGyY1n2g=', null, '0', 'test2', '', '', '1913278504@qq.com', '0', '1', '2019-03-01 22:10:05.270828', 'test2', '12312', 'image/default.jpg', '2', '2018-03-01', '21312');
INSERT INTO `users_userprofile` VALUES ('13', 'pbkdf2_sha256$36000$rsrRwrXel1He$6pbm+0bUUO66Slw6oD5P0hWhqpg+UGGJn0ADT7nhInI=', null, '0', 'test3', '', '', '1913278504@qq.com', '0', '0', '2019-03-01 22:10:31.304663', 'test3', 'qweqw', 'image/default.jpg', '2', '2018-03-01', 'ewqe');
INSERT INTO `users_userprofile` VALUES ('14', 'pbkdf2_sha256$36000$N2rZQTnoCjqV$OcbhWaAoTbWn+Wx15Z/vh6YtypDLrfxztpoNwcWcpdE=', null, '0', 'test4', '', '', '123213213@163.com', '0', '0', '2019-03-01 22:10:57.123349', 'test4', '12123', 'image/default.jpg', '2', '2018-03-01', '3123123');

-- ----------------------------
-- Table structure for `users_userprofile_groups`
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile_groups`;
CREATE TABLE `users_userprofile_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_userprofile_groups_userprofile_id_group_id_823cf2fc_uniq` (`userprofile_id`,`group_id`),
  KEY `users_userprofile_groups_group_id_3de53dbf_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_userprofile_gr_userprofile_id_a4496a80_fk_users_use` FOREIGN KEY (`userprofile_id`) REFERENCES `users_userprofile` (`id`),
  CONSTRAINT `users_userprofile_groups_group_id_3de53dbf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users_userprofile_groups
-- ----------------------------

-- ----------------------------
-- Table structure for `users_userprofile_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile_user_permissions`;
CREATE TABLE `users_userprofile_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_userprofile_user_p_userprofile_id_permissio_d0215190_uniq` (`userprofile_id`,`permission_id`),
  KEY `users_userprofile_us_permission_id_393136b6_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_userprofile_us_permission_id_393136b6_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_userprofile_us_userprofile_id_34544737_fk_users_use` FOREIGN KEY (`userprofile_id`) REFERENCES `users_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users_userprofile_user_permissions
-- ----------------------------
