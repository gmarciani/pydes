from core.rnd import rndgen
from core.rnd import rndvar
from core.simulations.web.calendar import Calendar
from core.simulations.web.metrics import NodeMetricTracker
from core.utils.report import SimpleReport
from core.utils import guiutils

# Events
SESSION_ARRIVAL = 0
REQUEST_ARRIVAL = 1
FEND_COMPLETION = 2
BEND_COMPLETION = 3

# Random Streams
STREAM_SESSION_ARRIVAL = 0
STREAM_REQUEST_ARRIVAL = 1
STREAM_FEND_COMPLETION = 2
STREAM_BEND_COMPLETION = 3
STREAM_SESSION_LENGTH = 4

# Queueing Network Parameters
SESSION_ARRIVAL_RATE = 35.0     # requests/second (exponentially distributed
SESSION_LENGTH_LB = 5           # requests/session (equilikely distributed, min)
SESSION_LENGTH_UB = 35          # requests/session (equilikely distributed, max)
THINK_AVERAGE = 7.0             # seconds/request (exponentially distributed)
FEND_SERVICE_AVERAGE = 0.00456  # seconds/request (exponentially distributed)
BEND_SERVICE_AVERAGE = 0.00117  # seconds/request (exponentially distributed)


class Simulation(object):

    def __init__(self,
                 session_arrival_rate=SESSION_ARRIVAL_RATE,
                 session_length_lb=SESSION_LENGTH_LB,
                 session_length_ub=SESSION_LENGTH_UB,
                 think_average=THINK_AVERAGE,
                 fend_service_average=FEND_SERVICE_AVERAGE,
                 bend_service_average=BEND_SERVICE_AVERAGE):
        """
        Creates a new simulation instance.
        :param session_arrival_rate: (float) the sessions arrival rate
        in requests/second; (default is 35.0).
        :param session_length_lb: (int) the minimum session length
        in requests/session; (default is 5.0).
        :param session_length_ub: (int) the maximum session length
        in requests/session; (default is 35.0).
        :param think_average: (float) the terminal think time in
        seconds/request; (default is 7.0).
        :param fend_service_average: (float) the front-end service rate
        in seconds/request; (default is 0.00456).
        :param bend_service_average: (float) the back-end service rate
        in seconds/request (default is 0.00117).
        """

        # Simulation Parameters
        self._stop = 0.0
        self._replications = 1
        self._generator = rndgen.MarcianiMultiStream(123456789)

        # Calendar
        self._calendar = Calendar([
            SESSION_ARRIVAL,
            REQUEST_ARRIVAL,
            FEND_COMPLETION,
            BEND_COMPLETION
        ], t_clock=0.0)

        # Queueing Network Parameters
        self._session_arrival_rate = session_arrival_rate
        self._session_length_lb = session_length_lb
        self._session_length_ub = session_length_ub
        self._think_average = think_average
        self._fend_service_average = fend_service_average
        self._bend_service_average = bend_service_average

        # States
        self._n_sess = 0
        self._n_fend = 0
        self._n_bend = 0

        # System Metrics
        self._completed_sessions = 0
        self._completed_requests = 0
        self._dropped_sessions = 0
        self._aborted_requests = 0

        # Front-End metrics
        self._track_fend = NodeMetricTracker()

        # Back-End metrics
        self._track_bend = NodeMetricTracker()

        # Session id
        self._sid = 0

        # Data structures
        self._sess_length = dict()
        self._fend_queue = []
        self._bend_queue = []

        self._t_last = 0.0

    def run(self, stop, replications=1):
        """
        Executes the simulation.
        :param stop: (float) a positive stop time.
        :param replications: (int) the number of replication of the simulation.
        :return: (SimpleReport) the simulation report.
        """
        # Initialization
        self._stop = stop
        self._replications = replications

        # Simulation Core
        t_session_arrival = self._calendar.get_clock() + self._get_session_inter_arrival()
        self._calendar.schedule(SESSION_ARRIVAL, t_session_arrival, self._sid)
        while self._calendar.get_clock() < self._stop:
            event_class, event_time, event_sid = self._calendar.get_next_event()

            self._track_fend.update(event_time, self._n_fend)
            self._track_bend.update(event_time, self._n_bend)
            self._calendar.set_clock(event_time)
            guiutils.print_progress(self._calendar.get_clock(), self._stop)
            if event_class is SESSION_ARRIVAL:
                self._handle_session_arrival(event_time, event_sid)
            elif event_class is REQUEST_ARRIVAL:
                self._handle_request_arrival(event_time, event_sid)
            elif event_class is FEND_COMPLETION:
                self._handle_fend_completion(event_time, event_sid)
            elif event_class is BEND_COMPLETION:
                self._handle_bend_completion(event_time, event_sid)
            else:
                pass

        # Report
        r = self._generate_report()
        return r

    def _handle_session_arrival(self, event_time, event_sid):
        """
        Handles the event *SESSION_ARRIVAL*
        :param event_time: (float) the event occurrence time.
        :param event_sid: (int) the session id.
        """
        self._n_sess += 1
        self._t_last = event_time
        self._sess_length[event_sid] = self._get_session_length()
        self._calendar.schedule(REQUEST_ARRIVAL, event_time, event_sid)
        self._sid += 1
        t_session_arrival = self._calendar.get_clock() + self._get_session_inter_arrival()
        if t_session_arrival < self._stop:
            self._calendar.schedule(SESSION_ARRIVAL, t_session_arrival, self._sid)
        else:
            self._calendar.mark_impossible(SESSION_ARRIVAL)

    def _handle_request_arrival(self, event_time, event_sid):
        """
        Handles the event *REQUEST_ARRIVAL*
        :param event_time: (float) the event occurrence time.
        :param event_sid: (int) the session id.
        """
        self._n_fend += 1
        if self._n_fend > 1:
            self._fend_queue.append(event_sid)
        else:
            t_fend_completion = self._calendar.get_clock() + self._get_fend_service()
            self._calendar.schedule(FEND_COMPLETION, t_fend_completion, event_sid)
        self._calendar.mark_impossible(REQUEST_ARRIVAL)

    def _handle_fend_completion(self, event_time, event_sid):
        """
        Handles the event *FEND_COMPLETION*
        :param event_time: (float) the event occurrence time.
        :param event_sid: (int) the session id.
        """
        self._n_fend -= 1
        if self._n_fend > 0:
            sid = self._fend_queue.pop()
            t_fend_completion = self._calendar.get_clock() + self._get_fend_service()
            self._calendar.schedule(FEND_COMPLETION, t_fend_completion, sid)
        else:
            self._calendar.mark_impossible(FEND_COMPLETION)

        self._n_bend += 1
        if self._n_bend > 1:
            self._bend_queue.append(event_sid)
        else:
            t_bend_completion = self._calendar.get_clock() + self._get_bend_service()
            self._calendar.schedule(BEND_COMPLETION, t_bend_completion, event_sid)

    def _handle_bend_completion(self, event_time, event_sid):
        """
        Handles the event *BEND_COMPLETION*
        :param event_time: (float) the event occurrence time.
        :param event_sid: (int) the session id.
        """
        self._n_bend -= 1
        self._completed_requests += 1
        if self._n_bend > 0:
            sid = self._bend_queue.pop()
            t_bend_completion = self._calendar.get_clock() + self._get_bend_service()
            self._calendar.schedule(BEND_COMPLETION, t_bend_completion, sid)
        else:
            self._calendar.mark_impossible(BEND_COMPLETION)

        self._sess_length[event_sid] -= 1
        if self._sess_length[event_sid] > 0:
            t_request_arrival = self._calendar.get_clock() + self._get_terminal_think()
            self._calendar.schedule(REQUEST_ARRIVAL, t_request_arrival, event_sid)
        else:
            self._n_sess -= 1
            self._completed_sessions += 1
            del self._sess_length[event_sid]

    def _get_session_inter_arrival(self):
        """
        Generates a session interarrival time, exponentially distributed with rate
        *SESSION_ARRIVAL_RATE*.
        :return (float) session interarrival time.
        """
        self._generator.stream(STREAM_SESSION_ARRIVAL)
        u = self._generator.rnd()
        m = 1.0 / self._session_arrival_rate
        t_session_inter_arrival = rndvar.exponential(m, u)
        return t_session_inter_arrival

    def _get_session_length(self):
        """
        Generates the number of requests per session, equilikely distributed in
        *[SESSION_LENGTH_LB, SESSION_LENGTH_UB]*.
        :return: (int) number of requests per session.
        """
        self._generator.stream(STREAM_SESSION_LENGTH)
        u = self._generator.rnd()
        a = self._session_length_lb
        b = self._session_length_ub
        requests = rndvar.equilikely(a, b, u)
        return requests

    def _get_terminal_think(self):
        """
        Generates a terminal think-time, exponentially distributed with average
        *THINK_AVERAGE*.
        :return (float) think-time.
        """
        self._generator.stream(STREAM_REQUEST_ARRIVAL)
        u = self._generator.rnd()
        m = self._think_average
        t_think = rndvar.exponential(m, u)
        return t_think

    def _get_fend_service(self):
        """
        Generates a front-end service-time, exponentially distributed with average
        *FEND_SERVICE_AVERAGE*.
        :return (float) front-end service-time.
        """
        self._generator.stream(STREAM_FEND_COMPLETION)
        u = self._generator.rnd()
        m = self._fend_service_average
        t_fend_service = rndvar.exponential(m, u)
        return t_fend_service

    def _get_bend_service(self):
        """
        Generates a back-end service-time, exponentially distributed with average
        *BEND_SERVICE_AVERAGE*.
        :return (float) back-end service-time.
        """
        self._generator.stream(STREAM_BEND_COMPLETION)
        u = self._generator.rnd()
        m = self._bend_service_average
        t_bend_service = rndvar.exponential(m, u)
        return t_bend_service

    def _generate_report(self):
        """
        Generates the simulation report
        :return: (SimpleReport) the simulation report.
        """
        simulation_time = self._calendar.get_clock()
        total_handled_sessions = self._n_sess + self._completed_sessions
        total_handled_requests = self._n_fend + self._n_bend + self._completed_requests
        average_inter_arrival_time = self._t_last / total_handled_sessions
        throughput = self._completed_sessions / simulation_time
        average_response_time = (self._track_fend.node + self._track_bend.node) / self._completed_requests

        fend_average_wait = self._track_fend.node / self._completed_requests
        fend_average_delay = self._track_fend.queue / self._completed_requests
        fend_average_service = self._track_fend.service / self._completed_requests
        fend_average_requests_in_node = self._track_fend.node / simulation_time
        fend_average_requests_in_queue = self._track_fend.queue / simulation_time
        fend_utilization = self._track_fend.service / simulation_time

        bend_average_wait = self._track_bend.node / self._completed_requests
        bend_average_delay = self._track_bend.queue / self._completed_requests
        bend_average_service = self._track_bend.service / self._completed_requests
        bend_average_requests_in_node = self._track_bend.node / simulation_time
        bend_average_requests_in_queue = self._track_bend.queue / simulation_time
        bend_utilization = self._track_bend.service / simulation_time

        drop_ratio = self._dropped_sessions / total_handled_sessions
        abort_ratio = self._aborted_requests / total_handled_requests

        r = SimpleReport('SIMULATION')
        r.add('General', 'Simulation Class', self.__class__.__name__)
        r.add('General', 'Replications', self._replications)
        r.add('General', 'Random Generator', self._generator.__class__.__name__)
        r.add('General', 'Simulation Time', self._stop)
        r.add('Overall', 'Sessions', total_handled_sessions)
        r.add('Overall', 'Requests', total_handled_requests)
        r.add('Overall', 'Session Inter-Arrival', average_inter_arrival_time)
        r.add('Overall', 'Throughput', throughput)
        r.add('Overall', 'Average response time', average_response_time)
        r.add('Overall', 'Drop Ratio', drop_ratio)
        r.add('Overall', 'Abort Ratio', abort_ratio)
        r.add('Front-End', 'Average Wait', fend_average_wait)
        r.add('Front-End', 'Average Delay', fend_average_delay)
        r.add('Front-End', 'Average Service', fend_average_service)
        r.add('Front-End', 'Average Requests in Node', fend_average_requests_in_node)
        r.add('Front-End', 'Average Requests in Queue', fend_average_requests_in_queue)
        r.add('Front-End', 'Utilization', fend_utilization)
        r.add('Back-End', 'Average Wait', bend_average_wait)
        r.add('Back-End', 'Average Delay', bend_average_delay)
        r.add('Back-End', 'Average Service', bend_average_service)
        r.add('Back-End', 'Average Requests in Node', bend_average_requests_in_node)
        r.add('Back-End', 'Average Requests in Queue', bend_average_requests_in_queue)
        r.add('Back-End', 'Utilization', bend_utilization)

        return r


if __name__ == '__main__':
    from experiments import EXP_DIR, RES_EXT

    sim = Simulation()
    rep = sim.run(3600.0, 1)
    rep.save('%s/%s.%s' % (EXP_DIR, sim.__class__.__name__, RES_EXT))
    print(rep)