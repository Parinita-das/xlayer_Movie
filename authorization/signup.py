import json
from bson.objectid import ObjectId
import tornado.web

from con import Database

class UserHandler(tornado.web.RequestHandler, Database):

    userTable = Database.db['user']

    #Create
    async def post(self):
        code = 1000
        status = False
        result = []
        message = ''

        try:
            # Parse the request body as JSON
            try:
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 1001
                message = "Invalid JSON"
                raise Exception

            print(self.request.arguments)

            #fields with validation

            mName = self.request.arguments.get('name')
            if not mName:
                message = 'Name is required'
                code = 4434
                raise Exception
            elif type(mName) != str:
                message = 'name should be in string'
                code = 4922
                raise Exception
            elif len(mName) > 50:
                message = 'length should be withing 50'
                code = 4512
                raise Exception
            
            mEmail = self.request.arguments.get('email')
            if not mEmail or '@' not in mEmail:
                message = 'email_id is required'
                code = 4533
                raise Exception

            mMobile = self.request.arguments.get('mobile')
            if not mMobile:
                message = 'mobile number is required'
                code = 4534
                raise Exception
            elif len(str(mMobile))!= 10:
                message = 'Invalid Mobile Number'
                code = 4535
                raise Exception
            elif not isinstance(mMobile, str) or not mMobile.isdigit():
                message = 'Mobile number should contain only digits'
                code = 4536
                raise Exception
            
            
            mPassword = self.request.arguments.get('password')
            if not mPassword:
                message = 'Input a password'
                code = 4536
                raise Exception
            elif len(mPassword) < 8 :
                message = 'password should have at least 8 character'
                code = 4537
                raise Exception

            mConfirmPassword = self.request.arguments.get('confirmPassword')
            if mPassword != mConfirmPassword:
                code = 1001
                message = "Passwords do not match"
                raise Exception
            
            # Create the user data dictionary
            data = {
                'name': mName,
                'email': mEmail,
                'mobile': mMobile,
                'password': mPassword
            }

            # # Insert the user into the database
            addUser = await self.userTable.insert_one(data)

            if addUser.inserted_id:
                code = 2000
                status = True
                message = "User added successfully"
                result.append(
                    {
                        'userId': str(addUser.inserted_id)
                    }
                )
            else:
                code = 1006
                message = "Failed to add user"
                raise Exception

 
        except Exception as e:
            code = 1005
            if not len(message):
                message = 'Internal error'
                print(e)
                raise Exception
        
        response = {
                'code': code,
                'message': message,
                'status': status,
            }

        try:
            if len(result):
                response['result'] = result
            #self.write(json.dumps(response))
            self.write(response)
            self.finish()
        except Exception as e:
            message = 'There is some issue'
            code = 1007
            raise Exception    
            
    #Retrieve
    async def get(self):

        code = 1000
        status = False
        result = []
        message = ''

        try:
            try:
                mUserId = self.get_argument('userId')
                if not mUserId:
                    raise Exception
                mUserId = ObjectId(mUserId)
            except Exception as e:
                mUserId = None
            
            query = {}
            if mUserId:
                query = { 
                    '_id': mUserId
                }
            mUser = self.userTable.find(query)
            async for user in mUser:
                user['_id'] = str(user.get('_id'))
                result.append(user)
            if len(result):
                message = 'Found'
                code = 1002
                status = True
            else:
                message = 'No data found'
                code = 1003
                raise Exception
            
        except Exception as e:
            print(e)
            if not len(message):
                message = 'There is some issue'
                code = 1004
                raise Exception
        
        try:
            response = {
                'code': code,
                'message': message,
                'status': status,
            }
            if len(result):
                response['result'] = result
            self.write(response)
            self.finish()
            return
        except:
            message = 'There is some issue'
            code = 1005
            raise Exception