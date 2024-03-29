from flask import Blueprint, request, redirect, request, url_for, flash, Response, jsonify, make_response
from database import db
from models import Route
import validator
from response_builder import get_route, get_routes, get_route_xml, get_routes_xml, get_route_response, error_toxml
from errors import errors_dic, custom_errors_dic

route_blueprint = Blueprint('route_blueprint', __name__)

#GET route
@route_blueprint.route('/api/resources/user/route')
def route():
    request_id = request.args.get('id')

    if request_id is None:
        if request.content_type == 'application/json':
            result = Route.query.all()
            if validator.validateJsonResponse(r'validators\json\get_route_schema.json', get_routes(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_routes(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Route.query.all()
            if validator.validateXmlResponse(r'validators\xml\get_route_schema.xsd', get_routes_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_routes_xml(result), mimetype='text/xml',status=200)
    else:
        if request.content_type == 'application/json':
            result = Route.query.filter_by(id=request_id).first()
            if validator.validateJsonResponse(r'validators\json\get_route_schema.json', get_route(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_route(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Route.query.filter_by(id=request_id).first()
            if validator.validateXmlResponse(r'validators\xml\get_route_schema.xsd', get_route_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_route_xml(result), mimetype='text/xml',status=200)
        
#POST route
@route_blueprint.route('/api/resources/user/route', methods=['POST'])
def route_post():
    if request.content_type == 'application/json':
        if validator.validateJsonResponse(r'validators\json\post_put_route_schema.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        name = list(request.json.get('route'))[0]
        start = request.json.get('route').get(name).get('locations').get('start_id', None)
        end = request.json.get('route').get(name).get('locations').get('end_id', None)
        user_id = request.json.get('route').get(name).get('user_id',None)
        if not name:
            return make_response(jsonify(errors_dic[7]), 422)
        if not start:
            return make_response(jsonify(errors_dic[7]), 422)
        if not end:
            return make_response(jsonify(errors_dic[7]), 422)
        if not user_id:
            return make_response(jsonify(errors_dic[7]), 422)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        if validator.validateXmlResponse(r'validators\xml\post_put_route_schema.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        name = get_route_response(request.data)['route']['name']
        start = get_route_response(request.data)['route']['locations']['start_id']
        end = get_route_response(request.data)['route']['locations']['end_id']
        user_id = get_route_response(request.data)['route']['user_id']
        if not name:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        if not start:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        if not end:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        if not user_id:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    else:
        return make_response(jsonify(errors_dic[6]), 415)
    new_route = Route(name=name, start_id=start, end_id=end, user_id=user_id)
    db.session.add(new_route)
    db.session.commit()
    if request.content_type == 'application/json':
        return Response('Route added!',mimetype='application/json',status=201)
    if request.content_type == 'application/xml' or request.content_type == 'text/xml':
        return Response('Route added!',mimetype='text/xml',status=201)
    
#UPDATE place
@route_blueprint.route('/api/resources/user/route', methods=['PUT'])
def route_put():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        update = Route.query.filter_by(id=request_id).first()
        name = None
        start = None
        end = None
        user_id = None
        if request.content_type == 'application/json':
            if validator.validateJsonResponse(r'validators\json\post_put_route_schema.json', request.json):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            name = list(request.json.get('route'))[0]
            start = request.json.get('route').get(name).get('locations').get('start_id', None)
            end = request.json.get('route').get(name).get('locations').get('end_id', None)
            user_id = request.json.get('route').get(name).get('user_id',None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            if validator.validateXmlResponse(r'validators\xml\post_put_route_schema.xsd', request.data) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            name = get_route_response(request.data)['route']['name']
            start = get_route_response(request.data)['route']['locations']['start_id']
            end = get_route_response(request.data)['route']['locations']['end_id']
            user_id = get_route_response(request.data)['route']['user_id']
        else:
            return make_response(jsonify(errors_dic[6]), 415)
        if update is None:
            if request.content_type == 'application/json':
                return make_response(jsonify(errors_dic[2]), 404)
            if request.content_type == 'application/xml' or request.content_type == 'text/xml':
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
        if name is not None:
            update.name = name
        if start is not None:
            update.start_id = start
        if end is not None:
                update.end_id = end
        if user_id is not None:
            update.user_id = user_id
        db.session.commit()
        if request.content_type == 'application/json':
            return Response('Route updated',mimetype='application/json')
        if request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Route updated',mimetype='text/xml')
        
#DELETE place
@route_blueprint.route('/api/resources/user/route', methods=['DELETE'])
def route_delete():
    request_id = request.args.get('id')
    if request_id is None:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        if request.content_type == 'application/json':
            place = Route.query.filter_by(id=request_id)
            if place is None:
                return make_response(jsonify(errors_dic[2]), 404)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            place = Route.query.filter_by(id=request_id)
            if place is None:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='text/xml')