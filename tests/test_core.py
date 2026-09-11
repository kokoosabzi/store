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
