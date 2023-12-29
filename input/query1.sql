SELECT
order_month,
order_day,
COUNT(DISTINCT order_id) AS num_orders,
COUNT(book_id) AS num_books,
SUM(price) AS total_price,
SUM(COUNT(book_id)) OVER (
  PARTITION BY order_month
  ORDER BY order_day
) AS running_total_num_books,
LAG(COUNT(book_id), 1) OVER (ORDER BY order_day) AS prev_books
FROM (
  SELECT
  DATE_FORMAT(co.order_date, '%Y-%m') AS order_month,
  DATE_FORMAT(co.order_date, '%Y-%m-%d') AS order_day,
  co.order_id,
  ol.book_id,
  ol.price
  FROM cust_order co
  INNER JOIN order_line ol ON co.order_id = ol.order_id
) sub
GROUP BY order_month, order_day
ORDER BY order_day ASC;