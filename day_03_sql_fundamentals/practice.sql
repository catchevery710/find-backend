-- ============================================================
-- Day 03 SQL Cumulative Review
--
-- Topics:
-- CREATE TABLE
-- INSERT
-- SELECT
-- WHERE
-- ORDER BY
-- LIMIT
-- UPDATE
-- DELETE
-- COUNT / SUM / AVG / MIN / MAX
-- GROUP BY
-- HAVING
-- DISTINCT
-- IN
-- BETWEEN
-- LIKE
-- NULL
-- AS
-- Primary Key
-- Foreign Key
-- ============================================================


-- ============================================================
-- 1. CREATE TABLE
-- ============================================================

-- products 是表名。
--
-- id:
-- INTEGER
-- PRIMARY KEY → 唯一标识一条记录
--
-- name / price:
-- NOT NULL → 不能是 NULL

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);


-- ============================================================
-- 2. INSERT
-- ============================================================

-- 插入一条数据。

INSERT INTO products (id, name, price)
VALUES (1, 'phone', 1000);

INSERT INTO products (id, name, price)
VALUES (2, 'laptop', 2000);


-- ============================================================
-- 3. 一次 INSERT 多行
-- ============================================================

INSERT INTO products (id, name, price)
VALUES
    (3, 'keyboard', 500),
    (4, 'monitor', 1500);


-- ============================================================
-- 4. SELECT
-- ============================================================

-- 查询所有列。

SELECT *
FROM products;


-- 查询指定列。

SELECT name, price
FROM products;


-- ============================================================
-- 5. WHERE
-- ============================================================

-- 查询 id = 2。

SELECT *
FROM products
WHERE id = 2;


-- 查询价格 >= 1000。

SELECT *
FROM products
WHERE price >= 1000;


-- ============================================================
-- 6. ORDER BY
-- ============================================================

-- ASC:
-- 从小到大。

SELECT *
FROM products
ORDER BY price ASC;


-- DESC:
-- 从大到小。

SELECT *
FROM products
ORDER BY price DESC;


-- ============================================================
-- 7. LIMIT
-- ============================================================

-- 只返回前两条。

SELECT *
FROM products
LIMIT 2;


-- 查询价格最高的两个商品。

SELECT *
FROM products
ORDER BY price DESC
LIMIT 2;


-- WHERE + ORDER BY + LIMIT 可以组合。

SELECT *
FROM products
WHERE price >= 1000
ORDER BY price DESC
LIMIT 2;


-- ============================================================
-- 8. UPDATE
-- ============================================================

-- 修改 id = 2 的价格。

UPDATE products
SET price = 1800
WHERE id = 2;


-- 同时修改多个字段。

UPDATE products
SET name = 'gaming laptop',
    price = 2500
WHERE id = 2;


-- 注意：
--
-- UPDATE products
-- SET price = 999;
--
-- 如果没有 WHERE，
-- 所有行都会被修改。


-- ============================================================
-- 9. DELETE
-- ============================================================

DELETE FROM products
WHERE id = 4;


-- 注意：
--
-- DELETE FROM products;
--
-- 会删除表中所有数据，
-- 但是 products 表本身仍然存在。


-- ============================================================
-- 10. Aggregation Functions
-- 聚合函数
-- ============================================================


-- COUNT
-- 统计数据数量。

SELECT COUNT(*)
FROM products;


-- SUM
-- 价格总和。

SELECT SUM(price)
FROM products;


-- AVG
-- 平均价格。

SELECT AVG(price)
FROM products;


-- MIN
-- 最低价格。

SELECT MIN(price)
FROM products;


-- MAX
-- 最高价格。

SELECT MAX(price)
FROM products;


-- WHERE + 聚合。

SELECT COUNT(*)
FROM products
WHERE price >= 1000;


-- ============================================================
-- 11. 添加 category
-- ============================================================

ALTER TABLE products
ADD COLUMN category TEXT;


-- 给不同商品设置 category。

UPDATE products
SET category = 'electronics'
WHERE id IN (1, 2);

UPDATE products
SET category = 'accessories'
WHERE id IN (3, 4);


-- ============================================================
-- 12. GROUP BY
-- ============================================================

-- 按 category 分组，
-- 然后统计每组数量。

SELECT category, COUNT(*)
FROM products
GROUP BY category;


-- 每个 category 的平均价格。

SELECT category, AVG(price)
FROM products
GROUP BY category;


-- ============================================================
-- 13. HAVING
-- ============================================================

-- WHERE:
-- 分组之前筛选原始数据。
--
-- HAVING:
-- GROUP BY 之后筛选组。


-- 查询平均价格 >= 1000 的 category。

SELECT category, AVG(price)
FROM products
GROUP BY category
HAVING AVG(price) >= 1000;


-- 查询商品数量 >= 2 的 category。

SELECT category, COUNT(*)
FROM products
GROUP BY category
HAVING COUNT(*) >= 2;


-- WHERE + GROUP BY + HAVING。

SELECT category, COUNT(*)
FROM products
WHERE price >= 500
GROUP BY category
HAVING COUNT(*) >= 2;


-- ============================================================
-- 14. DISTINCT
-- ============================================================

-- 去除重复结果。

SELECT DISTINCT category
FROM products;


-- ============================================================
-- 15. IN
-- ============================================================

-- id 是 1、2、4 中的任意一个。

SELECT *
FROM products
WHERE id IN (1, 2, 4);


-- ============================================================
-- 16. BETWEEN
-- ============================================================

-- BETWEEN 包含两边界。
--
-- 等价于：
-- price >= 500 AND price <= 1500

SELECT *
FROM products
WHERE price BETWEEN 500 AND 1500;


-- ============================================================
-- 17. LIKE
-- ============================================================

-- %:
-- 任意长度字符。


-- 包含 phone。

SELECT *
FROM products
WHERE name LIKE '%phone%';


-- 以 lap 开头。

SELECT *
FROM products
WHERE name LIKE 'lap%';


-- 以 phone 结尾。

SELECT *
FROM products
WHERE name LIKE '%phone';


-- ============================================================
-- 18. NULL
-- ============================================================

-- NULL 不是普通值。
--
-- 不能写：
-- category = NULL


-- category 没有值。

SELECT *
FROM products
WHERE category IS NULL;


-- category 有值。

SELECT *
FROM products
WHERE category IS NOT NULL;


-- ============================================================
-- 19. AS
-- ============================================================

-- 给结果列起一个临时名称。

SELECT AVG(price) AS average_price
FROM products;


-- ============================================================
-- 20. Primary Key / Foreign Key
-- ============================================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product TEXT NOT NULL,

    -- orders.user_id
    -- 指向 users.id

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);


-- ============================================================
-- Primary Key:
-- 唯一标识“我是谁”
--
-- Foreign Key:
-- 表示“我关联谁”
--
-- users.id
-- → Primary Key
--
-- orders.user_id
-- → Foreign Key
-- → REFERENCES users(id)
-- ============================================================


-- ============================================================
-- Day 03 核心总结
--
-- CRUD:
--
-- Create → INSERT
-- Read   → SELECT
-- Update → UPDATE
-- Delete → DELETE
--
--
-- WHERE
-- → 筛选原始数据
--
-- GROUP BY
-- → 分组
--
-- HAVING
-- → 筛选分组后的结果
--
--
-- ASC
-- → 小到大
--
-- DESC
-- → 大到小
-- ============================================================





