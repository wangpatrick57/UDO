# from __future__ import with_statement
#
# import os
# import sys
# import logging
# import MySQLdb
# from pprint import pprint, pformat
#
# import constants
# from abstractdriver import *
#
# TXN_QUERIES = {
#     "DELIVERY": {
#         "getNewOrder": "SELECT NO_O_ID FROM NEW_ORDER WHERE NO_D_ID = %s AND NO_W_ID = %s ORDER BY NO_O_ID ASC LIMIT 1",
#         #
#         "deleteNewOrder": "DELETE FROM NEW_ORDER WHERE NO_D_ID = %s AND NO_W_ID = %s AND NO_O_ID = %s",
#         # d_id, w_id, no_o_id
#         "getCId": "SELECT O_C_ID FROM ORDERS WHERE O_ID = %s AND O_D_ID = %s AND O_W_ID = %s",  # no_o_id, d_id, w_id
#         "updateOrders": "UPDATE ORDERS SET O_CARRIER_ID = %s WHERE O_ID = %s AND O_D_ID = %s AND O_W_ID = %s",
#         # o_carrier_id, no_o_id, d_id, w_id
#         "updateOrderLine": "UPDATE ORDER_LINE SET OL_DELIVERY_D = %s WHERE OL_O_ID = %s AND OL_D_ID = %s AND OL_W_ID = %s",
#         # o_entry_d, no_o_id, d_id, w_id
#         "sumOLAmount": "SELECT SUM(OL_AMOUNT) FROM ORDER_LINE WHERE OL_O_ID = %s AND OL_D_ID = %s AND OL_W_ID = %s",
#         # no_o_id, d_id, w_id
#         "updateCustomer": "UPDATE CUSTOMER SET C_BALANCE = C_BALANCE + %s, C_DELIVERY_CNT = C_DELIVERY_CNT + 1 WHERE C_ID = %s AND C_D_ID = %s AND C_W_ID = %s",
#         # ol_total, c_id, d_id, w_id
#     },
#     "NEW_ORDER": {
#         "getWarehouseTaxRate": "SELECT W_TAX FROM WAREHOUSE WHERE W_ID = %s",  # w_id
#         "getDistrict": "SELECT D_TAX, D_NEXT_O_ID FROM DISTRICT WHERE D_ID = %s AND D_W_ID = %s FOR UPDATE",
#         # d_id, w_id
#         "incrementNextOrderId": "UPDATE DISTRICT SET D_NEXT_O_ID = %s WHERE D_ID = %s AND D_W_ID = %s",
#         # d_next_o_id, d_id, w_id
#         "getCustomer": "SELECT C_DISCOUNT, C_LAST, C_CREDIT FROM CUSTOMER WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s",
#         # w_id, d_id, c_id
#         "createOrder": "INSERT INTO ORDERS (O_ID, O_D_ID, O_W_ID, O_C_ID, O_ENTRY_D, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#         # d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, o_ol_cnt, o_all_local
#         "createNewOrder": "INSERT INTO NEW_ORDER (NO_O_ID, NO_D_ID, NO_W_ID) VALUES (%s, %s, %s)",  # o_id, d_id, w_id
#         "getItemInfo": "SELECT I_PRICE, I_NAME, I_DATA FROM ITEM WHERE I_ID = %s",  # ol_i_id
#         "getStockInfo": "SELECT S_QUANTITY, S_DATA, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, S_DIST_%02d FROM STOCK WHERE S_I_ID = %s AND S_W_ID = %s FOR UPDATE",
#         # d_id, ol_i_id, ol_supply_w_id
#         "updateStock": "UPDATE STOCK SET S_QUANTITY = %s, S_YTD = %s, S_ORDER_CNT = %s, S_REMOTE_CNT = %s WHERE S_I_ID = %s AND S_W_ID = %s",
#         # s_quantity, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id
#         "createOrderLine": "INSERT INTO ORDER_LINE (OL_O_ID, OL_D_ID, OL_W_ID, OL_NUMBER, OL_I_ID, OL_SUPPLY_W_ID, OL_DELIVERY_D, OL_QUANTITY, OL_AMOUNT, OL_DIST_INFO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#         # o_id, d_id, w_id, ol_number, ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_dist_info
#     },
#
#     "ORDER_STATUS": {
#         "getCustomerByCustomerId": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM CUSTOMER WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s",
#         # w_id, d_id, c_id
#         "getCustomersByLastName": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM CUSTOMER WHERE C_W_ID = %s AND C_D_ID = %s AND C_LAST = %s ORDER BY C_FIRST",
#         # w_id, d_id, c_last
#         "getLastOrder": "SELECT O_ID, O_CARRIER_ID, O_ENTRY_D FROM ORDERS WHERE O_W_ID = %s AND O_D_ID = %s AND O_C_ID = %s ORDER BY O_ID DESC LIMIT 1",
#         # w_id, d_id, c_id
#         "getOrderLines": "SELECT OL_SUPPLY_W_ID, OL_I_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D FROM ORDER_LINE WHERE OL_W_ID = %s AND OL_D_ID = %s AND OL_O_ID = %s",
#         # w_id, d_id, o_id
#     },
#
#     "PAYMENT": {
#         "getWarehouse": "SELECT W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP FROM WAREHOUSE WHERE W_ID = %s",
#         # w_id
#         "updateWarehouseBalance": "UPDATE WAREHOUSE SET W_YTD = W_YTD + %s WHERE W_ID = %s",  # h_amount, w_id
#         "getDistrict": "SELECT D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP FROM DISTRICT WHERE D_W_ID = %s AND D_ID = %s",
#         # w_id, d_id
#         "updateDistrictBalance": "UPDATE DISTRICT SET D_YTD = D_YTD + %s WHERE D_W_ID  = %s AND D_ID = %s",
#         # h_amount, d_w_id, d_id
#         "getCustomerByCustomerId": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DATA FROM CUSTOMER WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s",
#         # w_id, d_id, c_id
#         "getCustomersByLastName": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DATA FROM CUSTOMER WHERE C_W_ID = %s AND C_D_ID = %s AND C_LAST = %s ORDER BY C_FIRST",
#         # w_id, d_id, c_last
#         "updateBCCustomer": "UPDATE CUSTOMER SET C_BALANCE = %s, C_YTD_PAYMENT = %s, C_PAYMENT_CNT = %s, C_DATA = %s WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s",
#         # c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id
#         "updateGCCustomer": "UPDATE CUSTOMER SET C_BALANCE = %s, C_YTD_PAYMENT = %s, C_PAYMENT_CNT = %s WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s",
#         # c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id
#         "insertHistory": "INSERT INTO HISTORY VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#     },
#
#     "STOCK_LEVEL": {
#         "getOId": "SELECT D_NEXT_O_ID FROM DISTRICT WHERE D_W_ID = %s AND D_ID = %s",
#         "getStockCount": """
#             SELECT COUNT(DISTINCT(OL_I_ID)) FROM ORDER_LINE, STOCK
#             WHERE OL_W_ID = %s
#               AND OL_D_ID = %s
#               AND OL_O_ID < %s
#               AND OL_O_ID >= %s
#               AND S_W_ID = %s
#               AND S_I_ID = OL_I_ID
#               AND S_QUANTITY < %s
#         """,
#     },
# }
#
#
# # delivery_order = ["getNewOrder", "deleteNewOrder", "getCId", "updateOrders", "updateOrderLine", "sumOLAmount",
# #                   "updateCustomer"]
# #
# # payment_order = ["getWarehouse", "updateWarehouseBalance", "getDistrict", "updateDistrictBalance",
# #                  "getCustomerByCustomerId",
# #                  "getCustomersByLastName", "updateBCCustomer", "updateGCCustomer", "insertHistory"]
# #
# # new_order_order = ["getWarehouseTaxRate", "getDistrict", "incrementNextOrderId", "getCustomer", "createOrder",
# #                    "createNewOrder", "getItemInfo", "getStockInfo", "updateStock", "createOrderLine"]
#
# class MysqlDriver(AbstractDriver):
#     DEFAULT_CONFIG = {
#         "host": ("The hostname to mysql", "localhost"),
#         "port": ("The port number to mysql", 3306),
#         "db": ("datbase name", "tpcc_py"),
#         # "user": ("user name", "root"),
#         # "passwd": ("password", "rootroot")
#         "user": ("user name", "jw2544"),
#         "passwd": ("password", "jw2544")
#     }
#
#     def __init__(self, ddl):
#         super(MysqlDriver, self).__init__("mysql", ddl)
#         logging.debug(ddl)
#
#     ## ----------------------------------------------
#     ## makeDefaultConfig
#     ## ----------------------------------------------
#     def makeDefaultConfig(self):
#         return MysqlDriver.DEFAULT_CONFIG
#
#     ## ----------------------------------------------
#     ## loadConfig
#     ## ----------------------------------------------
#     def loadConfig(self, config):
#         for key in MysqlDriver.DEFAULT_CONFIG.keys():
#             assert key in config, "Missing parameter '%s' in %s configuration" % (key, self.name)
#
#         self.conn = MySQLdb.connect(config['host'], config['user'], config['passwd'], config['db'])
#         self.cursor = self.conn.cursor()
#         if config["reset"]:
#             logging.debug("Deleting database '%s'" % config['db'])
#             self.cursor.execute("Drop database %s" % config['db'])
#
#     ## ----------------------------------------------
#     ## loadTuples
#     ## ----------------------------------------------
#     def loadTuples(self, tableName, tuples):
#         if len(tuples) == 0: return
#
#         p = ["%s"] * len(tuples[0])
#         sql = "INSERT INTO %s VALUES (%s)" % (tableName, ",".join(p))
#         logging.debug("sql:" + sql)
#         self.cursor.executemany(sql, tuples)
#         logging.debug("Loaded %d tuples for tableName %s" % (len(tuples), tableName))
#         self.conn.commit()
#         return
#
#     # def loadFinish(self):
#     #     sql = "ALTER TABLE ORDER_LINE ADD CONSTRAINT OL_FKEY_S FOREIGN KEY (OL_SUPPLY_W_ID, OL_I_ID) REFERENCES STOCK (S_W_ID, S_I_ID)"
#     #     self.cursor.execute(sql)
#     #     self.conn.commit()
#     #     return
#
#     def copyTable(self):
#         table_copy = 8
#         for i in range(table_copy):
#             self.cursor.execute("DROP TABLE IF EXISTS HISTORY%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS NEW_ORDER%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS ORDER_LINE%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS OORDER%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS CUSTOMER%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS DISTRICT%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS STOCK%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS ITEM%d" % i)
#             self.cursor.execute("DROP TABLE IF EXISTS WAREHOUSE%d" % i)
#             self.cursor.execute("CREATE TABLE CUSTOMER%d LIKE CUSTOMER" % i)
#             self.cursor.execute("CREATE TABLE DISTRICT%d LIKE DISTRICT" % i)
#             self.cursor.execute("CREATE TABLE HISTORY%d LIKE HISTORY" % i)
#             self.cursor.execute("CREATE TABLE ITEM%d LIKE ITEM" % i)
#             self.cursor.execute("CREATE TABLE NEW_ORDER%d LIKE NEW_ORDER" % i)
#             self.cursor.execute("CREATE TABLE OORDER%d LIKE OORDER" % i)
#             self.cursor.execute("CREATE TABLE ORDER_LINE%d LIKE ORDER_LINE" % i)
#             self.cursor.execute("CREATE TABLE STOCK%d LIKE STOCK" % i)
#             self.cursor.execute("CREATE TABLE WAREHOUSE%d LIKE WAREHOUSE" % i)
#             self.cursor.execute("INSERT INTO CUSTOMER%d SELECT * FROM CUSTOMER" % i)
#             self.cursor.execute("INSERT INTO DISTRICT%d SELECT * FROM DISTRICT" % i)
#             self.cursor.execute("INSERT INTO HISTORY%d SELECT * FROM HISTORY" % i)
#             self.cursor.execute("INSERT INTO ITEM%d SELECT * FROM ITEM" % i)
#             self.cursor.execute("INSERT INTO NEW_ORDER%d SELECT * FROM NEW_ORDER" % i)
#             self.cursor.execute("INSERT INTO OORDER%d SELECT * FROM OORDER" % i)
#             self.cursor.execute("INSERT INTO ORDER_LINE%d SELECT * FROM ORDER_LINE" % i)
#             self.cursor.execute("INSERT INTO STOCK%d SELECT * FROM STOCK" % i)
#             self.cursor.execute("INSERT INTO WAREHOUSE%d SELECT * FROM WAREHOUSE" % i)
#             self.cursor.execute(
#                 "ALTER TABLE DISTRICT%d ADD CONSTRAINT FKEY_DISTRICT_1%d FOREIGN KEY(D_W_ID) REFERENCES WAREHOUSE%d(W_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE CUSTOMER%d ADD CONSTRAINT FKEY_CUSTOMER_1%d FOREIGN KEY(C_W_ID,C_D_ID) REFERENCES DISTRICT%d(D_W_ID,D_ID)  ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE HISTORY%d ADD CONSTRAINT FKEY_HISTORY_1%d FOREIGN KEY(H_C_W_ID,H_C_D_ID,H_C_ID) REFERENCES CUSTOMER%d(C_W_ID,C_D_ID,C_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE HISTORY%d ADD CONSTRAINT FKEY_HISTORY_2%d FOREIGN KEY(H_W_ID,H_D_ID) REFERENCES DISTRICT%d(D_W_ID,D_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE NEW_ORDER%d ADD CONSTRAINT FKEY_NEW_ORDER_1%d FOREIGN KEY(NO_W_ID,NO_D_ID,NO_O_ID) REFERENCES OORDER%d(O_W_ID,O_D_ID,O_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE OORDER%d ADD CONSTRAINT FKEY_ORDER_1%d FOREIGN KEY(O_W_ID,O_D_ID,O_C_ID) REFERENCES CUSTOMER%d(C_W_ID,C_D_ID,C_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE ORDER_LINE%d ADD CONSTRAINT FKEY_ORDER_LINE_1%d FOREIGN KEY(OL_W_ID,OL_D_ID,OL_O_ID) REFERENCES OORDER%d(O_W_ID,O_D_ID,O_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE ORDER_LINE%d ADD CONSTRAINT FKEY_ORDER_LINE_2%d FOREIGN KEY(OL_SUPPLY_W_ID,OL_I_ID) REFERENCES STOCK%d(S_W_ID,S_I_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE STOCK%d ADD CONSTRAINT FKEY_STOCK_1%d FOREIGN KEY(S_W_ID) REFERENCES WAREHOUSE%d(W_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#             self.cursor.execute(
#                 "ALTER TABLE STOCK%d ADD CONSTRAINT FKEY_STOCK_2%d FOREIGN KEY(S_I_ID) REFERENCES ITEM%d(I_ID) ON DELETE CASCADE" % (
#                 i, i, i))
#
#     # ## ==============================================
#     # ## loadStart
#     # ## ==============================================
#     # def loadStart(self):
#
#     ## ----------------------------------------------
#     ## doDelivery
#     ## ----------------------------------------------
#     def doDelivery(self, params):
#         q = TXN_QUERIES["DELIVERY"]
#
#         w_id = params["w_id"]
#         o_carrier_id = params["o_carrier_id"]
#         ol_delivery_d = params["ol_delivery_d"]
#
#         # invoke order of that transaction
#         invoke_order = params["order"]["delivery_order"]
#         result = []
#         # whether need to initialize variable
#         for d_id in range(1, constants.DISTRICTS_PER_WAREHOUSE + 1):
#             for order in invoke_order:
#                 if order == 0:
#                     self.cursor.execute(q["getNewOrder"], [d_id, w_id])
#                     newOrder = self.cursor.fetchone()
#                     if newOrder == None:
#                         ## No orders for this district: skip it. Note: This must be reported if > 1%
#                         break
#                     assert len(newOrder) > 0
#                     no_o_id = newOrder[0]
#                 elif order == 1:
#                     self.cursor.execute(q["deleteNewOrder"], [d_id, w_id, no_o_id])
#                 elif order == 2:
#                     self.cursor.execute(q["getCId"], [no_o_id, d_id, w_id])
#                     c_id = self.cursor.fetchone()[0]
#                 elif order == 3:
#                     self.cursor.execute(q["updateOrders"], [o_carrier_id, no_o_id, d_id, w_id])
#                 elif order == 4:
#                     self.cursor.execute(q["updateOrderLine"], [ol_delivery_d, no_o_id, d_id, w_id])
#                 elif order == 5:
#                     self.cursor.execute(q["sumOLAmount"], [no_o_id, d_id, w_id])
#                     ol_total = self.cursor.fetchone()[0]
#                 elif order == 6:
#                     # These must be logged in the "result file" according to TPC-C 2.7.2.2 (page 39)
#                     # We remove the queued time, completed time, w_id, and o_carrier_id: the client can figure
#                     # them out
#                     # If there are no order lines, SUM returns null. There should always be order lines.
#                     assert ol_total != None, "ol_total is NULL: there are no order lines. This should not happen"
#                     assert ol_total > 0.0
#                     self.cursor.execute(q["updateCustomer"], [ol_total, c_id, d_id, w_id])
#             result.append((d_id, no_o_id))
#         ## FOR
#         self.conn.commit()
#         return result
#
#     ## ----------------------------------------------
#     ## doNewOrder
#     ## ----------------------------------------------
#     def doNewOrder(self, params):
#         try:
#             q = TXN_QUERIES["NEW_ORDER"]
#
#             w_id = params["w_id"]
#             d_id = params["d_id"]
#             c_id = params["c_id"]
#             o_entry_d = params["o_entry_d"]
#             i_ids = params["i_ids"]
#             i_w_ids = params["i_w_ids"]
#             i_qtys = params["i_qtys"]
#
#             assert len(i_ids) > 0
#             assert len(i_ids) == len(i_w_ids)
#             assert len(i_ids) == len(i_qtys)
#
#             invoke_order = params["order"]["new_order_order"]
#             all_local = True
#             items = []
#             for i in range(len(i_ids)):
#                 ## Determine if this is an all local order or not
#                 all_local = all_local and i_w_ids[i] == w_id
#                 self.cursor.execute(q["getItemInfo"], [i_ids[i]])
#                 items.append(self.cursor.fetchone())
#             assert len(items) == len(i_ids)
#
#             ## TPCC defines 1% of neworder gives a wrong itemid, causing rollback.
#             ## Note that this will happen with 1% of transactions on purpose.
#             for item in items:
#                 if len(item) == 0:
#                     ## TODO Abort here!
#                     return
#             ## FOR
#
#             ## ----------------
#             ## Insert Order Information
#             ## ----------------
#             ol_cnt = len(i_ids)
#             o_carrier_id = constants.NULL_CARRIER_ID
#
#             ## ----------------
#             ## Collect Information from WAREHOUSE, DISTRICT, and CUSTOMER
#             ## ----------------
#             for order in invoke_order:
#                 if order == 0:
#                     self.cursor.execute(q["getCustomer"], [w_id, d_id, c_id])
#                     customer_info = self.cursor.fetchone()
#                     c_discount = customer_info[0]
#                 elif order == 1:
#                     self.cursor.execute(q["getWarehouseTaxRate"], [w_id])
#                     w_tax = self.cursor.fetchone()[0]
#                 elif order == 2:
#                     self.cursor.execute(q["getDistrict"], [d_id, w_id])
#                     district_info = self.cursor.fetchone()
#                     d_tax = district_info[0]
#                     d_next_o_id = district_info[1]
#                     self.cursor.execute(q["incrementNextOrderId"], [d_next_o_id + 1, d_id, w_id])
#                 elif order == 3:
#                     self.cursor.execute(q["createOrder"],
#                                         [d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, ol_cnt, all_local])
#                 elif order == 4:
#                     self.cursor.execute(q["createNewOrder"], [d_next_o_id, d_id, w_id])
#
#             ## ----------------
#             ## Insert Order Item Information
#             ## ----------------
#             item_data = []
#             total = 0
#             for i in range(len(i_ids)):
#                 ol_number = i + 1
#                 ol_supply_w_id = i_w_ids[i]
#                 ol_i_id = i_ids[i]
#                 ol_quantity = i_qtys[i]
#
#                 itemInfo = items[i]
#                 i_name = itemInfo[1]
#                 i_data = itemInfo[2]
#                 i_price = itemInfo[0]
#
#                 self.cursor.execute(q["getStockInfo"] % (d_id, ol_i_id, ol_supply_w_id))
#                 stockInfo = self.cursor.fetchone()
#                 if len(stockInfo) == 0:
#                     logging.warn("No STOCK record for (ol_i_id=%d, ol_supply_w_id=%d)" % (ol_i_id, ol_supply_w_id))
#                     continue
#                 s_quantity = stockInfo[0]
#                 s_ytd = stockInfo[2]
#                 s_order_cnt = stockInfo[3]
#                 s_remote_cnt = stockInfo[4]
#                 s_data = stockInfo[1]
#                 s_dist_xx = stockInfo[5]  # Fetches data from the s_dist_[d_id] column
#
#                 ## Update stock
#                 s_ytd += ol_quantity
#                 if s_quantity >= ol_quantity + 10:
#                     s_quantity = s_quantity - ol_quantity
#                 else:
#                     s_quantity = s_quantity + 91 - ol_quantity
#                 s_order_cnt += 1
#
#                 if ol_supply_w_id != w_id: s_remote_cnt += 1
#
#                 self.cursor.execute(q["updateStock"],
#                                     [s_quantity, s_ytd, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id])
#
#                 if i_data.find(constants.ORIGINAL_STRING) != -1 and s_data.find(constants.ORIGINAL_STRING) != -1:
#                     brand_generic = 'B'
#                 else:
#                     brand_generic = 'G'
#
#                 ## Transaction profile states to use "ol_quantity * i_price"
#                 ol_amount = ol_quantity * i_price
#                 total += ol_amount
#
#                 self.cursor.execute(q["createOrderLine"],
#                                     [d_next_o_id, d_id, w_id, ol_number, ol_i_id, ol_supply_w_id, o_entry_d, ol_quantity,
#                                      ol_amount, s_dist_xx])
#
#                 ## Add the info to be returned
#                 item_data.append((i_name, s_quantity, brand_generic, i_price, ol_amount))
#             ## FOR
#
#             ## Commit!
#             self.conn.commit()
#
#             ## Adjust the total for the discount
#             # print "c_discount:", c_discount, type(c_discount)
#             # print "w_tax:", w_tax, type(w_tax)
#             # print "d_tax:", d_tax, type(d_tax)
#             total *= (1 - c_discount) * (1 + w_tax + d_tax)
#
#             ## Pack up values the client is missing (see TPC-C 2.4.3.5)
#             misc = [(w_tax, d_tax, d_next_o_id, total)]
#             return [customer_info, misc, item_data]
#
#         except MySQLdb.OperationalError:
#             self.conn.rollback()
#
#     ## ----------------------------------------------
#     ## doOrderStatus
#     ## ----------------------------------------------
#     def doOrderStatus(self, params):
#         try:
#             q = TXN_QUERIES["ORDER_STATUS"]
#
#             w_id = params["w_id"]
#             d_id = params["d_id"]
#             c_id = params["c_id"]
#             c_last = params["c_last"]
#
#             assert w_id, pformat(params)
#             assert d_id, pformat(params)
#
#             if c_id != None:
#                 self.cursor.execute(q["getCustomerByCustomerId"], [w_id, d_id, c_id])
#                 customer = self.cursor.fetchone()
#             else:
#                 # Get the midpoint customer's id
#                 self.cursor.execute(q["getCustomersByLastName"], [w_id, d_id, c_last])
#                 all_customers = self.cursor.fetchall()
#                 assert len(all_customers) > 0
#                 namecnt = len(all_customers)
#                 index = (namecnt - 1) / 2
#                 customer = all_customers[index]
#                 c_id = customer[0]
#             assert len(customer) > 0
#             assert c_id != None
#
#             self.cursor.execute(q["getLastOrder"], [w_id, d_id, c_id])
#             order = self.cursor.fetchone()
#             if order:
#                 self.cursor.execute(q["getOrderLines"], [w_id, d_id, order[0]])
#                 orderLines = self.cursor.fetchall()
#             else:
#                 orderLines = []
#
#             self.conn.commit()
#         except MySQLdb.OperationalError:
#             self.conn.rollback()
#         return [customer, order, orderLines]
#
#     ## ----------------------------------------------
#     ## doPayment
#     ## ----------------------------------------------
#     def doPayment(self, params):
#         try:
#             q = TXN_QUERIES["PAYMENT"]
#
#             w_id = params["w_id"]
#             d_id = params["d_id"]
#             h_amount = params["h_amount"]
#             c_w_id = params["c_w_id"]
#             c_d_id = params["c_d_id"]
#             c_id = params["c_id"]
#             c_last = params["c_last"]
#             h_date = params["h_date"]
#
#             invoke_order = params["order"]["payment_order"]
#
#             for query_num in invoke_order:
#                 if query_num == 0:
#                     self.cursor.execute(q["getWarehouse"], [w_id])
#                     warehouse = self.cursor.fetchone()
#                 elif query_num == 1:
#                     self.cursor.execute(q["updateWarehouseBalance"], [h_amount, w_id])
#                 elif query_num == 2:
#                     self.cursor.execute(q["getDistrict"], [w_id, d_id])
#                     district = self.cursor.fetchone()
#                 elif query_num == 3:
#                     self.cursor.execute(q["updateDistrictBalance"], [h_amount, w_id, d_id])
#                 elif query_num == 4:
#                     if c_id != None:
#                         self.cursor.execute(q["getCustomerByCustomerId"], [w_id, d_id, c_id])
#                         customer = self.cursor.fetchone()
#                     else:
#                         # Get the midpoint customer's id
#                         self.cursor.execute(q["getCustomersByLastName"], [w_id, d_id, c_last])
#                         all_customers = self.cursor.fetchall()
#                         assert len(all_customers) > 0
#                         namecnt = len(all_customers)
#                         index = (namecnt - 1) / 2
#                         customer = all_customers[index]
#                         c_id = customer[0]
#                     assert len(customer) > 0
#                     c_balance = customer[14] - h_amount
#                     c_ytd_payment = customer[15] + h_amount
#                     c_payment_cnt = customer[16] + 1
#                     c_data = customer[17]
#                 elif query_num == 5:
#                     # Customer Credit Information
#                     if customer[11] == constants.BAD_CREDIT:
#                         newData = " ".join(map(str, [c_id, c_d_id, c_w_id, d_id, w_id, h_amount]))
#                         c_data = (newData + "|" + c_data)
#                         if len(c_data) > constants.MAX_C_DATA: c_data = c_data[:constants.MAX_C_DATA]
#                         self.cursor.execute(q["updateBCCustomer"],
#                                             [c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id])
#                     else:
#                         c_data = ""
#                         self.cursor.execute(q["updateGCCustomer"],
#                                             [c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id])
#                 elif query_num == 6:
#                     # Concatenate w_name, four spaces, d_name
#                     h_data = "%s    %s" % (warehouse[0], district[0])
#                     # Create the history record
#                     self.cursor.execute(q["insertHistory"], [c_id, c_d_id, c_w_id, d_id, w_id, h_date, h_amount, h_data])
#
#             self.conn.commit()
#
#         except MySQLdb.OperationalError:
#             self.conn.rollback()
#
#         # TPC-C 2.5.3.3: Must display the following fields:
#         # W_ID, D_ID, C_ID, C_D_ID, C_W_ID, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP,
#         # D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1,
#         # C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM,
#         # C_DISCOUNT, C_BALANCE, the first 200 characters of C_DATA (only if C_CREDIT = "BC"),
#         # H_AMOUNT, and H_DATE.
#
#         # Hand back all the warehouse, district, and customer data
#         return [warehouse, district, customer]
#
#     ## ----------------------------------------------
#     ## doStockLevel
#     ## ----------------------------------------------
#     def doStockLevel(self, params):
#         q = TXN_QUERIES["STOCK_LEVEL"]
#
#         w_id = params["w_id"]
#         d_id = params["d_id"]
#         threshold = params["threshold"]
#
#         self.cursor.execute(q["getOId"], [w_id, d_id])
#         result = self.cursor.fetchone()
#         assert result
#         o_id = result[0]
#
#         self.cursor.execute(q["getStockCount"], [w_id, d_id, o_id, (o_id - 20), w_id, threshold])
#         result = self.cursor.fetchone()
#
#         self.conn.commit()
#
#         return int(result[0])
#
#     def buildIndex(self, index_creation_sql):
#         """build index"""
#         logging.debug("create index %s" % index_creation_sql)
#         self.cursor.execute(index_creation_sql)
#
#     def dropIndex(self, index_drop_sql):
#         """drop index"""
#         logging.debug("drop index %s" % index_drop_sql)
#         self.cursor.execute(index_drop_sql)
#
#     def setSystemParameter(self, parameter_sql):
#         """parameter change"""
#         logging.debug("change system parameter %s" % parameter_sql)
#         self.cursor.execute(parameter_sql)
#
# ## CLASS