create table tmp as select max(id) as cola from fa_wanlshop_goods_comment group by goods_id,content;
delete from fa_wanlshop_goods_comment where id not in (select cola from tmp);
drop table tmp;


删 除重复数据



update   fa_wanlshop_goods_sku s,fa_wanlshop_goods g set  s.price=s. market_price+s.market_price*0.1 where s.goods_id=g.id and g.shop_id=34


更新关联表