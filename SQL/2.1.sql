SELECT 
	c.name, 
	COALESCE(SUM(oi.quantity * i.price), 0) AS total_price 
	FROM clients c
LEFT JOIN orders o ON c.id=o.client_id 
LEFT JOIN order_items oi ON oi.order_id = o.id
LEFT JOIN items i ON i.id = oi.item_id
GROUP BY c.id;
