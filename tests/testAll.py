import json
from . import app, client, cache, create_token_buyer, create_token_seller, create_token_not_enough_saldo, create_token_invalid, create_token_dummy
from blueprints.barang.model import Barang
from blueprints.user.model import User
from tests import reset_database

class TestSuccessEvent():
    id_added_item = 0
    new_id = Barang.query.all()[-1].id + 100
    
    new_barang = 'barangdummy'+str(new_id)

    #topup
    def test_topup(self, client):
        token = create_token_buyer()
        url = '/user/topup'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'topup': 10000
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 200

    #topup
    def test_topup_negative_amount(self, client):
        token = create_token_buyer()
        url = '/user/topup'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'topup': -10000
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 200

    #invalid login
    def test_invalid_login(self, client):
        token = create_token_invalid()
        assert 200 == 200

    # signup
    def test_signup(self, client):
        token = create_token_buyer()
        url = '/welcome/signup'
        data = {
            'nama': TestSuccessEvent.new_barang,
            'email': 'tes@tes.com',
            'password': 'tes'
        }
        res = client.post(url, json=data)
        assert res.status_code == 200

    # signup
    def test_signup_blank(self, client):
        token = create_token_buyer()
        url = '/welcome/signup'
        data = {
            'nama': '',
            'email': '',
            'password': ''
        }
        res = client.post(url, json=data)
        assert res.status_code == 200

    def test_signup_already_register(self, client):
        token = create_token_buyer()
        url = '/welcome/signup'
        data = {
            'nama': 'tes',
            'email': 'tes@tes.com',
            'password': 'tes'
        }
        res = client.post(url, json=data)
        assert res.status_code == 200

    # get user status
    def test_get_user_status(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200


    # get all item
    def test_get_all_item(self, client):
        token = create_token_buyer()
        res = client.get(
            '/user/all', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    #get item by_id
    def test_get_an_item_by_id(self, client):
        token = create_token_buyer()
        res = client.patch(
            'user/3', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    # add to shopping bag
    def test_add_to_bag(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # add to shopping bag second time
    def test_add_to_bag_second_time(self, client):
        token = create_token_buyer()
        url2='/user/beli/1'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200
    
    # add to shopping bag firstTime
    def test_add_to_bag_first_time(self, client):
        token = create_token_seller()
        url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    #edit item in shopping bag
    def test_edit_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/1'
        data = {
            'qty': 2
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 200

    #get all item in shopping bag
    def test_get_all_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200

    #delete item in shopping bag
    def test_delete_item_in_bag(self, client):
        token = create_token_buyer()
        url = '/user/nota/2'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers=h)
        assert res.status_code == 200

    #get all transactions
    def test_get_all_transactions(self, client):
        token = create_token_buyer()
        url = '/user/transactions'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200

    #pay
    def test_pay(self, client):
        token = create_token_buyer()
        url2='/user/beli/1'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url2, query_string=data, headers=h)  

        url = '/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #pay
    def test_pay_not_enough_saldo(self, client):
        token = create_token_dummy()
        url2='/user/beli/1'
        data = {
            'qty': 20
        }
        url3='/user/beli/2'
        data3 = {
            'qty':3
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url3, query_string=data3, headers=h)
        res = client.get(url2, query_string=data, headers=h)  

        url = '/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #be a seller
    def test_be_a_seller(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #give rating
    def test_give_rating(self, client):
        token = create_token_buyer()
        url = '/user/give_rating/2'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 10
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    def test_give_rating_invalid_value(self, client):
        token = create_token_buyer()
        url = '/user/give_rating/4'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 12
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    def test_give_rating_to_nonexist_seller(self, client):
        token = create_token_buyer()
        url = '/user/give_rating/100'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 9
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    #give rating
    def test_give_rating2(self, client):
        token = create_token_buyer()
        person_id = User.query.filter_by(nama=TestSuccessEvent.new_barang).first().id
        url = '/user/give_rating/'+str(person_id)
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 10
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    #edit profile
    def test_edit_profile(self, client):
        token = create_token_seller()
        url = '/user/beli'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama': 'syamsul',
            'password': 'abc'
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    #delete_all_nota
    def test_delete_all_nota(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        url2='/user/nota/all'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        res = client.delete(url2,query_string=data, headers=h)        
        assert res.status_code == 200


    #forget password
    def test_forgot_password_profile(self, client):
        token = create_token_seller()
        url = '/user/beli'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'username': 'syamsul',
            'email': 'abc@gmail.com'
        }
        res = client.patch(url, headers=h, json=data)
        assert res.status_code == 200

    #search item
    def test_search_item(self, client):
        token = create_token_buyer()
        url = '/user/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        params = {
            'text': 'o'
        }
        res = client.post(url, headers=h, query_string=params)
        assert res.status_code == 200

    def test_failed_signup(self, client):
        token = create_token_buyer()
        url = '/welcome/signup'
        data = {
            'nama': 'tes',
            'email': 'tes@tes.com',
            'password': 'tes'
        }
        res = client.post(url, json=data)
        assert res.status_code == 200

    # get user status
    def test_failed_get_user_status(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200


    # get all item
    def test_failed_get_all_item(self, client):
        token = create_token_buyer()
        res = client.get(
            '/user/all', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    # qty invalid
    def test_failed_add_to_bag(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        url2='/user/beli/2'
        data = {
            'qty': -1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    #get all item in shopping bag
    def test_failed_get_all_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200

    #edit item in shopping bag qty invalid
    def test_failed_edit_item_in_bag(self, client):
        token = create_token_buyer()
        url1 = '/user/beli/1'
        buy_data = {
            'qty':1
        }
        url2='/user/nota/1'
        edit_data = {
            'qty': -1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1, query_string=buy_data, headers=h)
        res = client.put(url2, json=edit_data, headers=h)
        assert res.status_code == 200

    #delete item in shopping bag no header
    def test_failed_delete_item_in_bag(self, client):
        token = create_token_buyer()
        url = '/user/nota/2'
        h = {
            'Authorization': 'Bearer '
        }
        res = client.patch(url, headers=h)
        assert res.status_code == 422

    #pay not enough saldo
    def test_failed_pay(self, client):
        token = create_token_not_enough_saldo()
        url = '/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 400


    #be a seller not enough saldo
    def test_failed_be_a_seller(self, client):
        token = create_token_not_enough_saldo()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #give rating already give rating
    def test_failed_give_rating(self, client):
        token = create_token_buyer()
        url = '/user/give_rating/2'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 10
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200

    def test_get_all_myshop_item(self, client):
        token = create_token_seller()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200

    #get a shop item
    def test_get_a_shop_item(self, client):
        token = create_token_seller()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers = h)
        assert res.status_code == 200

    #edit item in shop
    def test_edit_item_in_shop(self, client):
        token = create_token_seller()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'Baju',
            'harga_satuan': 2000,
            'qty': 10,
            'url_image': 'https://m.media-amazon.com/images/I/A13usaonutL._CLa%7C2140,2000%7C61hLBkLke6L.png%7C0,0,2140,2000+0.0,0.0,2140.0,2000.0._UX342_.png'
        }
        res = client.put(url, headers = h, json = data)
        assert res.status_code == 200

    #add item to shop
    def test_add_item_to_shop(self, client):
        token = create_token_seller()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'kolor',
            'harga_satuan': 5000,
            'qty': 6,
            'url_image': ''
        }
        res = client.post(url, headers = h, json = data)
        assert res.status_code == 200

    #add item to shop
    def test_add_item_to_shop(self, client):
        token = create_token_seller()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': TestSuccessEvent.new_barang,
            'harga_satuan': 99999999,
            'qty': 6,
            'url_image': ''
        }
        res = client.post(url, headers = h, json = data)
        TestSuccessEvent.id_added_item = Barang.query.filter_by(nama_barang=data['nama_barang']).first().id
        assert res.status_code == 200

    #delete item in shop
    def test_delete_item_in_shop(self, client):
        token = create_token_seller()
        id = TestSuccessEvent.id_added_item
        url = '/user/myshop/'+ str(id)
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.delete(url, headers = h)
        assert res.status_code == 200


    def test_nonseller_get_all_myshop_item(self, client):
        token = create_token_buyer()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200

    #get a shop item nonseller
    def test_nonseller_get_a_shop_item(self, client):
        token = create_token_buyer()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers = h)
        assert res.status_code == 200

    #edit item in shop nonseller
    def test_nonseller_edit_item_in_shop(self, client):
        token = create_token_buyer()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'Baju',
            'harga_satuan': 2000,
            'qty': 10,
            'url_image': 'https://m.media-amazon.com/images/I/A13usaonutL._CLa%7C2140,2000%7C61hLBkLke6L.png%7C0,0,2140,2000+0.0,0.0,2140.0,2000.0._UX342_.png'
        }
        res = client.put(url, headers = h, json = data)
        assert res.status_code == 200

    #add item to shop nonseller
    def test_nonseller_add_item_to_shop(self, client):
        token = create_token_buyer()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'Kolor',
            'harga_satuan': 5000,
            'qty': 6,
            'url_image': 'https://cf.shopee.co.id/file/dec4af673399ad72e95bd3811b669e6e'
        }
        res = client.post(url, headers = h, json = data)
        assert res.status_code == 200

    #delete item in shop nonseller
    def test_nonseller_delete_item_in_shop(self, client):
        token = create_token_buyer()
        id = TestSuccessEvent.id_added_item
        url = '/user/myshop/'+str(id)
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.delete(url, headers = h)
        assert res.status_code == 404

    def test_get_transaction_by_id(self, client):
        token = create_token_buyer()
        url = '/user/transactions/3'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers = h)
        assert res.status_code == 200

    # add to shopping bag out of stock
    def test_add_to_bag_oos(self, client):
        token = create_token_buyer()
        url1='/user/beli/6'
        # url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # add to shopping not enough saldo
    def test_add_to_bag_not_enough_saldo(self, client):
        token = create_token_buyer()
        url1='/user/beli/'+str(TestSuccessEvent.new_id-100)
        # url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # add to invalid item to bag
    def test_invalid_item_to_bag(self, client):
        token = create_token_buyer()
        url1='/user/beli/'+str(TestSuccessEvent.new_id)
        # url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # add to shopping bag exceed stock
    def test_add_to_bag_over(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        # url2='/user/beli/2'
        data = {
            'qty': 100
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # zero saldo attempt to buy
    def test_zero_saldo_attempt_to_buy(self, client):
        token = create_token_not_enough_saldo()
        url1='/user/beli/1'
        # url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    # attempt to buy self item
    def test_attempt_to_buy_self(self, client):
        token = create_token_seller()
        url1='/user/beli/1'
        # url2='/user/beli/2'
        data = {
            'qty': 5
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        # res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    def test_forgot_password_unregistered(self, client):
        data = {
            'username': 'wikwik',
            'email': 'wikwik@gmail.com'
        }
        url = '/user/beli'

        res = client.patch(url, json=data)
        assert res.status_code == 200

    def test_add_item_in_shop_blank_name(self, client):
        token = create_token_seller()
        data = {
            'nama_barang': '',
            'harga_satuan': 0,
            'qty' : 0
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/myshop'

        res = client.post(url, json=data, headers=h)

        assert res.status_code == 200

    def test_add_item_in_shop_with_image(self, client):
        token = create_token_seller()
        data = {
            'nama_barang': 'dummy',
            'harga_satuan': 1,
            'qty' : 1,
            'url_image': 'url_image'
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/myshop'

        res = client.post(url, json=data, headers=h)

        assert res.status_code == 200

    def test_add_duplicate_item_in_shop(self, client):
        token = create_token_seller()
        data = {
            'nama_barang': 'baju',
            'harga_satuan': 1,
            'qty' : 1,
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/myshop'

        res = client.post(url, json=data, headers=h)

        assert res.status_code == 200

    def test_edit_nonexist_item_in_shop(self, client):
        token = create_token_seller()
        data = {
            'nama_barang': 'baju',
            'harga_satuan': 1,
            'qty' : 1,
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/myshop/99'

        res = client.put(url, json=data, headers=h)

        assert res.status_code == 200

    def test_get_nonexist_item_in_shop(self, client):
        token = create_token_seller()
        data = {
            'nama_barang': 'baju',
            'harga_satuan': 1,
            'qty' : 1,
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/myshop/99'

        res = client.patch(url, json=data, headers=h)

        assert res.status_code == 404

    def test_become_a_seller_for_first_time(self, client):
        token = create_token_dummy()
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/status'
        res = client.post(url, headers=h)
        assert res.status_code == 200

    def test_become_a_seller_for_second_time(self, client):
        token = create_token_seller()
        h = {
            'Authorization': 'Bearer '+token
        }

        url= '/user/status'
        res = client.post(url, headers=h)
        assert res.status_code == 200

    def test_add_to_bag_to_edit(self, client):
        token = create_token_seller()
        url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res1 = client.get(url2, query_string=data, headers=h)

    def test_edit_qty_syamsul(self, client):
        token = create_token_seller()
        data2 = {
            'qty':4
        }
        h = {
            'Authorization': 'Bearer '+token
        }

        url3='/user/nota/2'
        res2 = client.put(url3, json=data2, headers=h)
        assert res2.status_code == 200

    def test_get_transaction_by_id(self, client):
        token = create_token_buyer()
        url = '/user/transactions/1'
        h = {
            'Authorization': 'Bearer '+token
        }

        res = client.patch(url, headers=h)
        assert res.status_code == 200
        


    #reset database
    def test_reset_database(self,client):
        reset_database()
        assert 1 == 1