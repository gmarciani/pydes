"""
Next-Event simulation for a multi-tiered web-service.
"""

from demule.rnd import rndgen
from demule.rnd import rndvar
from demule.sim.metrics import NodeMetricTracker
from demule.sim.calendar import Calendar

# Queueing Network Parameters
SESSION_ARRIVAL_RATE = 35.0     # requests/second (exponentially distributed
SESSION_LENGTH_LW = 5           # requests/session (equilikely distributed, min)
SESSION_LENGTH_UB = 35          # requests/session (equilikely distributed, max)
THINK_AVERAGE = 7.0             # seconds/request (exponentially distributed)
FEND_SERVICE_AVERAGE = 0.00456  # seconds/request (exponentially distributed)
BEND_SERVICE_AVERAGE = 0.00117  # seconds/request (exponentially distributed)

# Events
SESSION_ARRIVAL = 0
REQUEST_ARRIVAL = 1
FEND_COMPLETION = 2
BEND_COMPLETION = 3

# Random Generator
rndgen.plant_seeds(123456789)
STREAM_SESSION_ARRIVAL = 0
STREAM_REQUEST_ARRIVAL = 1
STREAM_FEND_COMPLETION = 2
STREAM_BEND_COMPLETION = 3
STREAM_SESSION_LENGTH = 4

# Simulation Parameters
START = 0.0
STOP = 3600.0

# Calendar
calendar = Calendar([
    SESSION_ARRIVAL,
    REQUEST_ARRIVAL,
    FEND_COMPLETION,
    BEND_COMPLETION
], t_clock=START)


# Random timing Functions
def get_session_inter_arrival():
    """
    Generates a session interarrival time, exponentially distributed with rate
    *SESSION_ARRIVAL_RATE*.
    :return (float) session interarrival time.
    """
    rndgen.select_stream(STREAM_SESSION_ARRIVAL)
    u = rndgen.rnd()
    m = 1.0 / SESSION_ARRIVAL_RATE
    t_session_inter_arrival = rndvar.exponential(m, u)
    return t_session_inter_arrival


def get_session_length():
    """
    Generates the number of requests per session, equilikely distributed in
    *[SESSION_LENGTH_LB, SESSION_LENGTH_UB]*.
    :return: (int) number of requests per session.
    """
    rndgen.select_stream(STREAM_SESSION_LENGTH)
    u = rndgen.rnd()
    a = SESSION_LENGTH_LW
    b = SESSION_LENGTH_UB
    requests = rndvar.equilikely(a, b, u)
    return requests


def get_terminal_think():
    """
    Generates a terminal think-time, exponentially distributed with average
    *THINK_AVERAGE*.
    :return (float) think-time.
    """
    global calendar
    rndgen.select_stream(STREAM_REQUEST_ARRIVAL)
    u = rndgen.rnd()
    m = THINK_AVERAGE
    t_think = rndvar.exponential(m, u)
    return t_think


def get_fend_service():
    """
    Generates a front-end service-time, exponentially distributed with average
    *FEND_SERVICE_AVERAGE*.
    :return (float) front-end service-time.
    """
    rndgen.select_stream(STREAM_FEND_COMPLETION)
    u = rndgen.rnd()
    m = FEND_SERVICE_AVERAGE
    t_fend_service = rndvar.exponential(m, u)
    return t_fend_service


def get_bend_service():
    """
    Generates a back-end service-time, exponentially distributed with average
    *BEND_SERVICE_AVERAGE*.
    :return (float) back-end service-time.
    """
    rndgen.select_stream(STREAM_BEND_COMPLETION)
    u = rndgen.rnd()
    m = BEND_SERVICE_AVERAGE
    t_bend_service = rndvar.exponential(m, u)
    return t_bend_service

# States
n_sess = 0
n_fend = 0
n_bend = 0

# System Metrics
completed_sessions = 0
completed_requests = 0
dropped_sessions = 0
aborted_requests = 0

# Front-End metrics
track_fend = NodeMetricTracker()

# Back-End metrics
track_bend = NodeMetricTracker()

# Session id
SID = 0

# Data structures
sess_length = dict()
fend_queue = []
bend_queue = []

t_last = START

# Simulation
t_session_arrival = calendar.get_clock() + get_session_inter_arrival()
calendar.schedule(SESSION_ARRIVAL, t_session_arrival, SID)
while calendar.get_clock() < STOP:
    event_class, event_time, event_sid = calendar.get_next_event()

    track_fend.update(event_time, n_fend)
    track_bend.update(event_time, n_bend)

    calendar.set_clock(event_time)

    if event_class is SESSION_ARRIVAL:  # handle session arrival
        n_sess += 1
        t_last = event_time
        sess_length[event_sid] = get_session_length()
        calendar.schedule(REQUEST_ARRIVAL, event_time, event_sid)
        SID += 1
        t_session_arrival = calendar.get_clock() + get_session_inter_arrival()
        if t_session_arrival < STOP:
            calendar.schedule(SESSION_ARRIVAL, t_session_arrival, SID)
        else:
            calendar.mark_impossible(SESSION_ARRIVAL)

    elif event_class is REQUEST_ARRIVAL:  # handle request arrival
        n_fend += 1
        if n_fend > 1:
            fend_queue.append(event_sid)
        else:
            t_fend_completion = calendar.get_clock() + get_fend_service()
            calendar.schedule(FEND_COMPLETION, t_fend_completion, event_sid)
        calendar.mark_impossible(REQUEST_ARRIVAL)

    elif event_class is FEND_COMPLETION:  # handle front-end completion
        n_fend -= 1
        if n_fend > 0:
            sid = fend_queue.pop()
            t_fend_completion = calendar.get_clock() + get_fend_service()
            calendar.schedule(FEND_COMPLETION, t_fend_completion, sid)
        else:
            calendar.mark_impossible(FEND_COMPLETION)

        n_bend += 1
        if n_bend > 1:
            bend_queue.append(event_sid)
        else:
            t_bend_completion = calendar.get_clock() + get_bend_service()
            calendar.schedule(BEND_COMPLETION, t_bend_completion, event_sid)

    elif event_class is BEND_COMPLETION:  # handle back-end completion
        n_bend -= 1
        completed_requests += 1
        if n_bend > 0:
            sid = bend_queue.pop()
            t_bend_completion = calendar.get_clock() + get_bend_service()
            calendar.schedule(BEND_COMPLETION, t_bend_completion, sid)
        else:
            calendar.mark_impossible(BEND_COMPLETION)

        sess_length[event_sid] -= 1
        if sess_length[event_sid] > 0:
            t_request_arrival = calendar.get_clock() + get_terminal_think()
            calendar.schedule(REQUEST_ARRIVAL, t_request_arrival, event_sid)
        else:
            n_sess -= 1
            completed_sessions += 1
            del sess_length[event_sid]

    else:
        pass


# Report
simulation_time = calendar.get_clock()
total_handled_sessions = n_sess + completed_sessions
total_handled_requests = n_fend + n_bend + completed_requests
average_inter_arrival_time = t_last / total_handled_sessions
throughput = completed_sessions / simulation_time
average_response_time = (track_fend.node + track_bend.node) / completed_requests

fend_average_wait = track_fend.node / completed_requests
fend_average_delay = track_fend.queue / completed_requests
fend_average_service = track_fend.service / completed_requests
fend_average_requests_in_node = track_fend.node / simulation_time
fend_average_requests_in_queue = track_fend.queue / simulation_time
fend_utilization = track_fend.service / simulation_time

bend_average_wait = track_bend.node / completed_requests
bend_average_delay = track_bend.queue / completed_requests
bend_average_service = track_bend.service / completed_requests
bend_average_requests_in_node = track_bend.node / simulation_time
bend_average_requests_in_queue = track_bend.queue / simulation_time
bend_utilization = track_bend.service / simulation_time

drop_ratio = dropped_sessions / total_handled_sessions
abort_ratio = aborted_requests / total_handled_requests

print('==========================================')
print('SIMULATION - WEB SERVICE                  ')
print('==========================================')
print('Simulation Time                 : %d  ' % simulation_time)
print('Total handled sessions          : %d  ' % total_handled_sessions)
print('Total handled requests          : %d  ' % total_handled_requests)
print('Average session inter-arrival   : %.5f' % average_inter_arrival_time)
print('Throughput                      : %.5f' % throughput)
print('Average response time           : %.5f' % average_response_time)
print('Drop Ratio                      : %.5f' % drop_ratio)
print('Abort Ratio                     : %.5f' % abort_ratio)
print('------------------------------------------')
print('Front-End Statistics:')
print('\tAverage wait               : %.5f' % fend_average_wait)
print('\tAverage delay              : %.5f' % fend_average_delay)
print('\tAverage service            : %.5f' % fend_average_service)
print('\tAverage requests in node   : %.5f' % fend_average_requests_in_node)
print('\tAverage requests in queue  : %.5f' % fend_average_requests_in_queue)
print('\tUtilization                : %.5f' % fend_utilization)
print('------------------------------------------')
print('Back-End Statistics:')
print('\tAverage wait               : %.5f' % bend_average_wait)
print('\tAverage delay              : %.5f' % bend_average_delay)
print('\tAverage service            : %.5f' % bend_average_service)
print('\tAverage requests in node   : %.5f' % bend_average_requests_in_node)
print('\tAverage requests in queue  : %.5f' % bend_average_requests_in_queue)
print('\tUtilization                : %.5f' % bend_utilization)


if __name__ == '__main__':
    simparams = SimulationParameters()