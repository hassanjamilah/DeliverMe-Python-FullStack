import os 
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import  app
from models import setup_db , materials , orders, orders_details


class DeliverMeTestCase(unittest.TestCase):
    
    secretary_key = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxBTVdfVmxZRmRMeXlVS0xubkdrZiJ9.eyJpc3MiOiJodHRwczovL2FuZGFsdXNzb2Z0LmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjA2OTc5ODExNDQ0MTA0ODUzNCIsImF1ZCI6ImRlbGl2ZXJfbWVfYXBpIiwiaWF0IjoxNTg4Mzc2ODMyLCJleHAiOjE1ODg0NjMyMzIsImF6cCI6IkRDN3R0cW55Q2dpdXJpeXIzSkdyRU5PdTlOQ25SRnpwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6b3JkZXJzIiwicmVhZDptYXRlcmlhbHMiLCJyZWFkOm9yZGVycyJdfQ.KKmRKfOAzIN-S-is0Ihz98pP2sRxpuWoHvZ5SURYA_0TfK2rpjGEtpf-FOfRxsnOSEwFF_yjLuoulGuGAMd2alsdVV98DpQsLt8HCjy_TzHAjqDpoBKvQLIYMP_j5NDie1wsLGkjc31qmtb5_VAcTRyqyTZ7zdb85CucI10Hv6mlIbxQGlAQ_ceABPf9UA6boG_TCfkc0hY_SKv_kfNdl-lz9cyQPeOKIVe9dfxcehKS6MKAzeGRnCBJEGLF07cUJP2ldRYPMmhjxuI1PwCmTCAqmY4u_QaRy_mOk1HhSYULh9I8NSye6FTf1eQ2p0N89Td1YJgQNmXNF2GsCaxwTg'
    accountant_key = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxBTVdfVmxZRmRMeXlVS0xubkdrZiJ9.eyJpc3MiOiJodHRwczovL2FuZGFsdXNzb2Z0LmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjA2OTc5ODExNDQ0MTA0ODUzNCIsImF1ZCI6ImRlbGl2ZXJfbWVfYXBpIiwiaWF0IjoxNTg4Mzc2Nzc1LCJleHAiOjE1ODg0NjMxNzUsImF6cCI6IkRDN3R0cW55Q2dpdXJpeXIzSkdyRU5PdTlOQ25SRnpwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6bWF0ZXJpYWxzIiwiYWRkOm9yZGVycyIsInJlYWQ6bWF0ZXJpYWxzIiwicmVhZDpvcmRlcnMiLCJ1cGRhdGU6bWF0ZXJpYWxzIl19.jWlqjcyrH97NGW5u7eQbLROF-9nz4C5c-TXLaOoUMy1iVWdiSIgN29VTYhVM175jVV5MY8rldeK9TDk1-4q6n8Mb_G43gmkWimKsTRHxA2BL8jzazT6FyfRTZbZZpLmiga_f1MLCIhyIzCVg9ngeSO2Ipc0SeUKzudXdC2WPMj-X_svxae4_CNh_9zFaREN8NHYtsCcXoxgWxR4dqJUTFFTFjFJAA3O9BpQLi3m6vyVUOWVH5y0w689VyPTs6HrTH04_v50J5QSdCO-JEJ8jTE_Mbxu9B0nBZnrdlB7bPbMY3NkyPupQve_xOnaxOlEZ1Hy0EOfduGu5rDed2sr58w'
    manager_key = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxBTVdfVmxZRmRMeXlVS0xubkdrZiJ9.eyJpc3MiOiJodHRwczovL2FuZGFsdXNzb2Z0LmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjA2OTc5ODExNDQ0MTA0ODUzNCIsImF1ZCI6ImRlbGl2ZXJfbWVfYXBpIiwiaWF0IjoxNTg4Mzc2NjM0LCJleHAiOjE1ODg0NjMwMzQsImF6cCI6IkRDN3R0cW55Q2dpdXJpeXIzSkdyRU5PdTlOQ25SRnpwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6bWF0ZXJpYWxzIiwiYWRkOm9yZGVycyIsImRlbGV0ZTptYXRlcmlhbHMiLCJkZWxldGU6b3JkZXJzIiwicmVhZDptYXRlcmlhbHMiLCJyZWFkOm9yZGVycyIsInVwZGF0ZTptYXRlcmlhbHMiLCJ1cGRhdGU6b3JkZXJzIl19.uYE1XkJDcX4a-mKYDX_Q-btK8aGFeZPrgT45gQVoun_XDDQdBpHStSpW1LpWf1z9_yqd5mPdUb4SCExOQxT936kM1J111dr80YpCq5RlnQ6oYCpX8iiWNNfi-hWsTLeslZmGipGkgfQ9alKpEz10JimUheao5pV7iKAYH0E4qhuoM40x3vISFW3gDTdH7TB4ghWQVuA_hH4_5oy7i7RWhHNQsdndT0WD4DnEBGR2TvkasbDi2OKMxw66taQCk-zrtkLSjquaQBkjxSq6bGU02P15qTpa0UGeROVSZFu3nJLd1a3Ih9xgrU1lhN1fQ7_1RC9HEtrpME-T8Vbb-jkKEA'

    
    def setUp(self):
        print('🌯 🌯 🌯 🌯')
        self.app = app
        self.client = self.app.test_client
        self.test_database_name = "deliverme_test"
        self.test_database_path = "postgres://{}@{}/{}".format('postgres','localhost:5432', self.test_database_name)
        setup_db(self.app , self.test_database_path)
       
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app ( self.app )
            self.db.create_all()
    
    def tearDown(self):
        pass
    
    def test_get_all_materials(self):
        self.insert_material()
        res = self.client().get('/materials' , headers={'Authorization':self.secretary_key})
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(data["materials"])
        self.assertGreater(data["materials_count"] , 0)
        
    def test_seach_material(self):
        res = self.client().post('/materials' , json={"search":"a"},headers={'Authorization':self.accountant_key})
        data = json.loads(res.data)
        
        self.assertTrue(data["success"])
        self.assertTrue("materials")
        self.assertNotEqual("materials_count" , "0")
        
    def test_insert_material(self):
        res = self.client().post('/materials' , json={"material_name":"new material " ,
                                                      "material_description":"new material desc"}
                                 , headers={'Authorization':self.accountant_key}
                                 )
        data = json.loads(res.data)
        
        self.assertTrue(data["success"])
        self.assertTrue(["inserted_material_id"])
        
    def test_update_material(self):
        material = materials()
        material.mat_name = "test 15"
        material.mat_desc = "test desc 15"
        material.insert()
        res = self.client().patch('/materials/{}'.format(material.id),json={
                                                    	"material_name":"hot choccolate 44" , 
	                                                    "material_description":"del choccolate 44"
                                                            } , 
                                  headers={'Authorization':self.accountant_key}
                                  )
        data = json.loads(res.data) 
        material1 = data["updated_material"]
        
        self.assertTrue(data["success"])
        self.assertTrue(data["updated_material"])   
        self.assertEqual(material1["name"] , "hot choccolate 44")
        self.assertEqual(material1["description"] , "del choccolate 44")
        self.assertEqual(material1["id"] , material.id)

    def test_delete_materials(self):
        material = self.insert_material()
        res = self.client().delete('/materials/{}'.format(material.id),headers={'Authorization':self.manager_key})
        data = json.loads(res.data)
        
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted_material_id"],material.id)

    def test_insert_order(self):
        res = self.client().post('/orders' , json={
            	"order_notes":"note1342ddd" , 
                "details":[
                    {
                        "material_id":1 , 
                        "quantity":20 , 
                        "price":15 
                    } 
                    , 
                    {
                        "material_id":1 , 
                        "quantity":40 , 
                        "price":30 	
                    }
                    ]
        },
            headers={'Authorization':self.accountant_key})
        data = json.loads(res.data)
        
        self.assertTrue(data["success"])
        self.assertTrue(data["inserted_order"])

    def test_get_all_orders(self):
        res = self.client().get('/orders' , headers={'Authorization':self.secretary_key})
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(data["orders"])
    
    def test_get_order_details(self):
        res = self.client().get('/orders/10',headers={'Authorization':self.secretary_key})
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(data["order_details"])
    
    def test_delete_order(self):
        order_id = self.insert_order()
        res = self.client().delete('/orders/{}'.format(order_id),headers={'Authorization':self.manager_key})
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted_order_id"],order_id)
    
    
    def test_modify_order(self):
        order_id = self.insert_order()
        material = self.insert_material()
        res = self.client().patch('/orders/{}'.format(order_id)  , json={
                "order_notes":"note modified" , 
                "details":[
                    {
                        "material_id":material.id , 
                        "quantity":20 , 
                        "price":15 
                    } 
                    , 
                    {
                        "material_id":material.id , 
                        "quantity":40 , 
                        "price":30 	
                    }
                    ]
        },headers={'Authorization':self.manager_key})
        data = json.loads(res.data)
        self.assertTrue(data["success"])
    
    def insert_material(self):
        material = materials()
        material.mat_name = "test 15"
        material.mat_desc = "test desc 15"
        material.insert()
        return material
        
    def insert_order(self):
        material = materials()
        material.mat_name = "test 15"
        material.mat_desc = "test desc 15"
        material.insert()
        order =  orders()
        order.order_notes = "order note15"
        order.insert()
        details = orders_details()
        details.quantity = 10 
        details.price = 15 
        details.material_det = material
        details.order_det = order
        details.insert()
        return order.id
        

if __name__ == "__main__":
    unittest.main()