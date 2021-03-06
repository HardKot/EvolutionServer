import os
from datetime import datetime
from flask import request
from peewee import DoesNotExist

from app import app as rest_api
from utils.fireBase import authorizationWithFireBase, authorizationRequestWithFireBaseAuthorization
from utils.Errors import *
from models.User import User, UserRole, StatusAuthentication
from models.Order import Order, OrderStatus
from models.Product import Product
from models.Plant import Plant, PlantStatus
from models.Errors import *


def createJSONAnswer(user_id=None, code=200, **kwargs):
    return {'uid': user_id, 'timeReturn': datetime.now().isoformat(), **kwargs}, code


def createJSONReject(message: str, code=500, **kwargs):
    return createJSONAnswer(status='Error', message=message, code=code, **kwargs)


@rest_api.route('/api/users', methods=['POST'])
@rest_api.route('/api/users/<user_id>', methods=['DELETE', 'PUT'])
@authorizationWithFireBase
def users(request_uid, user_id=None):
    if user_id is None:
        user_id = request_uid
    try:
        if request_uid != user_id:
            user = User.get_by_id(request_uid)
            if user.role != UserRole.ADMIN:
                raise AccessDenied()
        if request.method == 'POST':
            request_data = request.get_json()
            user = User.createAccount(uid=user_id, **request_data)
            return createJSONAnswer(user_id=request_uid, status='AccountCreate',
                                    result=user.serialization(is_minimum_data=False))
        elif request.method == 'PUT':
            user = User.get_by_id(user_id)
            if request.files.get('image', False):
                user.updateData(image=request.files['image'])
                return createJSONAnswer(user_id=request_uid, status='User image suspect update',
                                        result=user.serialization(get_plants=False))
            else:
                request_data = request.get_json()
                user.updateData(**request_data)
                print(type(user.serialization()['status']))
                return createJSONAnswer(user_id=request_uid, status='User data suspect update',
                                        result=user.serialization())
    except DoesNotExist:
        return createJSONReject(message=str(TheUserNoExists(uid=user_id)), user_id=request_uid)
    except FileTypeError:
        return createJSONReject(message=str(FileTypeError(desired_type=FileType.IMG)), user_id=request_uid)
    except NicknameNoUnique:
        return createJSONReject(user_id=request_uid, message=str(NicknameNoUnique()))
    except TheUserExists:
        return createJSONReject(message=str(TheUserExists(uid=user_id)), user_id=request_uid)
    except AccessDenied:
        return createJSONReject(message=str(AccessDenied()), code=403)
    # except:
    #     return createJSONReject(user_id=request_uid, message=str(UnknownError()))


@rest_api.route('/api/users.search/<nick_name>', methods=['GET'])
def searchUser(nick_name):
    get_plants = True if request.args.get(
        'get_plants', 'false').lower() == 'true' else False
    is_minimum_data = True if request.args.get(
        'is_minimum_data', 'true').lower() == 'true' else False
    users = User.searchByNicknameOrDisplayName(
        nick_name=nick_name,
        strong=(True if request.args.get('strong', 'false').lower()
                == 'true' else False) or len(nick_name) < 4,
        limit=int(request.args.get('limit', 20))
    )

    return createJSONAnswer(
        result=list(map(lambda user: user.serialization(
            get_plants=get_plants, is_minimum_data=is_minimum_data), users))
    )


@rest_api.route('/api/users', methods=['GET'])
@rest_api.route('/api/users/<user_id>', methods=['GET'])
def getUser(user_id=None):
    try:
        get_plants = True if request.args.get(
            'get_plants', 'false').lower() == 'true' else False
        is_minimum_data = True if request.args.get(
            'is_minimum_data', 'false').lower() == 'true' else False
        if user_id is not None:
            user = User.get_by_id(user_id)
            user_data = user.serialization(is_minimum_data=is_minimum_data)
            if get_plants:
                plants, plants_count = Plant.getByUser(user=user)
                user_data['plantCount'] = plants_count
                if not is_minimum_data:
                    user_data['plants'] = []
                    for plant in plants:
                        user_data['plants'].append(
                            plant.serialization(is_minimum_data=True))
            return createJSONAnswer(result=user_data)
        else:
            users_ = []
            users_ = User.select()
            users = []
            for user in users_:
                users.append(user.serialization(
                    is_minimum_data=is_minimum_data))
            return createJSONAnswer(result=users)
    except DoesNotExist:
        return createJSONReject(message=str(TheUserNoExists(uid=user_id)))
    except:
        return createJSONReject(user_id=user_id, message=str(UnknownError()))


@rest_api.route('/api/orders', methods=['POST', 'PUT', 'DELETE'])
@rest_api.route('/api/orders/<order_id>', methods=['POST', 'PUT', 'DELETE'])
@authorizationRequestWithFireBaseAuthorization(stronger=False)
def orders(request_uid, order_id=None):
    try:
        if request_uid is None and request.method == 'POST':
            request_data = request.get_json()
            is_tinkoff = True if request_data.get(
                'TerminalKey', None) == os.environ['TERMINAL_KEY'] else False
            if is_tinkoff:
                print(request_data)
                order = Order.get_by_id(request_data['OrderId'], None)
                if order.generateToken() != request_data['Token']:
                    raise AccessDenied()
                if request_data['Status'] in ['CANCELED', 'DEADLINE_EXPIRED', 'REJECTED', 'CONFIRMED']:
                    order.editStatusPayment(
                        status=OrderStatus.PAID if request_data['Status'] == 'CONFIRMED' else OrderStatus.CANCEL,
                        amount=request_data['Amount']
                    )
                return 'OK'
            raise UnknownError()
        elif request.method == 'POST':
            if order_id is None:
                request_data = request.get_json()
                product_id = request_data.get(
                    'product_id', os.environ['ID_REGISTRATION_PLANTS'])
                user = User.get_by_id(request_uid)
                product = Product.get_by_id(product_id)
                if product_id == os.environ['ID_REGISTRATION_PLANTS']:
                    amount = request_data.get('amount', 30000)
                    if amount <= 500:
                        raise TheAmountIsTooSmall()
                    order = Order.createOrder(user=user, product=product, amount=amount,
                                              plant_id=request_data.get('plant_id', None))
                else:
                    order = Order.createOrder(user=user, product=product)
                return order.serialization()
            else:
                order = Order.get_by_id(order_id)
        elif request.method == 'PUT':
            pass
    except TheAmountIsTooSmall:
        return createJSONReject(message=str(TheAmountIsTooSmall()))
    except AccessDenied:
        return createJSONReject(message=str(AccessDenied()))
    # except:
    #    return createJSONReject(message=str(UnknownError()))


@rest_api.route('/api/plants', methods=['POST'])
@rest_api.route('/api/plants/<plant_id>', methods=['PUT', 'DELETE'])
@authorizationRequestWithFireBaseAuthorization(stronger=True)
def plants(request_uid, plant_id=None):
    try:
        user = User.get_by_id(request_uid)
        if plant_id is None and request.method == 'POST':
            plant_data = request.get_json()
            name, coordinate, category = plant_data['name'], plant_data['coordinate'], plant_data['category']
            image = plant_data['image'] if plant_data.get(
                'Image', False) else None
            amount = plant_data['amount'] if plant_data.get(
                'amount', False) else None
            message = plant_data['message'] if plant_data.get(
                'message', False) else None
            plant = Plant.plantingPlant(name=name, coordinate=coordinate, category=category,
                                        image=image, amount=amount, message=message, user=user)
            result = {
                'plant': plant.serialization(is_minimum_data=True)
            }
            if plant.status == PlantStatus.AWAITING_PAYMENT:
                order = Order.createOrder(user=user, product=os.environ['ID_REGISTRATION_PLANTS'],
                                          amount=amount, plant_id=plant.id)
                result['order_id'] = order.serialization()
            return createJSONAnswer(user_id=request_uid, result=result)
        elif plant_id is not None and request.method == 'PUT':
            plant = Plant.get_by_id(plant_id)
            if plant.user != user and user.role != UserRole.ADMIN:
                raise AccessDenied()
            if request.files.get('image', False) or request.get_json().get('image', False):
                type_image = 'file' if request.files.get(
                    'image', False) else 'string'
                plant.updateData(
                    image=request.files['image'] if type_image else request.get_json()['image'])
                return createJSONAnswer(user_id=request_uid, status='Plant image suspect update',
                                        result=plant.serialization())
            request_data = request.get_json()
            if request_data.get('amount', False) and user.role == UserRole.ADMIN and \
                    plant.status == PlantStatus.PLANTED:
                plant.updateData(amount=request_data['amount'])
                return createJSONAnswer(user_id=request_uid, status='Plant amount update',
                                        result=plant.serialization())
        return createJSONReject(message='Bad Error', code=400)
    except RequiredFields:
        return createJSONReject(message=str(RequiredFields()))
    except DoesNotExist:
        return createJSONReject(message=str(TheUserNoExists(uid=plant_id)), user_id=request_uid)
    except FileTypeError:
        return createJSONReject(message=str(FileTypeError(desired_type=FileType.IMG)), user_id=request_uid)
    except AccessDenied:
        return createJSONReject(message=str(AccessDenied()), code=403)
    # except:
    #    return createJSONReject(message=str(UnknownError()))


@rest_api.route('/api/authentication', methods=['GET'])
@authorizationRequestWithFireBaseAuthorization(stronger=True)
def authentication(request_uid):
    try:
        user = User.get_by_id(request_uid)
        return createJSONAnswer(user_id=request_uid, result={'user_data': user.serialization(), 'statusAuthentication': StatusAuthentication.AUTHORIZED.name})
    except DoesNotExist:
        return createJSONAnswer(user_id=request_uid, result={'user_data': None, 'statusAuthentication': StatusAuthentication.AUTHORIZED.name})
    # except:
    #   return createJSONReject(message=str(UnknownError()))


@rest_api.route('/api/nickName/<nick_name>', methods=['GET'])
def nickName(nick_name):
    try:
        generate_nickname = True if request.args.get(
            'generate_nickname', 'false').lower() == 'true' else False
        result_checking_unique_nick_name = User.checkUniqueNickname(
            nick_name.lower())
        if generate_nickname and not result_checking_unique_nick_name:
            return createJSONAnswer(result={
                'checking_unique_nick_name': result_checking_unique_nick_name,
                'nickname_variable': User.generateUniqueNickname(nick_name)
            })
        else:
            return createJSONAnswer(result={'checking_unique_nick_name': result_checking_unique_nick_name})
    except NicknameNoUnique:
        return createJSONReject(message=str(UnknownError()))


# @rest_api.route('/api/meditation', methods=['POST', 'PUT'])
# @authorizationRequestWithFireBaseAuthorization(stronger=True)
# def meditation(request_uid):
#     try:

#     except:
#         return createJSONReject(message=str(UnknownError()))
