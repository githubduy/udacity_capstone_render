import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, db_drop_and_create_all

from config import SQLALCHEMY_DATABASE_URI
from exam_main import create_app


def get_token_authen(email,passw):

    url = 'https://dev-ookv36rq07kmjg5a.us.auth0.com/oauth/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
            'grant_type':'password',
            'username':email,
            'password':passw,
            'client_id':'rhfuwLV0Py3R7lBMglMlaEkwbcQl1cTk',
            'audience':'http://127.0.0.1:5000/',
            'client_secret':'oERiiy3zzs6jyR2C0TqPyEUSe6tkc3PtXBLTrLW7ILfu3Z2nAIu3VEV>
    }
    print(data)

    respond = requests.post(url, headers=header,data=data)
    json_data=json.loads(respond.text)


    token = {
        'Authorization': f'Bearer {json_data["access_token"]}'
    }
    return token

token_barista = get_token_authen('barista_user@gmail.com','123123Jhg@')
token_manager =  get_token_authen('man_user@gmail.com','123123qqq@')
expried_token = {
    'Authorization': 'Bearer eyihbxciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOduyvVnn0MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5NjgzODc2NCwiZXhwIjoxNjk2ODQ1OTY0LCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.Nkm0-htqUxFozmhGpHYGDvfLIslrPFLb06h3WUx_v2H1dmwbyQVfDpileF0VtTWTYG4_Ygmwq3axFkFCkS1zG-Dq7O9ajLfz41ZDhnb9wb_hQx0IVCZVl8JfaPSylVRnGPMWzkOw5zRNM7_MUt5oHcKQxQa21w73Pew7HQbZzQrYPhvjHv4RIUo4MxE6IWMlzKLMBjiV74qYY0PTa7SfN4CaCFnBWe1-DovlB_CMl36DChGXlUj30rQwtwtG_kesZUOL3mS_e28D9unNeylWbKNr5MvVAOVs9_CnWiXvhpKKx4gKhr_OZUOvW8uYv-KPzRAMMzTRBPeCek-C1gf3wg'
}

if SQLALCHEMY_DATABASE_URI == "":
    print("Please set SQLALCHEMY_DATABASE_URI Env, read on file run.sh")
    exit()

class DrinkStoreTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test=True)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.database_path = SQLALCHEMY_DATABASE_URI
        setup_db(app=self.app, database_path=self.database_path)
        with self.app.app_context():
            db_drop_and_create_all()
        

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_rootpath(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_drinks_barista(self):
        response = self.client.get('/drinks', headers=token_barista)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_manager(self):
        response = self.client.get('/drinks', headers=token_manager)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_fake(self):
        response = self.client.get('/drinks', headers=expried_token)
        self.assertEqual(response.status_code, 401)

    def test_get_drink_items(self):
        response = self.client.get('/drinks/1', headers=token_barista)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_fail(self):
        response = self.client.get('/drinks', headers={})
        self.assertEqual(response.status_code, 401)

    def test_get_drinks_detail_barista(self):
        response = self.client.get(
            '/drinks-detail',
            headers=token_barista)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_detail_manager(self):
        response = self.client.get(
            '/drinks-detail',
            headers=token_manager)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_detail_fake(self):
        response = self.client.get('/drinks-detail', headers=expried_token)
        self.assertEqual(response.status_code, 401)

    def test_get_drinks_detail_fail(self):
        response = self.client.get('/drinks-detail', headers={})
        self.assertEqual(response.status_code, 401)

    def test_post_drinks_manager(self):
        response = self.client.post(
            '/drinks',
            headers=token_manager,
            json={
                'title': 'Coffee',
                'recipe': '[{"name": "Coffee", "color": "black", "parts": 1}]'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_drinks_barista(self):
        response = self.client.post(
            '/drinks',
            headers=token_barista,
            json={
                'title': 'water',
                'recipe': '[{"name": "water melon", "color": "blue", "parts": 1}'})
        self.assertEqual(response.status_code, 403)

    def test_post_drinks_fake(self):
        response = self.client.post('/drinks', headers=expried_token, json={
            'title': 'water',
            'recipe': '[{"name": "water melon", "color": "blue", "parts": 1}'
        })
        self.assertEqual(response.status_code, 401)

    def test_post_drinks_fail(self):
        response = self.client.post('/drinks', headers={}, json={
            'title': 'water',
            'recipe': '[{"name": "water melon", "color": "blue", "parts": 1}'
        })
        self.assertEqual(response.status_code, 401)

    def test_patch_drinks_manager(self):
        response = self.client.patch(
            '/drinks/1',
            headers=token_manager,
            json={
                'title': 'water',
                'recipe': '[{"name": "water melon", "color": "green", "parts": 1}]'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_drinks_barista(self):
        response = self.client.patch(
            '/drinks/1',
            headers=token_barista,
            json={
                'title': 'water',
                'recipe': '[{"name": "water melon", "color": "green", "parts": 1}]'})
        self.assertEqual(response.status_code, 403)

    def test_patch_drinks_fail(self):
        response = self.client.patch('/drinks/1', headers={}, json={
            'title': 'water',
            'recipe': '[{"name": "water melon", "color": "green", "parts": 1}]'
        })
        self.assertEqual(response.status_code, 401)

    def test_delete_drinks_manager(self):
        response = self.client.delete('/drinks/1', headers=token_manager)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_drinks_barista(self):
        response = self.client.delete('/drinks/1', headers=token_barista)
        self.assertEqual(response.status_code, 403)

    def test_delete_drinks_fail(self):
        response = self.client.delete('/drinks/1', headers={})
        self.assertEqual(response.status_code, 401)

    def test_get_ingredients_barista(self):
        response = self.client.get('/metals', headers=token_barista)
        self.assertEqual(response.status_code, 200)

    def test_get_ingredients_manager(self):
        response = self.client.get('/metals', headers=token_manager)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_metals_fail(self):
        response = self.client.get('/metals', headers={})
        self.assertEqual(response.status_code, 401)

    def test_post_ingredients_manager(self):
        response = self.client.post(
            '/metals',
            headers=token_manager,
            json={
                'name': 'Matcha',
                'density': '90%'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_ingredients_barista(self):
        response = self.client.post(
            '/metals',
            headers=token_barista,
            json={
                'name': 'Matcha',
                'density': '90%'})
        self.assertEqual(response.status_code, 403)

    def test_post_metals_fail(self):
        response = self.client.post('/metals', headers={}, json={
            'name': 'Matcha',
            'density': '90%'
        })
        self.assertEqual(response.status_code, 401)

    def test_patch_ingredients_manager(self):
        response = self.client.patch(
            '/metals/1',
            headers=token_manager,
            json={
                'name': 'water',
                'density': '80%'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_ingredients_barista(self):
        response = self.client.patch(
            '/metals/1',
            headers=token_barista,
            json={
                'name': 'water',
                'density': '80%'})
        self.assertEqual(response.status_code, 403)

    def test_patch_metals_fail(self):
        response = self.client.patch('/metals/1', headers={}, json={
            'name': 'water',
            'density': '80%'
        })
        self.assertEqual(response.status_code, 401)

    def test_delete_ingredients_manager(self):
        response = self.client.delete(
            '/metals/1', headers=token_manager)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_ingredients_barista(self):
        response = self.client.delete(
            '/metals/1', headers=token_barista)
        self.assertEqual(response.status_code, 403)

    def test_delete_metals_fail(self):
        response = self.client.delete('/metals/1', headers={})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
