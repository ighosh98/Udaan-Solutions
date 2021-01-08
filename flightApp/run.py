import flask
import os, sys
import json
from flask import jsonify, render_template,request

class Flight:
    def __init__(self,jsonIn):
        self.airlineName = jsonIn['airlineName']
        self.flightNumber = jsonIn['flightNumber']
        self.source = jsonIn['source']
        self.destination = jsonIn['destination']
        self.startTime = jsonIn['startTime']
        self.endTime = jsonIn['endTime']
        self.frequency = jsonIn['frequency']//array
        self.capacity = jsonIn['capacity']

    def toJson(self):
        return {'airlineName':self.airlineName,
        'flightNumber':self.flightNumber,
        'source':self.source,
        'destination':self.destination,
		'startTime':self.startTime,
		'endTime':self.endTime,
		'frequency':self.frequency,
        'capacity': self.capacity}

class Flyer:
    def __init__(self,jsonIn):
        self.flyerId = jsonIn['flyerId']
        self.flyerName = jsonIn['flyerName']
        self.reservations = jsonIn['reservations'] #array

    def addReservation(self,reservationIn):
        self.reservations.append(reservationIn)

    def toJson(self):
        return {'flyerId':self.flyerId, 'flyerName':self.flyerName, 'reservations':self.reservations}

class Reservation:
    def __init__(self,jsonIn):
        self.reservationId = jsonIn['reservationId']
        self.flightNumber = jsonIn['flightNumber']
        self.flyerId = jsonIn['flyerId']
        self.date = jsonIn['date']
        self.seatsReserved = jsonIn['seatsReserved'] #array

    def toJson(self):
        return {'reservationId' : self.reservationId,
		'flightNumber' : self.flightNumber,
		'flyerId' : self.flyerId,
		'seatsReserved' : self.seatsReserved,
		'date': self.date}

    def __eq__(self,other) :
        if (self.reservationId==other.reservationId and self.flightNumber==other.flightNumber and self.flyerId==other.flyerId and self.seatsReserved==other.seatsReserved and self.date==other.date):
            return True
        else:
            return False

class Helpers:
    def readFlightData(self):
        """
        :return: flight data in the form of JSON object
        """
        with open(os.path.join('database', 'flights.json'), 'r') as database:
            return json.loads(database.read())

    def readFlyerData(self):
        """
        :return: flyer data in the form of JSON object
        """
        with open(os.path.join('database', 'flyers.json'), 'r') as database:
            return json.loads(database.read())
    
    def readReservationData(self):
        """
        :return: reservation data in the form of JSON object
        """
        with open(os.path.join('database', 'reservations.json'), 'r') as database:
            return json.loads(database.read())
            
    def writeReservation(self,reservationData):
        """
        Function to update reservation data
        :param movie_data: New data of movies to override previous
        :return: None
        """
        with open(os.path.join('database', 'reservations.json'), 'w+') as database:
            database.write(json.dumps(reservationData))

    def writeFlyer(self,flightData):
        """
        Function to update reservation data
        :param movie_data: New data of movies to override previous
        :return: None
        """
        with open(os.path.join('database', 'flyers.json'), 'w+') as database:
            database.write(json.dumps(flightData))


    def writeFlight(self,flightData):
        """
        Function to update reservation data
        :param movie_data: New data of movies to override previous
        :return: None
        """
        with open(os.path.join('database', 'flights.json'), 'w+') as database:
            database.write(json.dumps(flightData))
    
    def is_available(self, source, destination, date):
        datetime_obj = datetime.datetime.strptime(date, format_str)
        week_day = datetime_obj.weekday()
        if self.source == source and self.destination == destination and self.frequency[week_day] == 1:
            return True
        return False


app = flask.Flask(__name__)
app.config["DEBUG"] = False 
app.run()

@app.route('/reserve', methods=['POST'])
def reserveSeats():
    data = request.get_json()
    _rJson = Helpers().readReservationData()
    rArr = [Reservation(_rJson[r]) for r in _rJson]
    rNew = Reservation(data)
    add = True
    for r in rArr:
        if r==rNew:
            add=False
    if (add==True):
        rArr.append(rNew)
        Helpers().writeReservation([r.toJson() for r in rArr])
    return {"success" : True}
    
@app.route('/flyer/<flyer_id>/', methods=['GET'])
def getFlyerReservations(flyer_id):
    """
    returns flights reserved by the user
    """
    _reservationsJson = Helpers().readReservationData()
    f = Flyer(Helpers().readFlyerData()[flyer_id])
    reservationsArr = [Reservation(_reservationsJson[r]) for r in _reservationsJson]
    reservationsF = [r for r in reservationsArr if r.flyerId==f.flyerId]
    return {"success" : True,
    "reservations" : [r.toJson() for r in reservationsF]}

@app.route('/search/', methods=['GET'])
def searchFlight():
    try:
        data = request.get_json()
        fJson = Helpers().readFlightData()
        fArr = [Flight(fJson[f] for f in fJson)]
        fFiltered = [f for f in fJson if f.source==data['source'] and f.destination==data['destination'] and dateTimeFunc(data['date']).day in f.frequency]
        return {"success": True,
				"flights": fFiltered}
    except Exception as e:
        # 	exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(sys.exc_info()[0], os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1], sys.exc_info()[2].tb_lineno)
        return {"success" : False, "exception" : str(e)
		# "exception" : {
		# 	"exceptionType" : sys.exc_info()[0],
		# 	"exceptionFile" : os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1],
		# 	"exceptionLine" : sys.exc_info()[2].tb_lineno
		# }
		}
