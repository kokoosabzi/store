import os
os.environ['LCC_DATABASE_URL']='sqlite:///./test_local_commerce.db'
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import Base,engine
client=TestClient(app)
def setup_function(): Base.metadata.drop_all(engine);Base.metadata.create_all(engine)
def test_health_and_sale_keeps_historical_cost():
    assert client.get('/api/health').json()['database']=='ok'
    account=client.post('/api/accounts',params={'name':'صندوق'}).json()
    supplier=client.post('/api/suppliers',json={'name':'تأمین‌کننده'}).json()
    product=client.post('/api/products',json={'name':'کالا','current_purchase_price':'100','retail_price':'150'}).json()
    purchase=client.post('/api/purchases/draft',json={'supplier_id':supplier['id'],'items':[{'product_id':product['id'],'quantity':'5','unit_price':'100'}]}).json()
    assert client.post(f"/api/purchases/{purchase['id']}/finalize",params={'account_id':account['id']}).status_code==200
    sale=client.post('/api/sales/draft',json={'items':[{'product_id':product['id'],'quantity':'2','unit_price':'150'}],'paid_amount':'300'}).json()
    assert client.post(f"/api/sales/{sale['id']}/finalize",params={'account_id':account['id']}).status_code==200
    assert client.get('/api/inventory').json()[0]['current_stock']=='3.000'
    report=client.get('/api/reports/profit-loss').json(); assert report['revenue']=='300.00' and report['cogs']=='200.00000'
def test_sale_rollback_when_stock_insufficient():
    product=client.post('/api/products',json={'name':'بدون موجودی'}).json()
    sale=client.post('/api/sales/draft',json={'items':[{'product_id':product['id'],'quantity':'1','unit_price':'1'}]}).json()
    response=client.post(f"/api/sales/{sale['id']}/finalize")
    assert response.status_code==422
    assert client.get('/api/inventory').json()[0]['current_stock']=='0.000'
def test_sellable_return_reverses_revenue_and_cogs():
    account=client.post('/api/accounts',params={'name':'صندوق'}).json()
    supplier=client.post('/api/suppliers',json={'name':'تامین'}).json()
    product=client.post('/api/products',json={'name':'قابل مرجوعی'}).json()
    purchase=client.post('/api/purchases/draft',json={'supplier_id':supplier['id'],'items':[{'product_id':product['id'],'quantity':'2','unit_price':'100'}]}).json()
    client.post(f"/api/purchases/{purchase['id']}/finalize",params={'account_id':account['id']})
    sale=client.post('/api/sales/draft',json={'items':[{'product_id':product['id'],'quantity':'1','unit_price':'150'}],'paid_amount':'150'}).json()
    client.post(f"/api/sales/{sale['id']}/finalize",params={'account_id':account['id']})
    sale_item_id=1
    returned=client.post(f"/api/sales/{sale['id']}/returns",json={'items':[{'sale_item_id':sale_item_id,'quantity':'1','condition':'sellable'}],'refund_amount':'150','refund_account_id':account['id']})
    assert returned.status_code==201
    assert client.get('/api/inventory').json()[0]['current_stock']=='2.000'
    report=client.get('/api/reports/profit-loss').json(); assert report['revenue']=='0.00' and report['cogs']=='0.00000'

def test_return_cannot_exceed_the_original_quantity():
    account=client.post('/api/accounts',params={'name':'صندوق'}).json()
    supplier=client.post('/api/suppliers',json={'name':'تامین'}).json()
    product=client.post('/api/products',json={'name':'کالای محدود'}).json()
    purchase=client.post('/api/purchases/draft',json={'supplier_id':supplier['id'],'items':[{'product_id':product['id'],'quantity':'1','unit_price':'10'}]}).json()
    client.post(f"/api/purchases/{purchase['id']}/finalize",params={'account_id':account['id']})
    sale=client.post('/api/sales/draft',json={'items':[{'product_id':product['id'],'quantity':'1','unit_price':'20'}],'paid_amount':'20'}).json()
    client.post(f"/api/sales/{sale['id']}/finalize",params={'account_id':account['id']})
    response=client.post(f"/api/sales/{sale['id']}/returns",json={'items':[{'sale_item_id':1,'quantity':'2'}]})
    assert response.status_code==422

def test_custom_attributes_and_low_stock_are_generic():
    product=client.post('/api/products',json={'name':'محصول عمومی','min_stock':'2'}).json()
    attribute=client.post('/api/attributes',json={'name':'رنگ','data_type':'select','is_filterable':True}).json()
    value=client.put(f"/api/products/{product['id']}/attributes",json={'attribute_definition_id':attribute['id'],'value':'آبی'})
    assert value.status_code==200
    assert client.get(f"/api/products/{product['id']}/attributes").json()[0]['value']=='آبی'
    assert client.get('/api/inventory/low-stock').json()[0]['id']==product['id']

def test_dashboard_reconciles_profit_and_balances():
    account=client.post('/api/accounts',params={'name':'صندوق'}).json()
    supplier=client.post('/api/suppliers',json={'name':'تامین‌کننده'}).json()
    customer=client.post('/api/customers',json={'name':'مشتری','credit_limit':'100'}).json()
    product=client.post('/api/products',json={'name':'محصول داشبورد','min_stock':'2'}).json()
    purchase=client.post('/api/purchases/draft',json={'supplier_id':supplier['id'],'items':[{'product_id':product['id'],'quantity':'2','unit_price':'10'}]}).json()
    client.post(f"/api/purchases/{purchase['id']}/finalize",params={'account_id':account['id']})
    sale=client.post('/api/sales/draft',json={'customer_id':customer['id'],'items':[{'product_id':product['id'],'quantity':'1','unit_price':'25'}],'paid_amount':'10'}).json()
    assert client.post(f"/api/sales/{sale['id']}/finalize",params={'account_id':account['id']}).status_code==200
    dashboard=client.get('/api/dashboard').json()
    assert dashboard['revenue']=='25.00' and dashboard['cogs']=='10.00000'
    assert dashboard['net_profit']=='15.00000' and dashboard['receivables']=='15.00'
    assert dashboard['low_stock_count']==1

def test_product_csv_import_and_export_handles_duplicates():
    csv_data='code,name,retail_price,min_stock\nSKU-1,کالای وارداتی,120,3\nSKU-1,تکراری,130,0\n'
    response=client.post('/api/import/products',files={'file':('products.csv',csv_data.encode('utf-8'),'text/csv')})
    assert response.status_code==200
    assert response.json()['created']==1 and response.json()['skipped_duplicates']==1
    exported=client.get('/api/export/products.csv')
    assert exported.status_code==200 and 'SKU-1' in exported.text

def test_manager_pin_setup_and_change_requires_current_pin():
    assert client.get('/api/security/status').json()['pin_configured'] is False
    assert client.post('/api/security/setup-pin',json={'pin':'1234'}).status_code==201
    assert client.post('/api/security/change-pin',json={'current_pin':'0000','pin':'5678'}).status_code==403
    assert client.post('/api/security/change-pin',json={'current_pin':'1234','pin':'5678'}).json()['changed'] is True

def test_low_stock_notification_is_exposed():
    client.post('/api/products',json={'name':'کالای هشدار','min_stock':'1'})
    notifications=client.get('/api/notifications').json()
    assert notifications[0]['notification_type']=='low_stock'
    assert 'کالای هشدار' in notifications[0]['message']
