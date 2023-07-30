class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.error_sum = 0
        self.prev_error = 0
        
    def update(self, error):
        self.error_sum += error
        p_term = self.Kp * error
        i_term = self.Ki * self.error_sum * self.dt
        d_term = self.Kd * (error - self.prev_error) / self.dt
        self.prev_error = error
        return p_term + i_term + d_term

class Controller:
    def __init__(self, Kp_steering, Ki_steering, Kd_steering, Kp_throttle, Ki_throttle, Kd_throttle, dt):
        self.pid_steering = PIDController(Kp_steering, Ki_steering, Kd_steering, dt)
        self.pid_throttle = PIDController(Kp_throttle, Ki_throttle, Kd_throttle, dt)
        self.steering = 0
        self.throttle = 0
    
    def update(self, processed_frame):
        offset = processed_frame['offset']
        self._update_steering(offset)
        self._update_throttle(offset)
        # radius = processed_frame['offset']
        
        self._update_steeringupdate_steering(offset)
        self._update_throttle(offset)
        
        return
        
    def _update_steering(self, offset): # PID based on offset to control steering
        self.steering = self.pid_steering.update(offset)

    def _update_throttle(self, offset):
        self.throttle = self.pid_throttle.update(offset)