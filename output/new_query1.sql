SELECT order_month,
       order_day,
       count(DISTINCT order_id) AS num_orders,
       count(book_id) AS num_books,
       sum(price) AS total_price,
       sum(count(book_id)) OVER (PARTITION BY order_month
                                 ORDER BY order_day) AS running_total_num_books,
                                lag(count(book_id), 1) OVER (
                                                             ORDER BY order_day) AS prev_books
FROM
  (SELECT date_format(co.order_date, '%Y-%m') AS order_month,
          date_format(co.order_date, '%Y-%m-%d') AS order_day,
          co.order_id,
          ol.book_id,
          ol.price
   FROM cust_order AS co
   INNER JOIN order_line AS ol ON co.order_id = ol.order_id) AS sub
GROUP BY order_month,
         order_day
ORDER BY order_day ASC