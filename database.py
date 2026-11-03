import pyrebase
import json
class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()


    def insert_item(self,name, data,img_path):

        item_info={
            "prodName": data.get('prodName'),
            "sellerId": data.get('sellerId'),
            "price": data.get('price'),
            "address": data.get('address'),
            "status": data.get('status'),
            "email": data.get('email'),
            "img_path": img_path,
        }

        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True

    # 회원가입 시 DB에 회원정보 저장
    def insert_user(self, data, pw):
        user_info ={
            "id": data['user_id'],
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['user_id'])):
            self.db.child("user").push(user_info)
            return True
        else:
            return False

    # 회원가입 시 아이디 중복 체크
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True