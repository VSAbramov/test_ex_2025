CREATE VIEW top_5_items_last_month AS
WITH root_categories AS (
    -- Recursive CTE to find root categories
    WITH RECURSIVE category_path AS (
        SELECT id, name, parent_id, name AS root_name
        FROM categories
        WHERE parent_id IS NULL
        UNION ALL
        SELECT c.id, c.name, c.parent_id, cp.root_name
        FROM categories c
        JOIN category_path cp ON c.parent_id = cp.id
    )
    SELECT id, root_name FROM category_path
),
last_month_orders AS (
    -- Get orders from last month
    SELECT id 
    FROM orders 
    WHERE created_at >= date('now', 'start of month', '-1 month')
      AND created_at < date('now', 'start of month')
)
SELECT 
    i.name AS item_name,
    COALESCE(rc.root_name, 'Uncategorized') AS category_name,
    SUM(oi.quantity) AS quantity_sold
FROM order_items oi
JOIN last_month_orders lmo ON oi.order_id = lmo.id
JOIN items i ON oi.item_id = i.id
LEFT JOIN root_categories rc ON i.category_id = rc.id
GROUP BY i.id, i.name, rc.root_name
ORDER BY quantity_sold DESC
LIMIT 5;