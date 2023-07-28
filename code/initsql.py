import linksql


def init_sql(root_id, password):
    link = linksql.bigflySQL()
    link.root_link(root_id, password)

    # 创建数据库
    link.execute("create DATABASE bigflydb")

    # 创建数据库管理员账号
    link.execute("create user bigfly identified by 'bigfly';")  # 账号密码仅供参考
    link.execute("grant all privileges on bigflydb.* to bigfly@'%';")

    # 创建查询账号
    link.execute("create user bigflyselect identified by 'bigflyselect';")
    link.execute("grant select on bigflydb.* to bigflyselect@'%';")

    link.execute("flush privileges;")
    link.execute("use bigflydb;")

    # 创建用户信息表
    link.execute("""
    CREATE TABLE `bigflydb`.`user_info` (
      `uid` INT NOT NULL,
      `name` VARCHAR(512) NULL,
      `email` VARCHAR(512) NULL,
      `tele` VARCHAR(512) NULL,
      `password` VARCHAR(512) NULL,
      `wechat` VARCHAR(512) NULL,
      `weibo` VARCHAR(512) NULL,
      `ischeck` TINYINT ZEROFILL NULL DEFAULT 0,
      `isfrozen` TINYINT ZEROFILL NULL DEFAULT 0,
      PRIMARY KEY (`uid`),
      UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
      UNIQUE INDEX `tele_UNIQUE` (`tele` ASC) VISIBLE,
      UNIQUE INDEX `wechat_UNIQUE` (`wechat` ASC) VISIBLE);
    """)

    link.execute("""
    DROP TRIGGER IF EXISTS `bigflydb`.`user_info_BEFORE_INSERT`;
    """)

    link.execute("""
    USE `bigflydb`;
    """)

    link.execute("""
    CREATE DEFINER = CURRENT_USER TRIGGER `bigflydb`.`user_info_BEFORE_INSERT` BEFORE INSERT ON `user_info` FOR EACH ROW
    BEGIN
        declare randid int;
        label:
        while true do
            set randid = (select floor(100000 + rand() * 999999999));
            if randid not in (select uid from user_info) then
                leave label;
            end if;
        end while;
        set new.uid = randid;
    END
    """)

    link.execute("""
    CREATE TABLE `bigflydb`.`file_info` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `filename` VARCHAR(45) NOT NULL,
      `owner_uid` INT NOT NULL,
      `upload_date` DATE NOT NULL,
      `filehash` VARCHAR(512) NOT NULL,
      `invalid_date` DATE NOT NULL,
      `isshared` TINYINT DEFAULT 0, 
      `filesize` INT NOT NULL,
      PRIMARY KEY (`id`));
    """)

    link.execute("""
    DROP TRIGGER IF EXISTS `bigflydb`.`file_info_BEFORE_INSERT`;
    
    DELIMITER $$
    USE `bigflydb`$$
    CREATE DEFINER=`bigfly`@`%` TRIGGER `file_info_BEFORE_INSERT` BEFORE INSERT ON `file_info` FOR EACH ROW BEGIN
        set new.upload_date = current_date();
        set new.invalid_date = date_add(new.upload_date, interval +30 day);
    END$$
    DELIMITER ;
    """)

    link.end_link()
