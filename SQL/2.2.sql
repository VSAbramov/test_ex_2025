WITH RECURSIVE lvl_cat AS (
    SELECT id, name, parent_id, 0 as lvl FROM categories 
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, lc.lvl + 1 AS lvl FROM categories c
    INNER JOIN lvl_cat lc ON c.parent_id = lc.id WHERE lc.lvl < 1
)
SELECT 
    p.name AS name, 
    COUNT(c.id) AS quantity
FROM lvl_cat p
LEFT JOIN categories c ON c.parent_id = p.id
WHERE p.parent_id IS NULL
GROUP BY p.id, p.name;