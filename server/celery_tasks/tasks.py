import json
import random
import time
from datetime import datetime

from sqlalchemy import func

from api.classes import DataExtractor
from app.extensions import celery, socketio, db
from models.algorithms import Algorithms
from models.analyses import Analyses
from models.basic_analysis import BasicAnalysis
from models.change_analysis import ChangeAnalysis
from models.monte_carlo_analysis import MonteCarloAnalysis
from models.notification import Notifications
from models.start_drawdown_analysis import StartDrawdownAnalysis


@celery.task(name='tasks.execute_analysis', bind=True)
def execute_analysis(self, alg, analysis_type: str, params: dict):
    from app.extensions import logger
    try:
        task_id = self.request.id
        alg['added_date'] = datetime.strptime(alg['added_date'], "%Y-%m-%d")
        # alg['oos_bdate'] = datetime.strptime(alg['oos_bdate'], "%Y-%m-%d")
        alg = Algorithms.query.get((alg['name'], alg['user_id']))
        # The reason why I commented out and used .get() is so that alg.trades will be available for the analyses.
        #(user_id=alg['user_id'], name=alg['name'], added_date=alg['added_date'], oos_bdate=alg['oos_bdate'],
        # ws_filename=alg['ws_filename'], report_filename=alg['report_filename'])

        notification = Notifications(user_id=alg.user_id, added_date=datetime.now(),
                                     data=json.dumps({
                                         'endpoint': 'algorithms',
                                         'message': analysis_type,
                                         'id': alg.name
                                     }))
        db.session.add(notification)
        db.session.commit()

        old = Analyses.query.filter(Analyses.user_id == alg.user_id, Analyses.alg_name == alg.name,
                                    Analyses.analysis_type == analysis_type)


        if analysis_type == BasicAnalysis.__tablename__:
            an = BasicAnalysis.execute(alg, DataExtractor(alg), params, old)
        elif analysis_type == MonteCarloAnalysis.__tablename__:
            an = MonteCarloAnalysis.execute(alg, DataExtractor(alg), params, old)
        elif analysis_type == StartDrawdownAnalysis.__tablename__:
            an = StartDrawdownAnalysis.execute(alg, DataExtractor(alg), params, old)
        elif analysis_type == ChangeAnalysis.__tablename__:
            an = ChangeAnalysis.execute(alg, None, params, old.first())
        else:
            raise Exception("Unknown analysis type")

        '''
        Why this sleep.
        There is an issue with fast performing analyses such as basic analysis.
        What happens is that the client waits for a confirmation that the analysis was submitted.
        If given, the client opens up a socket and wait for a notification.
        The problem is that, when the server send the "analysis request submitted" response to the user,
        celery worker also gets the analysis to perform.
        And now the question is who is quicker.
        
        
        Now what currently I attempting something new, previously in the client, I waited for that message 
        to open up a socket in the client, because socket is expensive and unless the analysis was submitted 
        successfully I don't want to open up a socket.
        
        So in Algorithm.js in the client I had dispatch(createNewAnalysis()) fired only when the response 
        for successful submission arrived from the server.
        I moved it to the top because the chances of failed request are narrow.
        If the problem repeats itself, because it still can. I'll return time.sleep(2) 
        '''
        # time.sleep(2)

    # notification = Notifications(user_id=alg.user_id, added_date=datetime.now(),
    #                              data=json.dumps({
    #                                  'endpoint': 'algorithms',
    #                                  'id': alg.name
    #                              }))

        if bool(old.first()):
            old.delete()
        db.session.add(an)
        notification.state = 'DONE'
        db.session.add(notification)
        db.session.commit()
        # TODO: why do I need pending count in the response?
        # Faster COUNT: https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query#:~:text=The%20SQLAlchemy%20count%20function%20takes,same%20query%20directly%20in%20MySQL.
        query = db.session.query(func.count(Notifications.added_date)).filter(Notifications.state == 'PENDING')
        socketio.emit('analysis_results_ready',
                      {'data': notification.as_dict(), 'pending': query.scalar()},
                      namespace='/main_socket')
    except Exception as e:
        logger.exception(f"Celery task error: {str(e)}")
        notification = Notifications(user_id=alg.user_id, added_date=datetime.now(),
                                     data=json.dumps({
                                         'endpoint': 'algorithms',
                                         'message': "The server encountered an error, performing the analysis, please try again later.",
                                         'id': alg.name
                                     }))
        db.session.add(notification)
        db.session.commit()
        query = db.session.query(func.count(Notifications.added_date)).filter(Notifications.state == 'PENDING')
        socketio.emit('analysis_fail',
                      {'data': notification.as_dict(), 'pending': query.scalar()},
                      namespace='/main_socket')

#
#         an = BasicAnalysis()
# @celery.task(name='do_analysis_tasker', bind=True)
# def do_analysis_task(self, data):
#     self.update_state(state=states.PENDING)
#     alg_name = data['alg_name']
#     analysis_type = int(data['analysis_type'])
#     try:
#         analysis_type = AnalysesTypes(analysis_type)
#     except ValueError:
#         return jsonify(error="Invalid analysis type given")
#     alg = db.get_algorithm_by_name(alg_name)
#     de = DataExtractor(alg, app.config['PERFORMANCE_FILES_UPLOAD_FOLDER'])
#     # Some delay code
#     # i = 2 ** 26
#     # while i:
#     #     i -= 1
#     an = None
#     if analysis_type == AnalysesTypes.BASIC:
#         an = BasicAnalysis()
#     an.set_data_extractor(de)
#     an.run_analysis()
#     db.insert_analysis(an)  # Will automatically override existing one.
#     return get_template_embedded_results([an])[0]
