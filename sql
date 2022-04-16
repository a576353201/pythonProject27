create table tmp as select max(id) as cola from fa_wanlshop_goods_comment group by goods_id,content;
delete from fa_wanlshop_goods_comment where id not in (select cola from tmp);
drop table tmp;


删 除重复数据



update   fa_wanlshop_goods_sku s,fa_wanlshop_goods g set  s.price=s. market_price+s.market_price*0.1 where s.goods_id=g.id and g.shop_id=34


更新关联表

分组查询次数：
SELECT

goods_id,

FROM
fa_wanlshop_goods_spu
GROUP BY
goods_id
HAVING count(goods_id) >1


SELECT goods_id,
fa_wanlshop_goods_sku.difference
FROM fa_wanlshop_goods_sku
WHERE difference not like  "%,%";


SELECT k.goods_id,
k.difference
FROM fa_wanlshop_goods_sku as k LEFT JOIN  fa_wanlshop_goods_spu as s
on k.goods_id=s.goods_id
WHERE k.difference not like  "%,%" GROUP BY
s.goods_id
HAVING count(s.goods_id) >1


SELECT s.goods_id,
k.proid
FROM fa_wanlshop_goods as k LEFT JOIN  fa_wanlshop_goods_spu as s
on k.id=s.goods_id
 GROUP BY
s.goods_id
HAVING count(s.goods_id) >1

update fa_wanlshop_goods set proid=(SELECT proid FROM fa_wanlshop_wholesale where fa_wanlshop_goods.wholesale_id= fa_wanlshop_wholesale.id)