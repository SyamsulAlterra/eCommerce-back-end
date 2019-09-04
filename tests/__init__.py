import pytest,json, logging
from flask import Flask, request

from blueprints import app, db
from blueprints.user.model import User
from blueprints.barang.model import Barang
from app import cache

def call_client(request):
    client=app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():

    db.drop_all()
    db.create_all()
    nama = ['aul', 'syamsul', 'raden', 'yovan', 'dummy']
    email ='abc@gmail.com'
    status_penjual = [False, True, True, True, False]
    rating = [8, 8, 8, 8, 8]
    saldo = [0, 100000, 200000, 250000, 20000]
    password = 'abc'
    for i in range(len(nama)):
        user = User(nama[i],password,email,status_penjual[i], rating[i], saldo[i])
        db.session.add(user)
        db.session.commit()

    nama_barang = ['baju', 'sepatu', 'kulkas', 'bola', 'raket', 'jam tangan', 'barang kosong']
    id_pemilik = [2, 3, 4, 2, 3, 4, 2]
    harga_satuan = [1000, 3000, 7000, 2000, 6000, 100000, 1000]
    qty = [100, 3, 1, 3, 2, 1, 0]
    rating_penjual = 8
    url = [
        'https://m.media-amazon.com/images/I/A13usaonutL._CLa%7C2140,2000%7C61hLBkLke6L.png%7C0,0,2140,2000+0.0,0.0,2140.0,2000.0._UX342_.png',
        'https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium//93/MTA-2945316/nike_nike-air-more-uptempo-supreme-sepatu-sneakers-pria---red-white_full05.jpg',
        'http://sinarberlianelektronik.com/wp-content/uploads/2016/09/Kulkas-SHARP-SJ-421KP_ADJ.png',
        'https://cdn2.tstatic.net/pekanbaru/foto/bank/images/ilustrasi_sepak_bola_sepakbolajpg_20170724_121315.jpg',
        'https://www.4muda.com/wp-content/uploads/2015/08/raket-bulutangkis-wilson-1.jpg',
        'https://www.jakartanotebook.com/images/products/77/63/28045/2/jam-tangan-wanita-unique-dial-black-13.jpg',
        ''
    ]
    deleted_status = False

    for i in range(len(nama_barang)):
        barang = Barang(
            nama_barang[i],
            id_pemilik[i],
            harga_satuan[i],
            qty[i],
            url[i]
        )
        db.session.add(barang)
        db.session.commit()



    # admin = UserModel("admin-tria", bcrypt.generate_password_hash("triapass"), "0986463", "Balikpapan", "admin")

    # # create test non-admin user

    # # save users to database
    # db.session.add(admin)
    # db.session.commit()

def create_token_buyer():
    token = cache.get('test-token-internal')
    if token is None:
        data={
            'nama' : 'aul',
            'password': 'abc'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_seller():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'nama' : 'syamsul',
            'password': 'abc'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-non-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_dummy():
    token = cache.get('test-token-dummy')
    if token is None:
        data={
            'nama' : 'dummy',
            'password': 'abc'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-dummy', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_not_enough_saldo():
    token = cache.get('test-token-not-enough-saldo')
    if token is None:
        data={
            'nama' : 'tes',
            'password': 'tes'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-not_enough_saldo', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_invalid():
    token = cache.get('test-invalid')
    if token is None:
        data={
            'nama' : 'tes',
            'password': 't'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-invalid', 'zong',timeout=60)

        return 'zong'
    else:
        return token