create table tmp as select max(id) as cola from fa_wanlshop_goods_comment group by goods_id,content;
delete from fa_wanlshop_goods_comment where id not in (select cola from tmp);
drop table tmp;


删 除重复数据