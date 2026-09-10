-- ============================================================
-- Day 04 - SQL Relationships, JOIN and GROUP BY Review
-- ============================================================


-- ============================================================
-- 0. 初始化练习数据库
-- ============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;


-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


-- 商品表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);


-- 订单表
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    amount INTEGER NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
);


INSERT INTO users (id, name)
VALUES
    (1, 'Alice'),
    (2, 'Bob'),
    (3, 'Charlie');


INSERT INTO products (id, name, price)
VALUES
    (1, 'phone', 1000),
    (2, 'laptop', 2000),
    (3, 'keyboard', 500),
    (4, 'mouse', 300);


INSERT INTO orders (
    id,
    user_id,
    product_id,
    quantity,
    amount
)
VALUES
    (1, 1, 1, 2, 2000),
    (2, 1, 2, 1, 2000),
    (3, 2, 3, 3, 1500),
    (4, 1, 1, 1, 1000);



-- ============================================================
-- 1. INNER JOIN
--
-- 只保留两张表中能够匹配的数据
-- ============================================================

SELECT
    o.id AS order_id,
    u.name AS user_name,
    o.amount
FROM orders AS o
INNER JOIN users AS u
ON o.user_id = u.id;



-- ============================================================
-- 2. ON 和 WHERE
--
-- ON:
-- 定义两张表如何连接
--
-- WHERE:
-- 对连接后的数据继续筛选
-- ============================================================

SELECT
    o.id AS order_id,
    u.name AS user_name,
    o.amount
FROM orders AS o
INNER JOIN users AS u
ON o.user_id = u.id
WHERE o.amount >= 2000;



-- ============================================================
-- 3. LEFT JOIN
--
-- LEFT JOIN 会保留左表的所有记录
--
-- 题目说：
-- "所有用户都要显示"
--
-- 那么 users 应该放在 FROM 后面
-- ============================================================

SELECT
    u.id,
    u.name,
    o.amount
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id;



-- ============================================================
-- 4. 找出没有订单的用户
--
-- LEFT JOIN 之后：
-- 没有匹配订单的用户，其 orders 字段会变成 NULL
--
-- 推荐检查右表主键：
-- o.id IS NULL
-- ============================================================

SELECT
    u.id,
    u.name
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
WHERE o.id IS NULL;



-- ============================================================
-- 5. JOIN + COUNT
--
-- 查询所有用户分别有多少笔订单
--
-- COUNT(o.id) 不统计 NULL
-- 因此 Charlie 会得到 0
-- ============================================================

SELECT
    u.name AS user_name,
    COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name;



-- ============================================================
-- 6. JOIN + SUM
--
-- 查询所有用户的总消费
--
-- 没订单：
-- SUM(...) 会得到 NULL
-- ============================================================

SELECT
    u.name AS user_name,
    SUM(o.amount) AS total_amount
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name;



-- ============================================================
-- 7. COALESCE
--
-- COALESCE(value, 0)
-- 如果 value 是 NULL，就返回 0
-- ============================================================

SELECT
    u.name AS user_name,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name;



-- ============================================================
-- 8. COUNT + SUM 综合
--
-- order_count:
-- 订单笔数
--
-- total_amount:
-- 总消费金额
-- ============================================================

SELECT
    u.name AS user_name,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name;



-- ============================================================
-- 9. HAVING
--
-- WHERE:
-- 分组前过滤普通行
--
-- HAVING:
-- GROUP BY 后过滤分组结果
--
-- 查询总消费 >= 2500 的用户
-- ============================================================

SELECT
    u.name AS user_name,
    SUM(o.amount) AS total_amount
FROM users AS u
INNER JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING SUM(o.amount) >= 2500;



-- ============================================================
-- 10. HAVING + ORDER BY
--
-- 总消费 >= 1000
-- 并按照总消费从高到低排列
-- ============================================================

SELECT
    u.name AS user_name,
    SUM(o.amount) AS total_amount
FROM users AS u
INNER JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING SUM(o.amount) >= 1000
ORDER BY total_amount DESC;



-- ============================================================
-- 11. 三表 JOIN
--
-- users 和 products 不直接连接
--
-- 关系：
--
-- users.id
--     ↑
-- orders.user_id
--
-- orders.product_id
--     ↓
-- products.id
--
-- orders 是中间表
-- ============================================================

SELECT
    o.id AS order_id,
    u.name AS user_name,
    p.name AS product_name,
    o.quantity,
    o.amount
FROM orders AS o
INNER JOIN users AS u
ON o.user_id = u.id
INNER JOIN products AS p
ON o.product_id = p.id;



-- ============================================================
-- 12. 三表 JOIN + GROUP BY
--
-- 查询：
-- 每个用户对每一种商品总共购买多少件
--
-- "每个用户 + 每种商品"
-- → GROUP BY 用户 + 商品
--
-- "总共多少件"
-- → SUM(quantity)
-- ============================================================

SELECT
    u.name AS user_name,
    p.name AS product_name,
    SUM(o.quantity) AS total_quantity
FROM orders AS o
INNER JOIN users AS u
ON o.user_id = u.id
INNER JOIN products AS p
ON o.product_id = p.id
GROUP BY
    u.id,
    u.name,
    p.id,
    p.name;



-- ============================================================
-- 13. 不同商品种类 + 总件数 + 总金额
--
-- COUNT(DISTINCT product_id)
-- → 买过多少种不同商品
--
-- SUM(quantity)
-- → 总共买多少件
--
-- SUM(amount)
-- → 总消费多少钱
--
-- 注意：
-- 这题不需要 products 表
-- 因为 orders 已经有 product_id
-- ============================================================

SELECT
    u.name AS user_name,
    COUNT(DISTINCT o.product_id) AS product_type_count,
    SUM(o.quantity) AS total_quantity,
    SUM(o.amount) AS total_amount
FROM orders AS o
INNER JOIN users AS u
ON o.user_id = u.id
GROUP BY u.id, u.name;



-- ============================================================
-- 14. 按商品统计销量
--
-- 查询实际卖出去的商品：
-- 总销量 + 总销售额
-- ============================================================

SELECT
    p.name AS product_name,
    SUM(o.quantity) AS total_quantity,
    SUM(o.amount) AS total_sales
FROM orders AS o
INNER JOIN products AS p
ON o.product_id = p.id
GROUP BY p.id, p.name;



-- ============================================================
-- 15. 所有商品都显示
--
-- 包括完全没有卖出去的 mouse
--
-- 题目主体：
-- 所有商品
--
-- 所以：
-- FROM products
--
-- LEFT JOIN orders
-- ============================================================

SELECT
    p.name AS product_name,
    COALESCE(SUM(o.quantity), 0) AS total_quantity,
    COALESCE(SUM(o.amount), 0) AS total_sales
FROM products AS p
LEFT JOIN orders AS o
ON p.id = o.product_id
GROUP BY p.id, p.name;



-- ============================================================
-- 16. LEFT JOIN + GROUP BY + HAVING + ORDER BY
--
-- 查询所有商品，
-- 最终只显示总销量 >= 2 的商品
-- 并按销量降序
-- ============================================================

SELECT
    p.name AS product_name,
    SUM(o.quantity) AS total_quantity
FROM products AS p
LEFT JOIN orders AS o
ON p.id = o.product_id
GROUP BY p.id, p.name
HAVING SUM(o.quantity) >= 2
ORDER BY total_quantity DESC;



-- ============================================================
-- 17. 所有用户综合统计
--
-- 所有用户都必须显示，包括 Charlie
--
-- product_type_count:
-- 买过多少种不同商品
--
-- total_quantity:
-- 买了多少件
--
-- total_amount:
-- 总消费
-- ============================================================

SELECT
    u.name AS user_name,
    COUNT(DISTINCT o.product_id) AS product_type_count,
    COALESCE(SUM(o.quantity), 0) AS total_quantity,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_amount DESC;



-- ============================================================
-- Day 04 核心速记
-- ============================================================

-- INNER JOIN
-- → 只保留匹配成功的数据


-- LEFT JOIN
-- → 保留左表全部数据
--
-- 所以先看题目：
-- "所有谁都要显示？"
-- 谁就通常应该放在 FROM 后面


-- ON
-- → 两张表怎么连接


-- WHERE
-- → 分组前过滤普通数据


-- GROUP BY
-- → "每个谁" 就按谁分组


-- HAVING
-- → 分组完成以后过滤聚合结果


-- ORDER BY
-- → 对最终结果排序


-- COUNT(o.id)
-- → 订单笔数


-- COUNT(DISTINCT o.product_id)
-- → 不同商品种类数


-- SUM(o.quantity)
-- → 商品总件数


-- SUM(o.amount)
-- → 总金额


-- COALESCE(SUM(...), 0)
-- → NULL 转成 0


-- 三表关系：
--
-- users ← orders → products
--
-- orders.user_id = users.id
-- orders.product_id = products.id


-- 最重要的做题顺序：
--
-- 1. 统计主体是谁？
--    → FROM
--
-- 2. 主体全部保留吗？
--    → INNER JOIN / LEFT JOIN
--
-- 3. 表之间怎么连接？
--    → ON 外键 = 主键
--
-- 4. 统计什么？
--    → COUNT / SUM / AVG ...
--
-- 5. 每个谁？
--    → GROUP BY
--
-- 6. 聚合结果是否还要筛选？
--    → HAVING
--
-- 7. 是否排序？
--    → ORDER BY






